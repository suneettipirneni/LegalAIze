import os
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import OpenAI
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.chains.question_answering import load_qa_chain
import os
import redis

# check windows or not
if os.name == 'nt':
    from dotenv import load
    load()
else:
    from dotenv import load_dotenv
    load_dotenv()

use_default_model = True
model_name = 'text-curie-001'
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# connect to redis
redis_url = os.getenv('REDIS_URL')
redis_client = redis.Redis.from_url(redis_url)

if use_default_model:
    llm = OpenAI(callback_manager=callback_manager)
else:
    llm = OpenAI(callback_manager=callback_manager, model_name='text-curie-001')

summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

def get_doc_and_summary(file_name: str):
    if redis_client.exists(file_name):
        data = redis_client.hgetall(file_name)
        data = {k.decode(): v.decode('utf-8', 'ignore') for k, v in data.items()}
        return data
    
    file_path = os.path.join(os.getcwd(), 'server','docs', file_name).replace('\\', '/')
    doc_loader = UnstructuredWordDocumentLoader(file_path)
    document = doc_loader.load()
    summary = summarize_document_chain.run(document[0].page_content)
    data = {
        'document': document[0].page_content,
        'summary': summary
    }
    redis_client.hmset(file_name, data)
    return data


def load_document(file_name: str):
    # check if file exists in redis
    if redis_client.exists(file_name):
        return redis_client.get(file_name).decode('utf-8', 'ignore')
    file_path = os.path.join(os.getcwd(), 'server','docs', file_name).replace('\\', '/')
    doc_loader = UnstructuredWordDocumentLoader(file_path)
    document = doc_loader.load()
    redis_client.set(file_name, document[0].page_content)
    return document[0].page_content

def summarize_document(file_name: str):
    if redis_client.exists(file_name):
        data = redis_client.hgetall(file_name)
        return data['summary'].decode('utf-8', 'ignore')
    data = get_doc_and_summary(file_name)
    return data['summary']

def answer_question(question: str, file_name: str):
    doc = get_doc_and_summary(file_name)
    return qa_document_chain.run(question = question, input_document = doc['document'])