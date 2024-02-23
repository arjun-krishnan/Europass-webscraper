# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:43:47 2024

@author: arjun
"""

import pathlib
import textwrap
from time import time
import google.generativeai as genai

def get_response(model,message):
    response = model.generate_content(message)
    return(response.text)

def chat_response(model,message):
    response = model.send_message(message)
    return(response.text)

def read_profile(filename):
    profile = {}
    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            key, value = line.split(' : ')

            profile[key] = eval(value)
                
    return(profile)


#%%    
genai.configure(api_key="AIzaSyBnb90WJgaLqxsww2uzL0DJCpsKR-oyLbA")

model = genai.GenerativeModel('gemini-pro')

# with open('../profile.txt', 'r') as file:
#     # Read all lines from the file and join them into a single string
#     profile = ''.join(file.readlines())

profile = read_profile("profile.txt")
    
job_d = jobs[16]["Description"]


#%%
t0 = time()

messages = [{'role':'user',
             'parts':[f"You are given a job description delimited by ```. \
Job description: ```{job_d}```."]},
            {'role':'model',
             'parts':["ok."]}] # ,


m_copies = [list(messages) for _ in range(3)]

m_copies[0].append({'role':'user',
                 'parts':[f"Is it a {profile['level']} job? Post-doc position can be considered entry-level. Answer in 1 word, yes or no."]})
res1 = get_response(model,m_copies[0])

m_copies[1].append({'role':'user',
                 'parts':[f"User's skills:{profile['skills']}. Does the user have more than half the skills relevant to the job? Answer in 1 word, yes or no."]})
res2 = get_response(model,m_copies[1])

m_copies[2].append({'role':'user',
                 'parts':[f"The user has {profile['languages']} language skills. Does that fullfil the language requirement for the job? Answer in 1 word, yes or no."]})
res3 = get_response(model,m_copies[2])

print(time()-t0)

#%%                 
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

t0 = time()

message = f"You are given the profile of the user delimited by ### and a job description delimited by ```. \
Profile: ###{profile}### \n \
Job description: ```{job_d}```. Respond in 1 word. \n"
 
chat_response(chat,message)

res1 = chat_response(chat,"Which is the preferred level of job by the user? Does it match with the job description? Answer in 1 word, yes or no.")
res2 = chat_response(chat,"Does the user have more than half the skills relevant to the job? Answer in 1 word, yes or no.")
res3 = chat_response(chat,"Does the job require proficieny in any language? is the user have the required proficieny in that language? Answer in 1 word, yes or no.")

t = time() - t0
print(t)