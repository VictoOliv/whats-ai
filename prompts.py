from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_contextualize_prompt(contextualize_prompt_text):
    """Prompt de contextualização (usado pelo history-aware retriever)"""
    return ChatPromptTemplate.from_messages([
        ("system", contextualize_prompt_text),
        MessagesPlaceholder('chat_history'),
        ("human", "{input}")  # histórico do usuário passado como 'input'
    ])

def get_qa_prompt(system_prompt_text):
    """Prompt de QA (usado pelo RAG chain)"""
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt_text),
        MessagesPlaceholder('chat_history'),
        ("human", "{input}\nContext: {context}")
    ])
