from flask import Flask, render_template, jsonify, request, redirect, url_for
import pyodbc
from datetime import datetime
from flask_socketio import SocketIO
from functools import wraps
from flask import session



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = 'dH7#k9$mP2&vL4@nR8'







def get_db_connection():
    conn = pyodbc.connect(r'Driver={SQL Server};'
                         r'Server=.\SQLEXPRESS;'
                         r'Database=dadd1;'
                         r'UID=sa;'
                         r'PWD=ahmed;'
                         r'Trusted_Connection=no;')
    return conn




def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'salary')
    CREATE TABLE salary (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100),
        hourly_rate DECIMAL(10,2),
        masroof DECIMAL(10,2) DEFAULT 0
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

create_tables()



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/manage_rates')
@login_required
def manage_rates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, hourly_rate, masroof FROM salary")
    rates = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_rates.html', rates=rates)

@app.route('/get_rates')
def get_rates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, hourly_rate, masroof FROM salary")
    rates = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'name': row[0], 'rate': row[1], 'masroof': row[2]} for row in rates])

@app.route('/update_rate', methods=['POST'])
def update_rate():
    name = request.form.get('name')
    rate = request.form.get('rate')
    masroof = request.form.get('masroof', 0)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF EXISTS (SELECT 1 FROM salary WHERE name = ?)
            UPDATE salary SET hourly_rate = ?, masroof = ? WHERE name = ?
        ELSE
            INSERT INTO salary (name, hourly_rate, masroof) VALUES (?, ?, ?)
    """, (name, rate, masroof, name, name, rate, masroof))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Elmohandes@Degla' and password == 'Elmohandes@degla':
            session['logged_in'] = True
            return redirect(url_for('salary'))
    return render_template('login.html')

@app.route('/salary')
@login_required
def salary():
    return render_template('salary.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/get_names')
def get_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nach
        FROM cheef
        WHERE debch NOT LIKE N'%دلفري%'
        AND debch NOT LIKE N'%دلفرى%'
    """)
    names = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify([{'name': row[0]} for row in names])

@app.route('/get_attendance')
def get_attendance():
    name = request.args.get('name')
    name = name.strip()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT hourly_rate, masroof FROM salary WHERE name = ?", (name,))
    rate_row = cursor.fetchone()
    hourly_rate = float(rate_row[0]) if rate_row else 0
    daily_masroof = float(rate_row[1]) if rate_row else 0
    
    cursor.execute('''
        SELECT day1, hodor, ener, tim
        FROM tim1
        WHERE nam = ? AND day1 BETWEEN ? AND ?
        ORDER BY day1
    ''', (name, start_date, end_date))
    
    records = cursor.fetchall()
    attendance_days = sum(1 for row in records if row[3] and float(row[3]) > 0)
    total_masroof = daily_masroof * attendance_days
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'records': [{
            'day': row[0],
            'time_in': row[1],
            'time_out': row[2],
            'hours': row[3]
        } for row in records],
        'hourly_rate': hourly_rate,
        'daily_masroof': daily_masroof,
        'attendance_days': attendance_days,
        'total_masroof': total_masroof
    })


@app.route('/get_all_attendance')
def get_all_attendance():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    names = request.args.getlist('names[]')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    result = []
    for name in names:
        name = name.strip()
        
        cursor.execute("SELECT hourly_rate, masroof FROM salary WHERE name = ?", (name,))
        rate_row = cursor.fetchone()
        hourly_rate = float(rate_row[0]) if rate_row else 0
        daily_masroof = float(rate_row[1]) if rate_row else 0
        
        query = '''
            SELECT
                CONVERT(VARCHAR, t.day1, 23) as day1,
                CONVERT(VARCHAR(10), CAST(t.hodor AS TIME), 100) as hodor,
                CONVERT(VARCHAR(10), CAST(t.ener AS TIME), 100) as ener,
                t.tim
            FROM tim1 t
            WHERE t.nam = ?
            AND CONVERT(DATE, t.day1) BETWEEN CONVERT(DATE, ?) AND CONVERT(DATE, ?)
            ORDER BY t.day1
        '''
        
        cursor.execute(query, (name, start_date, end_date))
        records = cursor.fetchall()
        
        attendance_records = []
        total_hours = 0
        attendance_days = 0
        
        for row in records:
            hours = float(row[3]) if row[3] else 0
            if hours > 0:
                attendance_days += 1
            total_hours += hours
            
            attendance_records.append({
                'day': row[0],
                'time_in': row[1],
                'time_out': row[2],
                'hours': hours
            })
        
        total_salary = total_hours * hourly_rate
        total_masroof = daily_masroof * attendance_days
        net_salary = total_salary - total_masroof
        
        result.append({
            'name': name,
            'hourly_rate': hourly_rate,
            'daily_masroof': daily_masroof,
            'total_hours': round(total_hours, 2),
            'attendance_days': attendance_days,
            'total_salary': round(total_salary, 2),
            'total_masroof': round(total_masroof, 2),
            'net_salary': round(net_salary, 2),
            'records': attendance_records
        })
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=False)
