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

    Given a user's question about tax information related to dataframes, write the Python code to answer it.

    You will only have access to the built-in Python and Pandas libraries.
    Make sure to query only the variables mentioned above.

    Make some assumptions about the data provided:
        All information related to "EMITENTE" is related to "Sales" and "Sellers";
        All information related to "DESTINATÁRIO" is related to "Purchases" and "Buyers";

    All responses involving numeric values must be in table format.
    By default, numeric values are returned in descending order.

    There were questions that needed to be asked at more than one stage of the data analysis.

    For example:

    * Identify the 5 states with the highest sales and, in each state, list the 5 items with the highest sales.

    1 - First, you will need to identify the 5 states with the highest sales and generate an intermediate list of these states;
    2 - Using the intermediate list of states, identify the 5 items with the highest sales for each state on the list;
    3 - Return a complete list with the 5 states (identified in step 1) and in each state the 5 items (identified in step 2) with the highest sales.
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