from coletorprecosbahia import ColetorPrecosBahia
import json

coletor = ColetorPrecosBahia()
# Nome do arquivo JSON
arquivo_json = "lista_eans.json"

# Abrindo e lendo o arquivo JSON
with open(arquivo_json, "r", encoding="utf-8") as f:
    lista_eans = json.load(f)  # Carrega a lista

#for ean in lista_eans:
    coletor.pesquisar_produto('7896321017666')
