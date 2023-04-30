import os
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import OpenAI
from langchain.chains import AnalyzeDocumentChain, LLMRequestsChain, LLMChain
from langchain.document_loaders import UnstructuredWordDocumentLoader
import os
import redis
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from langchain.prompts import PromptTemplate
import spacy

# check windows or not
if os.name == 'nt':
    from dotenv import load
    load()
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
else:
    from dotenv import load_dotenv
    load_dotenv()


template_google = """Extract the answer to the question '{query}' using the document text and the google search results
like a lawyer would and answer like a laywer would.
Use the format
Extracted:<answer or "cannot say from the given information">
document text: {doc_data},
google search results: {requests_result},
Extracted:"""

template = """You are a lawyer and your answers should be professional and accurate.
You are given a document and a question. You should answer the question using the document.
Make sure to provide any important context in your answer and give the reasoning and justification for your answer.
The question is: '{query}' and 
the document is: '{doc_data}'
Answer:"""

PROMPT_GOOGLE = PromptTemplate(
    input_variables=["query", "doc_data","requests_result"],
    template=template_google,
)

PROMPT = PromptTemplate(
    template=template, input_variables=["doc_data", "query"]
)

use_default_model = False
model_name = 'gpt-3.5-turbo'
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# connect to redis
redis_url = os.getenv('REDIS_URL')
redis_client = redis.Redis.from_url(redis_url)
# Load the English language model
nlp = spacy.load('en_core_web_sm')

if use_default_model:
    llm = OpenAI(callback_manager=callback_manager, temperature=0.3)
else:
    llm = OpenAI(callback_manager=callback_manager, model_name=model_name, temperature=0.3)

summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

google_chain = LLMRequestsChain(llm_chain = LLMChain(llm=llm, prompt=PROMPT_GOOGLE))
normal_chain = LLMChain(llm=llm, prompt=PROMPT)
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

def answer_question(question: str, file_name: str, general: bool = False):
    doc = get_doc_and_summary(file_name)
    if general:
        sentence = question

        # Parse the sentence
        parsed = nlp(sentence)

        # Extract keywords
        keywords = [token.text for token in parsed if not token.is_stop and token.pos_ in ['NOUN', 'PROPN']]
        inputs = {
            "query": question,
            "doc_data": doc['document'],
            "url": "https://www.google.com/search?q=" + '+'.join(keywords)
        }
        return google_chain.run(inputs)
    
    input = {
        "query": question,
        "doc_data": doc['document']
    }
    return normal_chain.run(input)