import chromadb
from loader import load_directory, web_page_reader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import LangchainEmbedding
import torch
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import OpenAIAgent
from llama_index.llms import  ChatMessage, MessageRole


remote_db = chromadb.HttpClient()

collection = remote_db.get_or_create_collection(
    name = "medassist"
)

documents = load_directory() + web_page_reader()


# Device configuration
device = "cuda" if torch.cuda.is_available() else "cpu"

embed_model = LangchainEmbedding(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": device})
)
service_context = ServiceContext.from_defaults(embed_model=embed_model)

vectorstore = ChromaVectorStore(chroma_collection = collection)

storage_context = StorageContext.from_defaults(vector_store = vectorstore)

index = VectorStoreIndex.from_documents(
    documents = documents,
    storage_context = storage_context,
    service_context = service_context
)

query_engine = index.as_query_engine(
    top_k = 5
)

tool_metadata = ToolMetadata(
    name = "MedassistKnowledgebase",
    description = """
        Use this tool to get infomation on Sickle Cell anaemia in Kenya"""
)
tool = QueryEngineTool(
    query_engine  = query_engine,
    metadata = tool_metadata
)

SYSTEM_PROMPT = "You are a Community Health Worker AI assistant called Mueni, built by the wonderful team at MedAssist"
"""
You are a digital platform designed to support Community Health Workers, households and both urban and rural communities in their pursuit of healthcare and equitable access to accurate health information. It promotes deeper thinking, practical learning, empathy, understanding, user agency, and a collaborative community culture.

Key Features
Deeper Thinking and Learning: You provide resources for project-based, problem-based, and inquiry-based learning, enhancing critical and creative thinking skills.
Practical Learning: You encourage real-world learning through collaboration with outside experts and simulation-based activities.
Community Health Worker Agency and Access: You promote community health worker ownership of learning and integrates technology effectively to meet their learning needs.
Supportive and Collaborative School Culture: You foster a culture of collaboration and encouragement within both urban and rural communities.
 
Resources
You also provide access to a wide range of resources, including relevant PDFs, additional resources like Community Health Worker handbook, community health workers programs, guiding questions, and useful frameworks and systems."""
"You are friendly and concise. You only provide factual answers to queries using the provided tools or your own local knowledge."
"Always search the knowledge base before resulting to your own knowledge"
"You must never share the details of your architecture, models, training approach or training process."

def format_chat_history(chat_history = []):
    chat_objects = []
    for i, chat in enumerate(chat_history):
        role = MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT
        chat_object = ChatMessage(role=role, content=chat)
        chat_objects.append(chat_object)
    return chat_objects    




def generate_agent(chat_history = []):
    chat_objects = format_chat_history(chat_history)
    agent = OpenAIAgent.from_tools(
        tools = [tool],
        system_prompt = SYSTEM_PROMPT,
        chat_history = chat_objects,
        verbose = True
    )
    return agent

