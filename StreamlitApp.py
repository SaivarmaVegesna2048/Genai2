import json
import os
import pandas as pd 
import traceback
import streamlit as st
from dotenv import load_dotenv
from src.mcq_generator.utils import read_data,get_table_data
from langchain.callbacks import get_openai_callback
from src.mcq_generator.MCQ_generator import quiz_model
from src.mcq_generator.logger import logging

with open(r'C:\Users\saivarma\Desktop\Genai2\response.json','r') as file:
    response_json=json.load(file)
st.title("MCQ Creator application with langchain")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("Upload a PDF or txt file")
    mcq_count=st.number_input("No.of mcq's",min_value=3,max_value=50)
    subject=st.text_input("Enter the subject",max_chars=20)
    tone=st.text_input("Enter the tone",max_chars=20,placeholder='simple')
    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone: 
        with st.spinner("loading..."):
            try:
                text=read_data(uploaded_file)
                with get_openai_callback() as cb:
                    response=quiz_model({
                        'text':text,
                        'number':mcq_count,
                        'subject':subject,
                        'tone':tone,
                        'response_json':json.dumps(response_json)

                    })
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error('Error')
            else:
                print(f"Total tokens:{cb.total_tokens}")
                print(f"prompt tokens:{cb.prompt_tokens}")
                print(f"completion tokens:{cb.completion_tokens}")
                print(f"Total cost:{cb.total_cost}")
                if isinstance(response,dict):
                    quiz=response.get("quiz")
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.dataframe(df)
                            st.text_area(label='review',value=response['review'])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)
                            
