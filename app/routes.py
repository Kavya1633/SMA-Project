# Handles the main pages like dashboard

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp=Blueprint('main',__name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required

def dashboard():
    # Pass the current user's detail to the html template
    return render_template('dashboard.html',user=current_user)

