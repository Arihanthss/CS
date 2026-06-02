from flask import Flask, render_template, request, redirect, session
from fare_calc import calculate_fare
from ticket_gen import ticketgen
from auth_module import auth, get_user_hash
from register_module import register
from balance_module import get_balance, add_funds

app = Flask(__name__)
app.secret_key = "super_secret_metro_key_123" 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/temptick')
def temporary_ticket_kiosk():
    return render_template('temptick.html')

@app.route('/buy', methods=['POST'])
def buy_ticket():
    start_id = int(request.form['start_station'])
    end_id = int(request.form['end_station'])
    
    final_cost = calculate_fare(start_station=start_id, end_station=end_id)
    if final_cost is None:
        return "Error: Invalid Stations."
        
    qr_string = ticketgen(start_id, end_id)
    return render_template('ticket.html', cost=final_cost, qr_data=qr_string, start=start_id, end=end_id)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
        
    if request.method == 'POST':
        user_input = request.form['username']
        pass_input = request.form['password']
        
        is_logged_in, message = auth(user_input, pass_input)
        
        if is_logged_in:
            session['user'] = user_input
            return redirect('/dashboard')
        else:
            return render_template('login.html', error=message)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
        
    if request.method == 'POST':
        user_input = request.form['username']
        pass_input = request.form['password']
        
        success, message = register(user_input, pass_input)
        
        if success:
            return f"<div style='font-family:Arial; text-align:center; margin-top:50px;'><h2 style='color:#4CAF50;'>{message}</h2><a href='/login' style='display:inline-block; margin-top:20px; padding:10px 20px; background:#8E24AA; color:white; text-decoration:none; border-radius:5px;'>Go to Login</a></div>"
        else:
            return render_template('register.html', error=message)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login') 
        
    current_user = session['user']
    current_balance = get_balance(current_user)
    
    # Grab hash and generate Type 1 Smart Card String
    user_hash = get_user_hash(current_user)
    qr_string = f"1:{current_user}:{user_hash}"
    
    return render_template('dashboard.html', username=current_user, balance=current_balance, qr_data=qr_string)

@app.route('/topup', methods=['POST'])
def topup():
    if 'user' not in session:
        return redirect('/login')
        
    amount_to_add = int(request.form['amount'])
    add_funds(session['user'], amount_to_add)
    return redirect('/dashboard')
    
@app.route('/logout')
def logout():
    session.pop('user', None) 
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)