import pandas as pd
from unidecode import unidecode 
from selenium import webdriver

df = pd.read_excel("commodities.xlsx")

def remover_acento(text):
    return unidecode(text)

lista_produtos = []

for linha in df.index:
    produto = df.loc[linha, "Produto"]

    if any(c in produto for c in 'áéíóúâêîôûãõÁÉÍÓÚÂÊÎÔÛÃÕ'):
        produto_sem_acento = remover_acento(produto)
        lista_produtos.append(produto_sem_acento.lower())
    else:
        lista_produtos.append(produto.lower())
           
navegador = webdriver.Chrome()

for linha, produto in enumerate(lista_produtos):

    link = f"https://www.melhorcambio.com/{produto}-hoje"
    
    navegador.get(link)
    preco_produto = navegador.find_element("xpath", '//*[@id="comercial"]').get_attribute("value")
    preco_produto = preco_produto.replace(".", "").replace(",", ".")
    
    df.loc[linha, "Preço Atual"] = preco_produto
    
navegador.quit()

df["Preço Atual"] = pd.to_numeric(df["Preço Atual"], errors="coerce")

for index, row in df.iterrows():
    if row["Preço Atual"] < row["Preço Ideal"] and row["Preço Atual"] != 0:
        df.at[index, "Comprar"] = "Comprar"
    elif row["Preço Atual"] > row["Preço Ideal"]:
        df.at[index, "Comprar"] = "Não Comprar"
    elif row["Preço Atual"] == 0:
        df.at[index, "Comprar"] = "Valor Não Encontrado"
    else:
        df.at[index, "Comprar"] = "ERROR" 

df.to_excel("nova_commodities.xlsx", index=False)

print("### SCRIPT FINALIZADO ###")