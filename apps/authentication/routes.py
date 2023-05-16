# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import requests
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

# AWS rds
from flask import jsonify
import pymysql.cursors


#  authentication
from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

# aws rds
# Define a route for retrieving data from the database
@blueprint.route('/data')
def get_data():
    # Connect to the database
    connection = pymysql.connect(
        host='awseb-e-mb89cnnti3-stack-awsebrdsdatabase-odsswowpmrqh.csmyswtkxubb.ap-southeast-3.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='admin123',
        cursorclass = pymysql.cursors.DictCursor
    )

    # Retrieve data from the database
    with connection.cursor() as cursor:
        sql1 = "use mq135;"
        cursor.execute(sql1)
        sql2 = '''select * from mq135_data where id_esp32 = 1;'''
        cursor.execute(sql2)
        result = cursor.fetchall()

    # Convert data to a list of dictionaries (for easy JSON serialization)
    data = result
    # for row in result:
    #     data.append({
    #         'id': row[0],
    #         'month': row[1],
    #         'day': row[2]
    #     })

    # Return data as JSON
    return jsonify(data)

@blueprint.route('/datadua')
def get_data2():
    # Connect to the database
    connection = pymysql.connect(
        host='awseb-e-mb89cnnti3-stack-awsebrdsdatabase-odsswowpmrqh.csmyswtkxubb.ap-southeast-3.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='admin123',
        cursorclass = pymysql.cursors.DictCursor
    )

    # Retrieve data from the database
    with connection.cursor() as cursor:
        sql1 = "use mq135;"
        cursor.execute(sql1)
        sql2 = '''select * from mq135_data where id_esp32 = 2;'''
        cursor.execute(sql2)
        result = cursor.fetchall()

    # Convert data to a list of dictionaries (for easy JSON serialization)
    data = result
    # for row in result:
    #     data.append({
    #         'id': row[0],
    #         'month': row[1],
    #         'day': row[2]
    #     })

    # Return data as JSON
    return jsonify(data)