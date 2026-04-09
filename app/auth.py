# Handles all authentication routes: register, login, logout

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo


auth_bp=Blueprint('auth',__name__)

# Register/Create Account Logic
@auth_bp.route('/register', methods=['GET','POST'])

def register():
    if request.method=='POST':
        
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        
        # find user in db using email
        existing_user=mongo.db.users.find_one({'email':email})
        
        if existing_user:
            flash('Email already registered. Please log in.','danger')
            
            return redirect(url_for('auth.login'))
        
        hashed_password=generate_password_hash(password)
        
        # adds the data in the mongoDb
        mongo.db.users.insert_one({
            'username':username,
            'email':email,
            'password':hashed_password
        })
        
        flash('Account created! Please log in.','success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


# Account Login Logic
@auth_bp.route('/login', methods=['GET','POST'])

def login():
    
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        
        # find user in the db using email
        user_data=mongo.db.users.find_one({'email':email})
        
        if user_data and check_password_hash(user_data['password'],password):
            
            from app.models import User
            user=User(user_data)
            
             # Flask stores user ID in a secure session cookie
            login_user(user)
            
            flash('Welcome back!','success')
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid email or password.','danger')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')

# Account Logout Logic
@auth_bp.route('/logout')
@login_required # only logged in users can visit this route

def logout():
    # clear the loggedIn user session- user is logged out now
    logout_user()
    
    flash('You have been logged out,','info')
    return redirect(url_for('auth.login'))
    
            
        
        