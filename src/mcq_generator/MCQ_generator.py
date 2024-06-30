import json
import os
from dotenv import load_dotenv
import pandas as pd 
from src.mcq_generator.logger import logging
from src.mcq_generator.utils import read_data,get_table_data
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SequentialChain

load_dotenv()
key=os.getenv("api_key")
llm=ChatOpenAI(openai_api_key=key,model='gpt-3.5-turbo',temperature=0.3)
template_1='''
            Text={text}
            You are an expert MCQ maker. Given the above text,it is your job to create a quiz\
            of {number} multiple choice questions for {subject} students in the {tone} tone.
            Make sure the questions are not repeated and check all the questions to be confirming the tone.\
            Make sure the format of your response like {response_json} below and use it as guide.\
            ensure to make {number} MCQs '''
quiz_creation_prompt=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=template_1
)
quiz_creation_chain=LLMChain(llm=llm,prompt=quiz_creation_prompt,output_key='quiz',verbose=False)


template_2='''
            You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:'''

quiz_review_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=template_2
)
quiz_review_chain=LLMChain(llm=llm,prompt=quiz_review_prompt,output_key='review',verbose=False)
quiz_model=SequentialChain(chains=[quiz_creation_chain,quiz_review_chain],input_variables=['text','number','subject','tone','response_json'],output_variables=['quiz','review'],verbose=False)
