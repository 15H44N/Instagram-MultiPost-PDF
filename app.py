import os
import io
import json
from createfile import *
from flask import Flask, request, abort, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def landing():
    return "Hello World"
    
@app.route("/instapost", methods=["GET"])
def get_pdf_post():
    scode = request.args.get('scode')
    fname = request.args.get('fname')
    
    with open('old_data.json') as json_file: 
        old_data = json.load(json_file)
    
    old_fname = old_data['old_fname']
    try:
        os.remove("./"+old_fname)
    except:
        print("File not Found!")
    
    v_dict = {
        'scode':scode,
        'fname':fname
    }
    #scode = 'CEEOLKNnNUU'
    file_out = createPDFandRemove(v_dict)
    
    old_data['old_fname'] = file_out
    with open('old_data.json','w') as json_file: 
        json.dump(old_data,json_file) 
    
    return send_from_directory(directory="./", 
                               filename=file_out, 
                               as_attachment=True)
    

if __name__ == "__main__":
    app.run(debug=True)
    #app.run()