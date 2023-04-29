from flask import Flask, request, abort, Response
from flask_cors import CORS, cross_origin
import os

from ml import summarize_document, answer_question, get_doc_and_summary

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

    result = answer_question(request.args['prompt'], request.args['filename']) 
    
    return {
        "content": result,
    }

@app.route("/summarize", methods=['GET'])
def summarize():
  if "filename" not in request.args:
        return {
            "errorMsg": "Expected a 'filename' query parameter, but it was not found"
        }, 500
  
  filename = request.args['filename']

  result = summarize_document(filename)

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
    get_doc_and_summary(file.filename)

    return file.filename, 200

@app.route("/documents", methods=["GET"])
def get_documents():
     if not os.path.exists('./server/docs'):
        return [], 200
     
     files = []

     for file in os.listdir("./server/docs"):
         summary = summarize_document(file)
         files.append({ "name": file, "summary": summary })

     return files
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')