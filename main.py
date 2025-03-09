from src.coletorprecosbahia import ColetorPrecosBahia
import json

# Instanciando o coletor responsávl por controlar o navegador
coletor = ColetorPrecosBahia()  #

# definindo caminho do arquivo json e carregando a lista de eans
arquivo_json_EANs_salvador = "data/lista_eans_copy.json"
arquivo_json_Descricao_salvador = "data/lista_descricao_copy.json"
arquivo_json_EANs_feira = "data/lista_eans_copy.json"
arquivo_json_Descricao_feira = "data/lista_descricao_copy.json"


# Abrindo e lendo o arquivo JSON
with open(arquivo_json_EANs_feira, "r", encoding="utf-8") as f:
    lista_eans = json.load(f)  # Carrega a lista
with open(arquivo_json_Descricao_feira, "r", encoding="utf-8") as f:
    lista_descricao = json.load(f)  # Carrega a lista

# Coleta via ambos os métodos
for cidade in ["feira de santana", "salvador"]:
    coletor.mudar_cidade(cidade)
    # for ean in lista_eans:
    #     coletor.pesquisar_produto(ean)
    for descricao in lista_descricao:
        coletor.pesquisar_produto(descricao)

# Salvando os resultados em CSV e JSON
coletor.salvar_resultado("resultado.csv", "resultado.json")

# Fechando o navegador
coletor.fechar_navegador()
