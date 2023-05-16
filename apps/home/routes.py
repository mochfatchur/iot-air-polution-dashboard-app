# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import requests
from apps import model_1, model_2
from apps.home import blueprint
from flask import render_template, request, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import jsonify

# model prediction
import pickle
import time
import numpy as np
import pandas as pd
from datetime import datetime

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
    

@blueprint.route('/predict')
def predict():
    # get hour and minute now
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    # preprocess hour and minute
    df = pd.DataFrame({'hour': [current_hour], 'minute': [current_minute]})
    features = df.values.reshape(1, -1)
    # predict
    prediction = model_1.predict(features)
    # classify
    if prediction[0] == 0:
        return "Normal"
    elif prediction[0] == 1:
        return "Warning"
    elif prediction[0] == 2:
        return "Danger"
    else:
        return "Error Occurs"



@blueprint.route('/predictdua')
def predictdua():
    # get hour and minute now
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    # preprocess hour and minute
    df = pd.DataFrame({'hour': [current_hour], 'minute': [current_minute]})
    features = df.values.reshape(1, -1)
    # predict
    prediction = model_2.predict(features)
    # classify
    if prediction[0] == 0:
        return "Normal"
    elif prediction[0] == 1:
        return "Warning"
    elif prediction[0] == 2:
        return "Danger"
    else:
        return "Error Occurs"


@blueprint.route('/latestsatu')
def get_latest_data_info1():
    # Retrieve the data from /data route
    response = requests.get('http://127.0.0.1:5000/data')  # Replace with the appropriate URL
    data = response.json()

    # Get the last item from the data
    latest_data = data[-1]

    return jsonify(latest_data)

@blueprint.route('/latestdua')
def get_latest_data_info2():
    # Retrieve the data from /data route
    response = requests.get('http://127.0.0.1:5000/datadua')  # Replace with the appropriate URL
    data = response.json()

    # Get the last item from the data
    latest_data = data[-1]

    return jsonify(latest_data)

@blueprint.route('/stream')
def stream():
    def generate():
        while True:
            prediction = predict()
            # latest_data_info = get_latest_data_info1()
            
            # day = latest_data_info.day
            # month = latest_data_info.month
            # hour = latest_data_info.hour
            # minute = latest_data_info.minute
            # timestamp = datetime(datetime.now().year, month, day, hour, minute)
            # value = latest_data_info.value

            yield f"data: {prediction}\n\n"
            # yield f"timestamp: {timestamp}\n\n"
            # yield f"value: {value}\n\n"
            time.sleep(60)  # Adjust the delay according to your needs

    return Response(generate(), mimetype='text/event-stream')

@blueprint.route('/streamdua')
def streamdua():
    def generate():
        while True:
            prediction = predictdua()
            yield f"data: {prediction}\n\n"
            time.sleep(60)  # Adjust the delay according to your needs

    return Response(generate(), mimetype='text/event-stream')




@blueprint.route('/predictall')
def predictAll1():
    # Define arrays of current_hour and current_minute
    current_hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    current_minute = [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Convert current_hour and current_minute to arrays
    current_hour = np.array(current_hour)
    current_minute = np.array(current_minute)
    
    # preprocess hour and minute
    df = pd.DataFrame({'hour': current_hour, 'minute': current_minute})
    features = df.values
    
    # predict
    predictions = model_1.predict(features)
    predictions1 = model_2.predict(features)
    
    # classify
    results = []
    for hour, prediction in zip(current_hour, predictions):
        if prediction == 0:
            result = "Normal"
        elif prediction == 1:
            result = "Warning"
        elif prediction == 2:
            result = "Danger"
        else:
            result = "Error Occurs"
        results.append({'hour': hour, 'prediction': result})
    
    results1 = []
    for hour, prediction in zip(current_hour, predictions1):
        if prediction == 0:
            result = "Normal"
        elif prediction == 1:
            result = "Warning"
        elif prediction == 2:
            result = "Danger"
        else:
            result = "Error Occurs"
        results1.append({'hour': hour, 'prediction': result})
    
    # Pass the results to the HTML template
    return render_template('home/tbl_bootstrap.html', results=results, results1 = results1)


@blueprint.route('/predictalldua')
def predictAllDua():
    # Define arrays of current_hour and current_minute
    current_hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    current_minute = [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Convert current_hour and current_minute to arrays
    current_hour = np.array(current_hour)
    current_minute = np.array(current_minute)
    
    # preprocess hour and minute
    df = pd.DataFrame({'hour': current_hour, 'minute': current_minute})
    features = df.values
    
    # predict
    predictions = model_2.predict(features)
    
    # classify
    results = []
    for prediction in predictions:
        if prediction == 0:
            results.append("Normal")
        elif prediction == 1:
            results.append("Warning")
        elif prediction == 2:
            results.append("Danger")
        else:
            results.append("Error Occurs")
    
    
    # Return the response as JSON
    return jsonify(results)