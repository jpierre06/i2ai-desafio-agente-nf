# 📌 Desbravando IA

Bem-vindo ao **Desbravando IA**! Este repositório reúne projetos e experimentos relacionados à Inteligência Artificial, com o objetivo de explorar e aprender técnicas modernas de forma acessível.

## 🔧 Tecnologias utilizadas

Este repositório utiliza as seguintes tecnologias:

- [Python](https://www.python.org/): Linguagem principal para desenvolvimento dos projetos.
- [Docker](https://www.docker.com/): Para criar ambientes isolados e facilitar a execução dos projetos.
- [Pandas](https://pandas.pydata.org/): Para manipulação e análise de dados.
- [LangChain](https://www.langchain.com/): Para construção de aplicações baseadas em modelos de linguagem.
- [Streamlit](https://streamlit.io/): Para criação de interfaces interativas e visualização de resultados.

## 🚀 Como usar este repositório?

### 🌐 Acesso na Web

A versão online do sistema está disponível em:
🔗 https://agente-ia-nf-main-kyr3p7syqfwz3ky23c4bpd.streamlit.app/

### 📥 Para uso local

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/seu-usuario/Desbravando-IA.git
    ```
2. **Construa a imagem Docker**:
    ```bash
    docker-compose build
    ```
3. **Execute o container**:
    ```bash
    docker-compose up -d
    ```
4. **Acesse a aplicação**:
    - Abra o navegador e vá para `http://0.0.0.0:8501/` para interagir com a interface criada em Streamlit.

## 📁 Estrutura do Projeto

A solução foi organizada de forma a facilitar a navegação e o entendimento, tanto para iniciantes quanto para desenvolvedores experientes. Abaixo está a estrutura principal do repositório:

- **/core**: Contém arquivos com as funções de ler arquivos .csv `get_csv_content`, carregar dataframe apartir de arquivo .zip `load_dataframes`, salvar histórico de logs `save_chat_log` e fazer perguntas sobre os arquivos para a LLM `run_csv_question_chain`.
- **/data**: Contém arquivo .zip que compacta arquivos .csv utilizados por agente de IA.
- **/pages**: Contém as páginas de listagem de cabeçalhos e itens de notas fiscais construidas utilizando streamlit.
- **requirements.txt**: Lista todas as dependências necessárias para executar os projetos localmente.
- **Dockerfile**: Arquivo para criar um ambiente Docker isolado, garantindo que a solução funcione de forma consistente em diferentes sistemas.
- **app.py**: Arquivo principal para a interface interativa criada com Streamlit, permitindo a visualização e interação com os resultados dos projetos.

## ✍️ Como contribuir?

Sinta-se à vontade para enviar sugestões, correções ou melhorias.
Crie uma issue ou envie um pull request.

## 📝 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.