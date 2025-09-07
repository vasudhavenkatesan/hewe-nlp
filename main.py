from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

from PIL import Image
import pytesseract

import pymysql
import config

# Point to the Tesseract executable (required for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\vasud\Documents\tesseract\tesseract.exe' 

def load_text_from_image(image):
    # Load the image
    image = Image.open(image)

    # Perform OCR
    text = pytesseract.image_to_string(image)

    return text.lower()

def extract_fields_from_text(information, prompt_template=None):
    urinary_report_template = """
    Given the urinary report {information} of a patient, extract the observation value of following fields in JSON format. Remove if two words are repeated in the same field, for example 'absent absent', and keep only one 'absent'.
    "full name":
    "age":
    "colour"
    "appearance":
    "specificGravity":
    "reaction":  
    "glucose": 
    "urobilinogen":
    "bilirubin": 
    "ketones":
    "nitrites": 
    "pusCells": 
    "rbc":
    "epithelialCells":
    "casts": 
    "crystals": 
    "remarks":
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=urinary_report_template
    )

    llm = ChatOllama(temperature=0, model="gemma3")
    parser = JsonOutputParser() 
   
    chain = summary_prompt_template | llm | parser

    response = chain.invoke(input={"information": text})
    return response


def get_connection_to_db():
    conn = pymysql.connect(
            host=config.db_host,
            user=config.db_user,
            password=config.db_password,
            database=config.db_name,
            port=config.db_port  # default MySQL port
        )

    return conn
def save_to_db(json_data):
    # Placeholder function to simulate saving to a database
    print("Saving to database:", json_data)
    conn = get_connection_to_db()
    cursor = conn.cursor()
    results = json_data
    results['id'] = 4
    results.pop('age', None)
    if 'full name' in results:
        results['patientName'] = results.pop('full name')

    # Build insert query dynamically from dict
    fields = ', '.join(results.keys())
    placeholders = ', '.join(['%s'] * len(results))
    values = tuple(results.values())

    sql = f"INSERT INTO urine_reports ({fields}) VALUES ({placeholders})"

    # Execute Insert
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    text = load_text_from_image("1.jpg")
    json_output = extract_fields_from_text(text)
    save_to_db(json_output)
