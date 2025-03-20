from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
