from coletorprecosbahia import ColetorPrecosBahia
import json

coletor = ColetorPrecosBahia()
# Nome do arquivo JSON
arquivo_json = "lista_eans_copy.json"

# Abrindo e lendo o arquivo JSON
with open(arquivo_json, "r", encoding="utf-8") as f:
    lista_eans = json.load(f)  # Carrega a lista

for ean in lista_eans:
    coletor.pesquisar_produto(ean)

coletor.salvar_resultado("resultado.csv", "resultado.json")
coletor.fechar_navegador()