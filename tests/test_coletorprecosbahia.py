import unittest
from src.coletorprecosbahia import ColetorPrecosBahia
import os
import pandas as pd


# Testa as funções do Coletor de Precos Bahia
class TestColetorPrecosBahia(unittest.TestCase):
    def setUp(self):
        self.coletor = ColetorPrecosBahia()

    # Teste de preço válido
    def test_formatar_preco_valido(self):
        self.assertEqual(self.coletor.formatar_preco("R$ 1.234,56"), 1234.56)
        self.assertEqual(self.coletor.formatar_preco("R$ 0,99"), 0.99)
        self.assertEqual(self.coletor.formatar_preco("R$ 123"), 123.0)

    # Teste de preço inválido
    def test_formatar_preco_invalido(self):
        with self.assertRaises(ValueError):
            self.coletor.formatar_preco("Preço inválido")

    # Teste de extração de informações de endereço
    def test_extrair_endereco_completo(self):
        endereco = "Rua das Flores 123 Bairro Jardim 12345678, Salvador"
        resultado = self.coletor.extrair_endereco(endereco)
        esperado = {
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Bairro Jardim",
            "cep": "12345678",
            "cidade": "Salvador",
            "uf": "BA",
        }
        self.assertEqual(resultado, esperado)

    # Teste de adição de resultados
    def test_adicionar_resultados(self):
        produto1 = {
            "ean": "1234567890123",
            "descricao": "Produto Teste 1",
            "preco": 10.99,
            "data_coleta": "2023-10-01 12:00:00",
            "codmunicipio": 2910800,
            "codestado": "29",
            "rede_fonte": "Loja Teste 1",
            "logradouro": "Rua Teste 1",
            "bairro": "Bairro Teste 1",
            "cep": "12345678",
            "cidade": "Salvador",
            "uf": "BA",
        }
        produto2 = {
            "ean": "9876543210987",
            "descricao": "Produto Teste 2",
            "preco": 20.99,
            "data_coleta": "2023-10-02 12:00:00",
            "codmunicipio": 2927408,
            "codestado": "29",
            "rede_fonte": "Loja Teste 2",
            "logradouro": "Rua Teste 2",
            "bairro": "Bairro Teste 2",
            "cep": "87654321",
            "cidade": "Feira de Santana",
            "uf": "BA",
        }
        # Adicionando produtos ao resultado
        self.coletor.adicionar_resultado(produto1)
        self.coletor.adicionar_resultado(produto2)

        # Verificando se os produtos foram adicionados corretamente
        self.assertEqual(len(self.coletor.resultado), 2)

        # Verifica se a descrição dos produtos está correta e na ordem correta
        self.assertEqual(self.coletor.resultado.iloc[0]["descricao"], "Produto Teste 1")
        self.assertEqual(self.coletor.resultado.iloc[1]["descricao"], "Produto Teste 2")

    # Teste de limpeza de resultados
    def test_limpar_resultado(self):
        produto = {
            "ean": "1234567890123",
            "descricao": "Produto Teste",
            "preco": 10.99,
            "data_coleta": "2023-10-01 12:00:00",
            "codmunicipio": 2910800,
            "codestado": "29",
            "rede_fonte": "Loja Teste",
            "logradouro": "Rua Teste",
            "bairro": "Bairro Teste",
            "cep": "12345678",
            "cidade": "Salvador",
            "uf": "BA",
        }
        # Adiciona o resultado
        self.coletor.adicionar_resultado(produto)

        # Verifica se o resultado possui um produto
        self.assertFalse(self.coletor.resultado.empty)

        # Limpa o resultado
        self.coletor.limpar_resultados()

        # Verifica se o resultado está vazio
        self.assertTrue(self.coletor.resultado.empty)

    # Teste de salvamento de resultados
    def test_salvar_resultado(self):
        produto = {
            "ean": "1234567890123",
            "descricao": "Produto Teste",
            "preco": 10.99,
            "data_coleta": "2023-10-01 12:00:00",
            "codmunicipio": 2910800,
            "codestado": "29",
            "rede_fonte": "Loja Teste",
            "logradouro": "Rua Teste",
            "bairro": "Bairro Teste",
            "cep": "12345678",
            "cidade": "Salvador",
            "uf": "BA",
        }
        # Adiciona o resultado
        self.coletor.adicionar_resultado(produto)
        self.coletor.salvar_arquivo_resultados("test.csv", "test.json")

        # Verifica se os arquivos foram criados
        caminho_output = "output"
        caminho_csv = os.path.join(caminho_output, "test.csv")
        caminho_json = os.path.join(caminho_output, "test.json")
        self.assertTrue(os.path.exists(caminho_csv))
        self.assertTrue(os.path.exists(caminho_json))

        # Lê o arquivo CSV para verificar se o produto foi salvo corretamente
        df = pd.read_csv(caminho_csv)
        self.assertEqual(df.iloc[0]["descricao"], "Produto Teste")


if __name__ == "__main__":
    unittest.main()
