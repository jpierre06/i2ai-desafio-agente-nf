from langchain_experimental.tools import PythonAstREPLTool
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser

def run_csv_question_chain(question: str, locals: dict, api_key: str):
    
    tool = PythonAstREPLTool(locals=locals)

    llm = init_chat_model(
        model="gemini-2.0-flash",
        model_provider="google_genai",
        api_key=api_key  # chave passada explicitamente
    )

    llm_with_tool = llm.bind_tools(tools=[tool], tool_choice=tool.name)

    df_template = """\`\`\`python
    {df_name}.head().to_markdown()
    >>> {df_head}
    \`\`\`"""

    df_context = "\n\n".join(
        df_template.format(df_head=_df.head().to_markdown(), df_name=df_name)
        for _df, df_name in [(locals["heads"], "heads"), (locals["items"], "items")]
    )

    system = f"""
    Você é um agente especialista em análise de dados tributários do Brasil, com foco em dados estruturados em DataFrames do Pandas.

    Sua função é responder perguntas do usuário com base nesses dados, gerando código Python que utilize exclusivamente:
        * Bibliotecas padrão do Python;
        * A biblioteca pandas (já importada como import pandas as pd).

    Dados disponíveis
        Você terá acesso a múltiplos DataFrames, fornecidos dinamicamente no contexto de cada tarefa.

    Abaixo está um exemplo da estrutura dos DataFrames, incluindo algumas linhas de dados de cabecalho e itens de notas fiscais

    {df_context}

    Use essas informações para compreender a estrutura dos dados e desenvolver sua análise.

    Regras e Suposições

    Assuma o seguinte mapeamento semântico:
        * Tudo relacionado ao EMITENTE diz respeito a Vendas, Vendedores, Entregas;
        * Tudo relacionado ao DESTINATÁRIO diz respeito a Compras, Compradores e Recebimento.

    Restrições técnicas:
        * Utilize apenas as variáveis e bibliotecas mencionadas;
        * Não crie variáveis fictícias nem consulte fontes externas.

    Formato da Resposta:
        * Toda resposta com valores numéricos deve estar em formato tabular (DataFrame);
        * Formatar valores númericos com separador de milhar e seperador decimal para ser utilizado posteriormente pela biblioteca tabulate para exibição dos dados em formato de texto;
        * Os valores numéricos devem ser ordenados em ordem decrescente por padrão, salvo solicitação contrária.
        
    Caso a análise envolva múltiplas etapas, execute e descreva cada etapa sequencialmente, com clareza
    Exemplo de Fluxo de Análise por Etapas

    Pergunta:
    Quais são os 5 estados com as maiores vendas e, para cada um deles, os 5 itens mais vendidos?

    Passos esperados:
        * Filtrar as vendas por estado do EMITENTE e somar os valores;
        * Selecionar os 5 estados com maiores vendas;
        * Para cada um desses estados, identificar os 5 produtos com maiores vendas;
        * Exibir os resultados em formato organizado e estruturado por estado.

    Objetivo final:
    Dado qualquer questionamento do usuário relacionado aos dados tributários carregados, gere apenas o código Python necessário para executar a análise solicitada, sempre seguindo as regras acima.
    """

    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])

    parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)
    
    # Etapas separadas: gerar código -> executar
    chain_to_code = prompt | llm_with_tool | parser
    python_code = chain_to_code.invoke({"question": question})

    try:
        # Agora executa o código gerado
        resultado = tool.invoke(python_code)
        
    except Exception as e:
        resultado = f"⚠️ Ocorreu um erro ao processar sua pergunta: {str(e)}"
        python_code = "Error."

    return resultado, python_code