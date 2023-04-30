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
import PyPDF2
import pytesseract
from pdf2image import convert_from_path

# check windows or not
if os.name == 'nt':
    from dotenv import load
    load()
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
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


def get_text_from_pdf(file_path: str):
    text = ""
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    pdf_file.close()

    # remove all whitespaces and newlines
    text = text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')

    if text == "":
        # extract images from pdf
        images = convert_from_path(file_path)
        for image in images:
            # extract text from image
            text += pytesseract.image_to_string(image)
    return text

def get_doc_and_summary(file_name: str):
    if redis_client.exists(file_name):
        data = redis_client.hgetall(file_name)
        data = {k.decode('utf-8', 'ignore'): v.decode('utf-8', 'ignore') for k, v in data.items()}
        return data
    
    file_path = os.path.join(os.getcwd(), 'server','docs', file_name).replace('\\', '/')

    if file_name.endswith('.docx') or file_name.endswith('.doc'):
        doc_loader = UnstructuredWordDocumentLoader(file_path)
        doc_loader = UnstructuredWordDocumentLoader(file_path)
        document = doc_loader.load()
        text = document[0].page_content
    elif file_name.endswith('.pdf'):
        text = get_text_from_pdf(file_path)
    elif file_name.endswith('.txt'):
        with open(file_path, 'r') as f:
            text = f.read()
    elif file_name.endswith('.jpg') or file_name.endswith('.png'):
        text = pytesseract.image_to_string(file_path)
    else:
        raise Exception('File format not supported')
    
    # remove whitespaces, new lines and characters that are not supported by OpenAI
    text = text.replace('\n', ' ').replace('\r', '').replace('  ', ' ').replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-').replace('…', '...').replace('•', '*').replace('·', '*').replace('´', "'").replace('`', "'").replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-').replace('…', '...').replace('•', '*').replace('·', '*').replace('´', "'").replace('`', "'").replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-').replace('…', '...').replace('•', '*').replace('·', '*').replace('´', "'").replace('`', "'").replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-').replace('…', '...').replace('•', '*').replace('·', '*').replace('´', "'").replace('`', "'").replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-').replace('…', '...').replace('•', '*').replace('·', '*').replace('´', "'").replace('`', "'")

    summary = summarize_document_chain.run(text)
    data = {
        'document': text,
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
        data = {k.decode('utf-8', 'ignore'): v.decode('utf-8', 'ignore') for k, v in data.items()}
        return data['summary']
    data = get_doc_and_summary(file_name)
    return data['summary']

def answer_question(question: str, file_name: str):
    doc = get_doc_and_summary(file_name)
    return qa_document_chain.run(question = question, input_document = doc['document'])