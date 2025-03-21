import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
import io
import PIL.Image
import tempfile
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from pathlib import Path

genai.configure(api_key="AIzaSyDc6bNS1lVtLovKK4mEmHkalKZqkRRtO3Q")

def generate_response(user_input):
    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(contents=user_input)
        return response.text
    except Exception as e:
        print("Error:", e)
        return "I'm having trouble generating a response."
def csv_to_pdf(csv_filepath, pdf_filepath):
    df = pd.read_csv(csv_filepath)
    c = canvas.Canvas(pdf_filepath, pagesize=letter)
    width, height = letter

    c.drawString(30, height - 40, "CSV Data Summary")
    y_position = height - 80

    for i, row in df.iterrows():
        c.drawString(30, y_position, str(row.values))
        y_position -= 20
        if y_position < 40:
            c.showPage()
            y_position = height - 40
    
    c.save()