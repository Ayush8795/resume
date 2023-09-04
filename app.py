import json 
import time
import path
import resume_data as rd
import resume_score as rs
import boto3
from flask import Flask ,render_template, request,jsonify
from flask_cors import CORS
from dotenv import load_dotenv

import time
import os
app= Flask(__name__)

CORS(app)

load_dotenv()


@app.route('/resume',methods=['POST'])
def predict():
    key= os.getenv('API_KEY_ID')
    access_key= os.getenv('API_SECRECT_KEY')
    getdata=request.get_json()
    file= getdata['file_name']  
    s3=boto3.client('s3',aws_access_key_id=key,aws_secret_access_key=access_key)
    s3.download_file('resume-store-hiremeclub',file,file)
    result=rd.json_maker(file)
    return jsonify(result)

@app.route('/score',methods=['POST'])
def pred_score():

    data= request.get_json()
    file= data['file_name']
    score= rs.ResumeScore(file)
    return jsonify(score)




if __name__ =='__main__':
    app.run()