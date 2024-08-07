import os
import json
import PyPDF2
import traceback
def read_data(file):
    if file.name.endswith('.pdf'):
        try:
            pdfreader=PyPDF2.PdfFileReader(file)
            text=[]
            for page in pdfreader.pages:
                text=page.extract_text()
            return text
        except Exception as e:
            raise Exception('Error reading the pdf file')
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise Exception('Unsupported file format only pdf and text format file supported')
def get_table_data(quiz):
    try:
        quiz_dict=json.loads(quiz)
        quiz_data_table=[]
        for key,value in quiz_dict.items():
            mcq=value['mcq'],
            options='|'.join(
                [
                    f"{option}:{option_value}"
                    for option, option_value in value['options'].items()
                ]
            ),
            correct=value['correct'],
            quiz_data_table.append({'MCQ':mcq,'Choices':options,'Correct':correct})
        return quiz_data_table
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False