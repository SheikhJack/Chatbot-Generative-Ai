from flask import Flask, render_template, request, jsonify,request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


embeddings = download_hugging_face_embeddings()



#Embed each chunk and upsert the embeddings into Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name="medibot",
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")
prompt = ChatPromptTemplate.from_messages(
     [
          ("system", system_prompt),
          ("human", "{input}")
     ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)




@app.route("/")
def index():
    return render_template('index.html')



@app.route("/ask", methods=[ 'GET','POST'])
def ask():
    msg = request.form['msg']
    print("User input:", msg)
    
    response = rag_chain.invoke({"input": msg})
    print("Response:", response["answer"])
    
    return str(response["answer"])

    



if __name__ == '__main__':
     app.run(host="0.0.0.0")
