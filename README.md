# Automação de Coleta e Análise de Cotação de Commodities

###
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT) 

### Sobre:

Elaboração de um script (algoritmo) visando à automatização do processo de obter informações de commodities.

### Proposta:

Desenvolver um script que automatize a coleta de cotações de commodities, analisar se o valor está abaixo do preço ideal definido no conjunto de dados para compra e, se for o caso, atualize com as indicações de compra. O resultado final será exportado em um novo arquivo .**xlsx**.

O site utilizado para a coleta das cotações foi o  <a href="https://www.melhorcambio.com/">**Melhor Câmbio**</a>

### Estrutura do Repositório:
- <strong>data:</strong> Encontrará o arquivo **.xlsx** do dataset base para pesquisa e o dataset gerado ao fim do script.
- <strong>img:</strong> Aqui você encontrará os prints obtidos durante o processo.
- <strong>script:</strong> Este diretório contém o script desenvolvido.
- <strong>readme_translated:</strong> This repository contains the **PDF** with the **report** translated into English.

### Linguagem Utilizada:
###
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white&color=black)

### Bibliotecas Utilizadas:
###
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white&color=black) ![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white&color=black)

### Metodologia:

No início, foi empregado a biblioteca **Pandas** para efetuar a importação e a leitura do conjunto de dados. 
###
<img src="/img/dataset.png">

###
Foi possível identificar as commodities para as quais os valores atuais seriam coletados e os preços ideais.

Em seguida, foi feito o tratamento dos nomes dos produtos, onde alguns apresentavam a primeira letra em maiúscula e ou contendo acentuação. Para realizar essa tarefa, foi utilizada a biblioteca **Unidecode**. 

Inicialmente, uma função foi criada para eliminar caracteres do texto. Um loop **for** foi utilizado para percorrer as linhas, exigindo uma estrutura condicional.

###
```
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
```

###
O trecho de código **if any(c in produto for c in 'áéíóúâêîôûãõÁÉÍÓÚÂÊÎÔÛÃÕ')** verifica se algum dos caracteres acentuados da lista está presente na variável **"produto"**. Se pelo menos um desses caracteres estiver presente, a expressão **any(...)** será avaliada como **verdadeira**; caso contrário, será avaliada como **falsa**.

Por fim, a função **.append** foi utilizada para criar uma nova lista contendo as modificações necessárias.

A coleta automatizada teve sua implementação através da utilização do framework **Webdriver** do **Selenium**.

###
```
navegador = webdriver.Chrome()

for linha, produto in enumerate(lista_produtos):

    link = f"https://www.melhorcambio.com/{produto}-hoje"
    
    navegador.get(link)
    preco_produto = navegador.find_element("xpath", '//*[@id="comercial"]').get_attribute("value")
    preco_produto = preco_produto.replace(".", "").replace(",", ".")
    
    df.loc[linha, "Preço Atual"] = preco_produto
    
navegador.quit()
```

###
O **xpath** foi utilizado como ponto de referência para extrair o atributo **"value"**, sendo necessário, em seguida, efetuar a substituição de vírgulas por pontos, a fim de se adequar ao padrão do **Python**.

O uso da função **enumerate** permitiu a obtenção do índice e do valor do produto, possibilitando, assim, a atualização do DataFrame durante a iteração do loop.

Processamento da coluna **"Preço Atual"** e à subsequente o preenchimento da coluna **"Comprar"** com as informações essenciais. Este último passo envolveu a aplicação das devidas operações para garantir a precisão da inserção das indicações apropriadas na coluna **"Comprar"**.

###
```
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
```

###
O resultado final foi exportado em um novo arquivo **xlsx**.
###
<img src="/img/dataset_atualizado.png">

###
**Obs:** Os valores obtidos são referentes ao dia da publicação deste repositório. 

### Conclusão:

Ao longo deste processo de automação de coleta e análise de cotações de commodities, diversas etapas foram realizadas para otimizar e agilizar a obtenção de dados.

A etapa final, que incluiu o processamento da coluna **"Preço Atual"** e o preenchimento da coluna **"Comprar"** com as informações necessárias, adicionou um elemento estratégico à análise.

O resultado desse processo de automação e análise foi um novo arquivo **.xlsx**, contendo as informações relevantes das cotações das commodities e as marcações de compra. Essa abordagem não apenas economizou tempo e esforço, mas também contribuiu para tomadas de decisão mais eficazes. A automação demonstrou ser uma ferramenta valiosa na simplificação e agilização de processos, impulsionando a eficiência e a precisão na gestão e análise.

---
### Contato:

<div>
  <a href="https://linkedin.com/in/marcospontesjunior" target="_blank"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white&color=black" target="_blank"></a>  
  <a href = "mailto:marcospntsjunior@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white&color=black" target="_blank"></a>
</div>
