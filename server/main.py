from flask import Flask, request, abort
import os

from ml import summarize_document, answer_question

app = Flask(__name__)

import sys, os
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

  result = summarize_document(filename)

  print(result)
  
  return result, 200


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

if __name__ == "__main__":
    app.run(host='0.0.0.0')