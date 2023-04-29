from flask import Flask, request, abort
import os

app = Flask(__name__)

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
  
  return "", 200


@app.route("/fileupload", methods=["POST"])
def file_upload():
    if 'document' not in request.files:
        return {
            "errorMsg": "Expected a file with key 'document' to be uploaded."
        }, 500
    
    file = request.files['document']

    if not os.path.exists('./docs'):
        os.mkdir('./docs')

    file.save(f"./docs/{file.filename}")

    return file.filename, 200