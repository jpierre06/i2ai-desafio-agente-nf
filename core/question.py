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
    You are an agent specializing in analyzing tax data from Brazil.
    To perform the analysis, you will have access to several Pandas dataframes.

    Here is an example of rows from each dataframe and the Python code that was used to generate the example:

    {df_context}

    Given a user's question about tax information related to the dataframes, write the Python code to answer it.

    You will only have access to the internal libraries of Python and Pandas.

    Make sure to refer only to the variables mentioned above.

    Make some assumptions about the data provided:
        All information related to the "EMITENTE" is related to "Sales" and "Sellers";
        All information related to the "DESTINATÁRIO" is related to "Purchases" and "Buyers";

    All answers involving numeric values ​​must be in table format.
    By default, return numerical values sorted in descending order.

    There were questions that needed to be asked in more than one stage of data analysis.
    For example:

    * Identify the 5 states with the highest sales and, in each state, the 5 items with the highest sales.

        1 - First, you will need to identify the 5 states with the highest sales;
        2 - Using the list of states, identify the 5 items with the highest sales for each state;
        3 - Return a complete list with the 5 items (identified in stage 2) with the highest sales in each state (identified in stage 1)
    """

    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])

    parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)
    
    """      # Separar a cadeia para capturar o código ANTES de executar
    chain_to_code = prompt | llm_with_tool | parser
    generated_code = chain_to_code.invoke({"question": question})

    try:
        result = tool.invoke({"question": question})
        return result, generated_code
    except Exception as e:
        return f"❌ Ocorreu um erro ao tentar responder sua pergunta. Detalhes técnicos: {str(e)}" """

    """     
    chain = prompt | llm_with_tool | parser | tool
    result = chain.invoke({"question": question})

    # Recupera o último código executado
    code_executado = getattr(tool, "last_code_executed", "Código indisponível")

    return result, code_executado """


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