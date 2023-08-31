import json 
import time
import path
import resume_data as rd
import resume_score as rs
import boto3
from flask import Flask ,render_template, request,jsonify
from flask_cors import CORS

import time
import os
app= Flask(__name__)

CORS(app)


@app.route('/resume',methods=['POST'])
def predict():
    
    getdata=request.get_json()
    file= getdata['file_name']  
    s3=boto3.client('s3',aws_access_key_id='',aws_secret_access_key='')
    s3.download_file('resume-store-hiremeclub',file,file)

    
    result=rd.json_maker(file)
    score= rs.ResumeScore("resume_data.json")
    print(score)
    return jsonify(score)

@app.route('/score',methods=['POST'])
def pred_score():

    data= request.get_json()
    file= data['file_name']
    score= rs.ResumeScore(file)
    print(score)
    return jsonify(score)




if __name__ =='__main__':
    app.run()