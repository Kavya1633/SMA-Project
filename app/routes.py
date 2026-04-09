# Handles the main pages ->dashboard, cases

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user


from app import mongo

from bson.objectid import ObjectId
from datetime import datetime

main_bp=Blueprint('main',__name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required

def dashboard():
    
    cases=mongo.db.cases.find({'user_id':current_user.id})
    
    cases_list=list(cases)
    # Pass the current user's detail and cases to the html template
    return render_template('dashboard.html',
                           user=current_user,
                           cases=cases_list)
    
@main_bp.route('/case/create', methods=['POST'])
@login_required

def create_case():
    
    # Case form fields
    case_name=request.form.get('case_name')
    keyword=request.form.get('keyword')
    platform=request.form.get('platform')
    date_range=request.form.get('date_range')
    
    # Case name and keyword **
    if not case_name or not keyword:
        flash('Case name and keyword are required!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Create and link case with loggedIn user
    mongo.db.cases.insert_one({
        'user_id':current_user.id,
        'case_name':case_name,
        'keyword':keyword,
        'platform':platform,
        'date_range':date_range,
        'created_at':datetime.now().strftime('%d %b %Y'),
        'status':'active'
    })
    
    flash(f'Case "{case_name}" created successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/case/<case_id>')
@login_required

def view_case(case_id):
    
    case=mongo.db.cases.find_one({
        '_id':ObjectId(case_id),
        'user_id':current_user.id
    })
    
    if not case:
        flash('Case not found!','danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('case.html',case=case, user=current_user)


@main_bp.route('/case/<case_id>/delete', methods=['POST'])
@login_required

def delete_case(case_id):
    # verify user ownership before deleting
    mongo.db.cases.delete_one({
        '_id':ObjectId(case_id),
        'user_id':current_user.id
    }) 
    
    flash('Case deleted successfully!', 'info')
    return redirect(url_for('main.dashboard'))


    
    
    
    

