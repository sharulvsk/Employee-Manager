from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functs import generate_response, csv_to_pdf
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
import io
import PIL.Image
import tempfile
import csv
from reportlab.lib.pagesizes import letter
import google.generativeai as genai
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'supersecretkey' 
genai.configure(api_key="AIzaSyDc6bNS1lVtLovKK4mEmHkalKZqkRRtO3Q")
model = genai.GenerativeModel(model_name="gemini-2.0-flash")



credentials = {
    "manager@gmail.com": {"password": "manager123", "role": "manager"},
    "employee@gmail.com": {"password": "employee123", "role": "employee"}
}
    
@app.route('/')
def home():
    return redirect(url_for('signup'))

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/manage_tasks')
def manage_tasks():
    return render_template('manage_tasks.html')


@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/view_task')
def view_task():
    task_id = request.args.get('id')
    return render_template('view_task.html', task_id=task_id)

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/team_management')
def team_management():
    return render_template('team_management.html')

@app.route('/add_employee')
def add_employee():
    return render_template('add_employee.html')

@app.route('/delete_employee')
def delete_employee():
    return render_template('delete_employee.html')

@app.route('/update_employee')
def update_employee():
    return render_template('update_employee.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = credentials.get(email)
        if user and user['password'] == password:
            session['email'] = email
            session['role'] = user['role']
            if user['role'] == 'manager':
                return redirect(url_for('manager_home'))
            else:
                return redirect(url_for('employee_home'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('signin.html')

@app.route('/manager_home')
def manager_home():
    if session.get('role') == 'manager':
        return render_template('manager_home.html')
    else:
        return "Access Denied. Managers Only."

@app.route('/employee_home')
def employee_home():
    if session.get('role') == 'employee':
        return render_template('employee_home.html')
    else:
        return "Access Denied. Employees Only."
    
@app.route('/assign.html')  
def assign_task():
    return render_template('assign.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
    if user_message.lower() == "hi":
        return jsonify({"response": "Hello! How can I assist you today?"})
    
    elif user_message.lower() == "i have few doubts in csv":
        try:
            csv_filepath = r'C:\From Destop\purple-chat-bot\purple-chatbot\data.csv'
            pdf_filepath = r'C:\Users\shankaripriya s\Downloads\output.pdf'
            csv_to_pdf(csv_filepath, pdf_filepath)

            media = Path(r'C:\Users\shankaripriya s\Downloads')
            sample_pdf = genai.upload_file(media / 'output.pdf')
            response4 = model.generate_content(["Summary", sample_pdf])
            
            return jsonify({"response": response4.text})
        except Exception as e:
            return jsonify({"response": f"Error: {str(e)}"})
    
    else:
        try:
            response = model.generate_content(user_message)
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"response": f"Error generating response: {str(e)}"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
