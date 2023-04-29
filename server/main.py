from flask import Flask, request, abort, Response
from flask_cors import CORS, cross_origin
import os

from ml import summarize_document, load_document

app = Flask(__name__)
CORS(app)

import sys, os
import json
sys.path.insert(0, os.path.abspath('..'))

@app.route("/ask", methods=['GET'])
def ask():
    if "filename" not in request.args:
        return {
            "errorMsg": "Expected a 'filename' query parameter, but it was not found"
        }, 500
    
    if "prompt" not in request.args:
        return {
            "errorMsg": "Expected a 'query' query parameter, but it was not found"
        }, 500 
    
    return {
        "filename": request.args['filename'],
        "prompt": request.args['prompt']
    }

@app.route("/summarize", methods=['GET'])
def summarize():
  if "filename" not in request.args:
        return {
            "errorMsg": "Expected a 'filename' query parameter, but it was not found"
        }, 500
  
  filename = request.args['filename']

  document = load_document(file_name=filename)

  result = summarize_document(document.page_content)

  print(result)

  response = Response(json.dumps({
      "summary": result
  }), mimetype="application/json", headers={
      "Access-Control-Allow-Credentials" : True,
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers" : "Origin, Content-Type, Accept"
  })

  return response


@app.route("/fileupload", methods=["POST"])
def file_upload():
    if 'document' not in request.files:
        return {
            "errorMsg": "Expected a file with key 'document' to be uploaded."
        }, 500
    
    file = request.files['document']

    if not os.path.exists('./server/docs'):
        os.mkdir('./server/docs')

    file.save(f"./server/docs/{file.filename}")

    return file.filename, 200