# resume_data_getter

Run:

pip install -r requirements.txt


File: resume_data.py:-
Has several functions for fetching of data like name, experience, skills, etc.

It has a function json_maker(file_name):
arguments: file_name- input the file path
output: json file path of the parsed resume in the same folder where the file is installed

code snippet:

import resume_data

path= resume_data.json_maker(resume_path)


the json path will be of format: Name_of_candidate_resume_data.json file will be created in the same folder where the file is installed

After correction from user the updated json will be created.

pass updated json to resume_score.py 

Code snippet:

from resume_score import ResumeScore

score= ResumeScore(json_file_path)

the score will be returned



