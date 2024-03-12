
import os
import google.generativeai as genai
from openai import OpenAI

genai.configure(api_key = os.environ["GEMINI_API_KEY"])
model_gemini = genai.GenerativeModel('gemini-pro')

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_response_gpt(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1.0
    )
    return response.choices[0].message.content

def get_response_gemini(message, model=model_gemini):
    response = model.generate_content(message)
    return(response.text)


def read_profile(filename):
    profile = {}
    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            key, value = line.split(' : ')

            profile[key] = eval(value)

    return (profile)


def profile_match(job, profile, agent):

    if agent == 'gemini':
        messages = [{'role': 'user',
                     'parts': [f"You are given a job description delimited by ```. \
        Job description: ```{job}```."]},
                    {'role': 'model',
                     'parts': ["ok."]}]

        m_copies = [list(messages) for _ in range(3)]

        m_copies[0].append({'role': 'user',
                            'parts': [
                                f"Is it a {profile['level']} job? Post-doc position can be considered entry-level. Answer in 1 word, yes or no."]})
        res1 = get_response_gemini(m_copies[0])

        m_copies[1].append({'role': 'user',
                            'parts': [
                                f"User's skills:{profile['skills']}. Does the user have more than half the skills relevant to the job? Answer in 1 word, yes or no."]})
        res2 = get_response_gemini(m_copies[1])

        # m_copies[2].append({'role':'user',
        #                 'parts':[f"The user has {profile['languages']} language skills. Does that fullfil the language requirement for the job? Answer in 1 word, yes or no."]})
        # res3 = get_response(model,m_copies[2])

    elif agent == 'openai':
        messages = [{'role': 'system',
                     'content': f"You are given a job description delimited by ```. \
            Job description: ```{job}```. Your job is to answer the following questions with 'Yes' or 'No'."},
                    ]

        m_copies = [list(messages) for _ in range(3)]

        m_copies[0].append({'role': 'user',
                            'content':
                                f"Is it a {profile['level']} job? Post-doc position can be considered entry-level."})
        res1 = get_response_gpt(m_copies[0])

        m_copies[1].append({'role': 'user',
                            'content':
                                f"User's skills:{profile['skills']}. Does the user have more than half the skills relevant to the job?"})
        res2 = get_response_gpt(m_copies[1])

        # m_copies[2].append({'role':'user',
        #                 'parts':[f"The user has {profile['languages']} language skills. Does that fullfil the language requirement for the job? Answer in 1 word, yes or no."]})
        # res3 = get_response(model,m_copies[2])

    results = [res1.lower(), res2.lower()]  # ,res3.lower()]
    # print(results)
    verdict = all('yes' in s for s in results)

    return (results, verdict)