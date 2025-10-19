from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from config import (
    OPENAI_MODEL_NAME,
    OPENAI_MODEL_TEMPERATURE,
    ENABLE_GOOGLE_CALENDAR,
)
from memory import get_session_history
from vectorstore import get_vectorstore
from prompts import get_contextualize_prompt, get_qa_prompt


def get_rag_chain(contextualize_prompt_text, system_prompt_text):
    # Inicializa o LLM (desabilitando streaming para evitar erro 400)
    llm = ChatOpenAI(
        model=OPENAI_MODEL_NAME,
        temperature=OPENAI_MODEL_TEMPERATURE,
        streaming=False,  # Desabilita streaming para evitar erro de organização
    )

    # Recuperador de vetores
    retriever = get_vectorstore().as_retriever()
    contextualize_prompt = get_contextualize_prompt(contextualize_prompt_text)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_prompt)

    # Chain de QA ajustada para aceitar a variável "context"
    qa_prompt = get_qa_prompt(system_prompt_text)
    question_answer_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=qa_prompt,
        document_variable_name="context"  # ESSENCIAL: indica que o texto recuperado estará na variável 'context'
    )

    # Cria o chain completo de RAG
    return create_retrieval_chain(history_aware_retriever, question_answer_chain)


def get_conversational_rag_chain(contextualize_prompt_text, system_prompt_text):
    # Se o Google Calendar estiver habilitado, usa agent com tools
    if ENABLE_GOOGLE_CALENDAR:
        try:
            from calendar_tools import CALENDAR_TOOLS
            return get_agent_with_tools(contextualize_prompt_text, system_prompt_text, CALENDAR_TOOLS)
        except Exception as e:
            print(f"Erro ao carregar ferramentas do Google Calendar: {e}")
            print("Continuando sem integração do Calendar...")
    
    # Chain RAG padrão sem tools
    rag_chain = get_rag_chain(contextualize_prompt_text, system_prompt_text)
    return RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key='input',
        history_messages_key='chat_history',
        output_messages_key='answer',
    )


def get_agent_with_tools(contextualize_prompt_text, system_prompt_text, tools):
    """Cria um agente com ferramentas (tools) e RAG."""
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    # Inicializa o LLM (desabilitando streaming para evitar erro 400)
    llm = ChatOpenAI(
        model=OPENAI_MODEL_NAME,
        temperature=OPENAI_MODEL_TEMPERATURE,
        streaming=False,  # Desabilita streaming para evitar erro de organização
    )
    
    # Recuperador de vetores
    retriever = get_vectorstore().as_retriever()
    
    # Cria uma tool para buscar no RAG
    from langchain_core.tools import tool
    
    @tool
    def search_knowledge_base(query: str) -> str:
        """
        Busca informações na base de conhecimento da escola.
        Use esta ferramenta quando precisar de informações sobre a escola, 
        seus programas, processos, infraestrutura, etc.
        
        Args:
            query: A pergunta ou termo de busca
        
        Returns:
            Informações relevantes da base de conhecimento
        """
        docs = retriever.get_relevant_documents(query)
        if not docs:
            return "Nenhuma informação encontrada na base de conhecimento."
        return "\n\n".join([doc.page_content for doc in docs[:3]])
    
    # Adiciona a tool de RAG às outras tools
    all_tools = tools + [search_knowledge_base]
    
    # Cria o prompt do agente
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt_text + "\n\nVocê tem acesso a ferramentas para buscar informações e gerenciar o calendário. Use-as quando necessário."),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Cria o agente
    agent = create_tool_calling_agent(llm, all_tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        return_intermediate_steps=False,  # Evita streaming interno
    )
    
    # Retorna com histórico de mensagens
    return RunnableWithMessageHistory(
        runnable=agent_executor,
        get_session_history=get_session_history,
        input_messages_key='input',
        history_messages_key='chat_history',
        output_messages_key='output',
    )
