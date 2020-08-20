import os
import io
import json
from createfile import *
from flask import Flask, render_template,request, abort, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("index.html")
    
@app.route("/instapost", methods=["GET"])
def get_pdf_post():
    url = request.args.get('PostURL')
    #scode = request.args.get('Post SCode')
    fname = request.args.get('FileName')
    
    after_p = url[url.find("/p/")+len("/p/"):]
    scode = after_p.split("/")[0]
    
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