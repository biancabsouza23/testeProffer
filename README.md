# README - Projeto de Coleta de Dados
autor: [Bianca Bastos de Souza](git@github.com:biancabsouza23/testeProffer.git)

## Descrição do Projeto
Este projeto foi desenvolvido como parte do processo seletivo para estágio na Proffer. O objetivo é coletar informações de preços de produtos do site Preço da Hora Bahia para as cidades de Salvador e Feira de Santana, utilizando listas de EANs e descrições de produtos fornecidas em formato JSON.

## Arquitetura e Tecnologias Utilizadas
A solução foi implementada em **Python**, utilizando as seguintes tecnologias:

- **Selenium**: Para automação da navegação no site e extração dos dados.
- **Pandas**: Para manipulação e armazenamento estruturado dos dados coletados.
- **JSON**: Para carregamento das listas de produtos.
- **CSV**: Para armazenamento final dos dados coletados.
- **WebDriverManager**: Para gerenciamento automático do driver do Chrome.

## Como Executar o Projeto

### Requisitos
Antes de executar o projeto, certifique-se de ter instalado:
- Python 3.12
- Google Chrome
- WebDriver compatível com sua versão do Chrome
- Bibliotecas necessárias (instale com `pip install -r requirements.txt` caso um arquivo de dependências seja fornecido)
- Lista de EANs e Descrições na pasta `data/`

### Execução
```sh
# Clone este repositório
git clone <git@github.com:biancabsouza23/testeProffer.git>
cd <testeProffer>

# Execute o script principal
python main.py
```

Os resultados serão salvos na pasta `output/` nos formatos `.csv` e `.json`.

## Como os Dados São Coletados
1. O sistema carrega as listas de EANs e descrições de produtos.
2. Para cada cidade (Salvador e Feira de Santana), a ferramenta:
   - Alterna a cidade no site.
   - Realiza buscas pelos produtos utilizando suas descrições.
   - Captura dados disponíveis, incluindo preço, descrição e localização do estabelecimento.
3. Os dados são processados e salvos em um DataFrame pandas.
4. Os resultados são exportados para CSV e JSON.

## Desafios Encontrados e Soluções
### CAPTCHA no site
- Foi implementado um método para detectar CAPTCHA e solicitar resolução manual antes de continuar a execução. O usuário deve apertar a tecla "enter" no terminal após resolver o captcha. O usuário é avisado por um alerta sonoro quando um captcha é detectado. Inicialmente foi tentada a utilização de uma lista circular de proxys, mas não deu certo. Acredito que, caso seja contratada, minha experiência e aprendizagem na Proffer me ajudarão a lidar melhor com desafios como esses. Por isso também que optei por utilizar uma quantidade menor de EANs e descrições, para tonar possível a resolução manual dos captchas em tempo hábil.

### Variações na estrutura da página
- O código foi estruturado para lidar com diferenças na presença de descontos e estrutura dos elementos HTML.

### Erros na pesquisa de produtos
- Implementamos tratamento de exceções para registrar produtos não encontrados e evitar falhas na execução.

## Possíveis Melhorias
- Paralelização das buscas para reduzir o tempo de execução.
- Melhor tratamento de CAPTCHA usando soluções automáticas.
- Implementação de um sistema de logs para melhor acompanhamento da execução.
- Suporte para mais cidades e categorias de produtos.

## Conclusão

A solução é capaz de coletar informações de preço de produtos a partir do site Preço da Hora Bahia utilizando Selenium e Pandas. Com futuras melhorias, a solução pode ser otimizada para levar menos tempo e coletar mais itens em paralelo.


