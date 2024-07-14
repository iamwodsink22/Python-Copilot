from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.cohere import CohereEmbeddings
from dotenv import load_dotenv
from langchain.llms.cohere import Cohere
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain.chains import create_retrieval_chain
import os
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from src.prompts import qa_prompt,contextualize_q_prompt
from langchain.chains.combine_documents import create_stuff_documents_chain
class BaseAgent:
   
    def __init__(self):
        load_dotenv()
        self.chat_mssg=[]
        self.embeddings=CohereEmbeddings(cohere_api_key=st.secrets["COHERE_API_KEY"],user_agent="langchain")
        self.llm=Cohere(cohere_api_key=st.secrets["COHERE_API_KEY"])
        retriever=self.init_db().as_retriever()
        self.history_aware_retriever = create_history_aware_retriever(
    self.llm, retriever, contextualize_q_prompt)
        self.create_doc_chain=create_stuff_documents_chain(self.llm,qa_prompt)
        self.rag_chain=create_retrieval_chain(self.history_aware_retriever,self.create_doc_chain)
        

    
    def init_db(self):
        
        pc=Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
        vector_store=PineconeVectorStore(index_name='python',embedding=self.embeddings)
        return vector_store
        
    def chat(self,query):
        
        response=self.rag_chain.invoke({'input':query,'chat_history':self.chat_mssg})
        self.chat_mssg.extend([HumanMessage(content=query),response['answer']])
        return response['answer']
    
