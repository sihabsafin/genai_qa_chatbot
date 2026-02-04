from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

# Load API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional AI Q&A assistant. Answer clearly and concisely."),
    ("human", "{question}")
])

# LLM
llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0.3
)

# Chain
chain = prompt | llm

def get_answer(question: str) -> str:
    response = chain.invoke({"question": question})
    return response.content
