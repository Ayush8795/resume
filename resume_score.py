#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np




import re
import math



import json








def get_clg_category(json_file):
    clg_lis= json_file['educational_details']['college_details']
    clg= clg_lis[0]
    df1= pd.read_excel('Category A CollegeList.xlsx')
    df2= pd.read_excel('Category B CollegeList.xlsx')
    lisA= df1['CollegeName'].values
    lisB= df2['CollegeName'].values
    cat='C'
    
    
    if clg in lisA:
        cat='A'
    if clg in lisB:
        cat= 'B'
    return cat
    



def get_edu_score(json_file):
    clg_cat= get_clg_category(json_file)
    cat_score=0
    if clg_cat=='A':
        cat_score=10
    elif clg_cat=='B':
        cat_score=8
    else:
        cat_score= 6
    
    degrees= json_file['educational_details']['degrees']
    deg_score=0
    for deg in degrees:
        if re.search('master',deg,re.IGNORECASE) or re.search('M\.',deg):
            deg_score= max(deg_score,10)
        elif re.search('bachelor',deg,re.IGNORECASE) or re.search('B\.',deg):
            deg_score= max(deg_score,8)
        else:
            deg_score= max(deg_score,6)
    cgpa= float(json_file['educational_details']['cgpa'])
    if cgpa>10:
        cgpa/=10
    
    score= cat_score+deg_score+cgpa
    return score
    
    
    



def get_experience_score(json_file):
    exp= json_file['work_experience']['experience']
    l= len(exp)
    s=0
    if l>2:
        s=10
    elif l==2:
        s=8
    elif l==1:
        s=6
    return s
    




def get_project_score(json_file):
    proj= json_file['projects']['project_names']
    l= len(proj)
    if l>=3:
        return 10
    elif l==2:
        return 8
    elif l==1:
        return 6
    return 0



def get_achievement_score(json_file):
    ach= json_file['achievements']
    l= len(ach)
    if l>=4:
        return 20
    else:
        return l*5
    



def get_por_score(json_file):
    por= json_file['responsibilities']['positions_of_responsibility']
    l= len(por)
    if l>=4:
        return 10
    elif l==3:
        return 8
    elif l==2:
        return 6
    elif l==1:
        return 5
    return 0


def get_training_score(json_file):
    cf= json_file['trainings and certifications']
    l= len(cf)
    if l>=2:
        return 5
    elif l==1:
        return 3
    return 0



def get_skill_score(json_file):
    req=['Business Development','Sales','Marketing','Customer Success','English','MS Excel','Digital Marketing','Email Marketing','MS Office','Social Media Marketing','Google Analytics Tools','SEO','Facebook Marketing','Instagram Marketing','Communication','CRM']
    skl= json_file['skills']
    l= len(req)
    c=0
    for sl in skl:
        for rs in req:
            if sl.lower()==rs.lower():
                c+=1
                break
    score= (c/l)*15
    return score
    



def ResumeScore(json_path):
    json_file= json.load(open(json_path))
    with open('Sample_json.json','w') as file:
        json.dump(json_file,file)
    score= get_edu_score(json_file)+get_experience_score(json_file)+get_project_score(json_file)+get_achievement_score(json_file)+get_por_score(json_file)+get_training_score(json_file)+get_skill_score(json_file) 
    return score





# print(ResumeScore('resume_data.json'))
