
import pandas as pd
import numpy as np
from pypdf import PdfReader




import json




import pytesseract as tess




from pdf2image import convert_from_path as cfp




tess.pytesseract.tesseract_cmd= r'C:\Program Files\Tesseract-OCR\tesseract.exe'




from pyresparser import ResumeParser




import nltk
import re
import os






resume_specific_words= ['course','courses','linkedin','github','mobile','social','email','professional summary','skills','skill','languages','language','hobbies','hobby','employment history','research','experience','education','research and collaborations','skill summary','skills summary','project','projects','honors','honor','award','awards','honors and awards','honor and award','certificate','certificates','achievement','achievements','extracurricular activity','extracurricular activities','positions of responsibility','position of responsibility','positions of responsibilities','trainings','training','additional details','contact','cover letter','cover letter and availability','availability','work experience']




def name_extract(text,data):
    tex= text.lower()
    parser_name= str(data['name'])
    sentences= nltk.sent_tokenize(text)[0].split('\n')
    nam=""
    c=0
    for sen in sentences:
        sen= sen.lower()
        if sen== ' ' or sen== '':
            continue
        
        if sen in resume_specific_words:
            break
        
        nam+= sen+" "
        if len(nam.split(' '))>=3:
            break
    
    par= parser_name.lower()
    par= str(par)
    nam= str(nam)
    if nam == par:
        return parser_name, None
    if re.search(nam,par) is not None:
        x= re.search(nam,par)
        ret= parser_name[x.start():x.end()]
        return ret, None
    
    if parser_name is None:
        nam= nam[0].upper()+nam[1:]
        return nam
    x=""
    for wd in nam.split(' '):
        x= x+wd.capitalize()+' '
    
    return parser_name,x 
    




def get_edu(text):
    tex=[]
    for tx in text.split('\n'):
        if tx != '':
            tex.append(tx)
    sentences= tex
    deg=[]
    clg=[]
    exp1= r'bachelor|master|diploma|senior secondary|high school|class X|class XII|secondary|intermediate'
    sped= r'MBA|BBA|B\.Tech|B\.E\.|B\.A\.|M\.A\.|B\.Com|X|XII'
    exp2= r'college|university|institute|school|vidyalaya'
    
    for sen in sentences:
        if re.search(exp1,sen,re.IGNORECASE) or re.search(sped,sen):
            if re.search(exp1,sen,re.IGNORECASE) is not None:
                f=1
                for rwd in resume_specific_words:
                    if re.search(rwd,sen,re.IGNORECASE):
                        f=0
                        break
                if f!=0:
                    deg.append(sen)
                
            elif re.search(sped,sen) is not None:
                f=1
                for rwd in resume_specific_words:
                    if re.search(rwd,sen,re.IGNORECASE):
                        f=0
                        break
                if f!=0:
                    deg.append(sen)
        if re.search(exp2,sen,re.IGNORECASE):
            clg.append(sen)
    
    return deg,clg






def get_experience(text,data):
    par_exp= data['experience']
    ob= re.search('experience|job|jobs',text,re.IGNORECASE)
    if ob is None and par_exp is None:
        return [],[]
    
    exp=[]
    desc=[]
    if par_exp is not None and ob is None:
        exp= data['college_name']
        desc= data['experience']
        return exp,desc
    tex=[]
    texx= text[ob.end():]
    for tx in texx.split('\n'):
        if tx != '':
            tex.append(tx)
    sentences= tex
    flag= 1
    c=0
    for sen in sentences:
        for wd in resume_specific_words:
            if re.search(wd,sen,re.IGNORECASE) and re.search(wd,'experience intern internship job',re.IGNORECASE) is None:
                flag=0
                break
        if flag==0:
            break
        if c==0:
            exp.append(sen)
        elif c==1 or c==2:
            desc.append(sen)
        
        c+=1
        c= c%3
    
    return exp,desc





def get_projects(text):
    ob= re.search('projects',text,re.IGNORECASE)
    if ob is None:
        return [],[]
    
    tex=[]
    texx= text[ob.end():]
    for tx in texx.split('\n'):
        if tx != '':
            tex.append(tx)
    sentences= tex
    flag= 1
    c=0
    proj=[]
    desc=[]
    for sen in sentences:
        if flag==0:
            break
        if c==0:
            proj.append(sen)
        elif c==1 or c==2:
            desc.append(sen)
        
        c+=1
        c= c%3
        for wd in resume_specific_words:
            if re.search(wd,sen,re.IGNORECASE) and re.search(wd,'project',re.IGNORECASE) is None:
                flag=0
                break
        
    
    return proj,desc
    





def get_POR(text):
    reg= 'positions of responsibility|position of responsibility|positions of responsibilities'
    ob= re.search(reg,text,re.IGNORECASE)
    if ob is None:
        return [],[]
    pos=[]
    desc=[]
    
    tex=[]
    texx= text[ob.end():]
    for tx in texx.split('\n'):
        if tx != '':
            tex.append(tx)
    sentences= tex
    flag= 1
    c=0
    proj=[]
    desc=[]
    for sen in sentences:
        if c==0:
            pos.append(sen)
        elif c==1 or c==2:
            desc.append(sen)
        
        c+=1
        c= c%3
        for wd in resume_specific_words:
            if re.search(wd,sen,re.IGNORECASE):
                flag=0
                break
        if flag==0:
            break
    
    return pos,desc




def get_skills(data):
    return data['skills']




def get_achieve(text):
    reg= 'achievement|achievements|accomplishment|accomplishments'
    ob= re.search(reg,text,re.IGNORECASE)
    if ob is None:
        return []
    ach=[]
    tex=[]
    texx= text[ob.end()+1:]
    for tx in texx.split('\n'):
        if tx != '':
            tex.append(tx)
    sentences= tex
    flag=1
    for sen in sentences:
        ach.append(sen)
        for wd in resume_specific_words:
            if re.search(wd,sen,re.IGNORECASE):
                flag=0
                break
        if flag==0:
            break
        
        
    
    return ach
    




def get_trainings(text):
    reg1= 'certification|certifications|certificates'
    ob1= re.search(reg1,text,re.IGNORECASE)
    reg2= 'training|trainings'
    ob2= re.search(reg2,text,re.IGNORECASE)
    cer=[]
    if ob1 is None and ob2 is None:
        return []
    if ob1 is not None:
        tex=[]
        texx= text[ob1.end()+1:]
        for tx in texx.split('\n'):
            if tx != '':
                tex.append(tx)
        sentences= tex
        flag=1
        for sen in sentences:
            cer.append(sen)
            for wd in resume_specific_words:
                if re.search(wd,sen,re.IGNORECASE):
                    flag=0
                    break
            if flag==0:
                break
            
    
    
    if ob2 is None:
        return cer+[]
    trn=[]
    tex2=[]
    texx2= text[ob2.end()+1:]
    for tx in texx2.split('\n'):
        if tx != '':
            tex2.append(tx)
    sentences2= tex2
    flag=1
    for sen in sentences2:
        trn.append(sen)
        for wd in resume_specific_words:
            if re.search(wd,sen,re.IGNORECASE):
                flag=0
                break
        if flag==0:
            break
        
        
    
    return cer+trn




def dict_maker(file_name):
    images= cfp(file_name,poppler_path=r'C:\Program Files\poppler-23.08.0\Library\bin')

    length= len(images)
    text=''
    for img in images:
        text= text+tess.image_to_string(img)+'\n'
    
    
    data= ResumeParser(file_name).get_extracted_data()
    pname,cname= name_extract(text,data)
    name=''
    if pname.lower()==cname.lower():
        name= pname
    else:
        name= cname
    name= name.strip()
    deg,clg= get_edu(text)
    experience,exp_desc= get_experience(text,data)
    skills= get_skills(data)
    pos_of_resp,pos_desc= get_POR(text)
    achievements= get_achieve(text)
    training_and_certif= get_trainings(text)
    projects,proj_desc= get_projects(text)
    
    # print(name)
    summary_dict= {
        'name': name,
        'educational_details': {'degrees': deg, 'college_details':clg,'cgpa':0},
        'work_experience': {'experience':experience, 'description':exp_desc},
        'skills': skills,
        'responsibilities': {'positions_of_responsibility':pos_of_resp,'description':pos_desc},
        'achievements': achievements,
        'trainings and certifications': training_and_certif,
        'projects': {'project_names':projects, 'description':proj_desc}
        
        
    }
    return summary_dict
    




def json_maker(file_name):
    res_dict= dict_maker(file_name)
    path= 'resume_data.json'
    pth= r'D:\hiremeclub\resume_data_getter-main'
    path= os.path.join(pth,path)
    with open(path,'w') as file:
        json.dump(res_dict,file)
    return path




# print(json_maker(r'a.pdf'))





