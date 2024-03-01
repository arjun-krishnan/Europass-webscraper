# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:43:47 2024

@author: arjun
"""

import os
import google.generativeai as genai

genai.configure(api_key = os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-pro')

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

def profile_match(job, profile):
    messages = [{'role':'user',
                 'parts':[f"You are given a job description delimited by ```. \
    Job description: ```{job}```."]},
                {'role':'model',
                 'parts':["ok."]}]
                     
    m_copies = [list(messages) for _ in range(3)]

    m_copies[0].append({'role':'user',
                     'parts':[f"Is it a {profile['level']} job? Post-doc position can be considered entry-level. Answer in 1 word, yes or no."]})
    res1 = get_response(model,m_copies[0])

    m_copies[1].append({'role':'user',
                     'parts':[f"User's skills:{profile['skills']}. Does the user have more than half the skills relevant to the job? Answer in 1 word, yes or no."]})
    res2 = get_response(model,m_copies[1])

    #m_copies[2].append({'role':'user',
    #                 'parts':[f"The user has {profile['languages']} language skills. Does that fullfil the language requirement for the job? Answer in 1 word, yes or no."]})
    #res3 = get_response(model,m_copies[2])
    
    results = [res1.lower(),res2.lower()] #,res3.lower()]
    #print(results)
    verdict = all('yes' in s for s in results) 
    
    return(results, verdict)