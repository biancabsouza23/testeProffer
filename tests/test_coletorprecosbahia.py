import unittest
from src.coletorprecosbahia import ColetorPrecosBahia
import os
import pandas as pd


class TestColetorPrecosBahia(unittest.TestCase):
    def setUp(self):
        self.coletor = ColetorPrecosBahia()

    def test_formatar_preco_valido(self):
        self.assertEqual(self.coletor.formatar_preco("R$ 1.234,56"), 1234.56)
        self.assertEqual(self.coletor.formatar_preco("R$ 0,99"), 0.99)
        self.assertEqual(self.coletor.formatar_preco("R$ 123"), 123.0)

    def test_formatar_preco_invalido(self):
        with self.assertRaises(ValueError):
            self.coletor.formatar_preco("Preço inválido")

    def test_extrair_endereco_completo(self):
        endereco = "Rua das Flores 123 Bairro Jardim 12345678, Salvador"
        resultado = self.coletor.extrair_endereco(endereco)
        esperado = {
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Bairro Jardim",
            "cep": "12345678",
            "cidade": "Salvador",
            "uf": "",
        }
        self.assertEqual(resultado, esperado)

    def test_criar_resultado_com_dataframe_vazio(self):
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
        self.coletor.criar_resultado(produto)
        self.assertEqual(len(self.coletor.resultado), 1)
        self.assertEqual(self.coletor.resultado.iloc[0]["descricao"], "Produto Teste")

    def test_criar_resultado_com_dataframe_existente(self):
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
        self.coletor.criar_resultado(produto1)
        self.coletor.criar_resultado(produto2)
        self.assertEqual(len(self.coletor.resultado), 2)
        self.assertEqual(self.coletor.resultado.iloc[1]["descricao"], "Produto Teste 2")

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
        self.coletor.criar_resultado(produto)
        self.coletor.salvar_resultado("test.csv", "test.json")
        caminho_output = "output"
        caminho_csv = os.path.join(caminho_output, "test.csv")
        caminho_json = os.path.join(caminho_output, "test.json")
        self.assertTrue(os.path.exists(caminho_csv))
        self.assertTrue(os.path.exists(caminho_json))
        df = pd.read_csv(caminho_csv)

        self.assertEqual(df.iloc[0]["descricao"], "Produto Teste")


if __name__ == "__main__":
    unittest.main()
