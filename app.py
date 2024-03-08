from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__, static_folder='website/static', template_folder='website/templates')
app.secret_key = 'your_secret_key'

# MySQL connection configuration
mysql_config = {
    'host': 'cs1.ucc.ie',
    'user': 'facialrecognition2024',
    'password': 'caipu',
    'database': 'facialrecognition2024'
}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return "User already exists! Please choose a different username."
            
            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            connection.commit()
            cursor.close()
            connection.close()
            
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            return f"Error: {e}"
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            
            # Check if username and password match
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
                    
            if user:
                session['username'] = username
                return redirect('https://emotions-dashboard.upwardsdesignstudio.com')
            else:
                return "Incorrect username or password."
        except mysql.connector.Error as e:
            return f"Error: {e}"
            
    return render_template('login.html')

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
