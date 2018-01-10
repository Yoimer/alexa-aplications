import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

######################################
from flask import Flask

import json

import requests

######################################


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# voice command is Alexa ask longview
# launch skill
@ask.launch
# read welcome message from template.yaml file
def launch_app():

    welcome_msg = render_template('welcome')

    return statement(welcome_msg)

# voice command is Alexa tell longview on
# turn system on
@ask.intent("OnIntent")

def turn_on():

    sess = requests.Session()

    # read actual(lastest) value on db
    url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?'
     
    data = sess.get(url)
     
    print data.content

    # check whether system is ON already
    if 'ON' in data.content:

        turn_on_msg = "System is already turned on. Not action taken."

        print(turn_on_msg)

        return statement(turn_on_msg)

    # save ON in db to be read by nodemcu
    else:
        sess = requests.Session()

        # sent ON to Nodemcu by sending 7 to db on castillolk
        url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?sw=7'

        data = sess.get(url)

        print data.content

        print "next line is the statement"

        turn_on_msg = "Turning system ON... It might take a few seconds, please wait."

        print(turn_on_msg)

        return statement(turn_on_msg)

# voice command is Alexa tell longview off
# turn system off
@ask.intent("OffIntent")

def turn_off():

    sess = requests.Session()

    # read actual(lastest) value on db
    url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?'
     
    data = sess.get(url)
     
    print data.content

    # check whether system is OFF already
    if 'OFF' in data.content:

        turn_off_msg = "System is already turned off. Not action taken."

        print(turn_off_msg)

        return statement(turn_off_msg)

    # save OFF in db to be read by nodemcu
    else:
        sess = requests.Session()

        # sent OFF to Nodemcu by sending 8 to db on castillolk
        url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?sw=8'
     
        data = sess.get(url)

        print data.content
     
        print "next line is the statement"

        turn_on_msg = "Turning system OFF... It might take a few seconds, please wait."

        print(turn_on_msg)
     
        return statement(turn_on_msg)

# voice command is Alexa ask longview temperature
# check temperature
@ask.intent("TemperatureIntent")

def get_temperature():
    sess = requests.Session()

    url = 'https://phpcourse.000webhostapp.com/temperature.txt'

    '''
    /temperature.txt file content
    32.56
    '''

    data = sess.get(url)
     
    print data.content
     
    print "next line is temperature"
    
    temperature_msg = "The temperature value that you requested is: " + data.content + " Celsius"

    #return statement(data.content)
    return statement(temperature_msg)

# voice command is Alexa tell ask longview humidity
# check humidity
@ask.intent("HumidityIntent")

def get_humidity():
    sess = requests.Session()

    url = 'https://phpcourse.000webhostapp.com/humidity.txt'

    '''
    /humidity.txt file content
    60.25
    '''

    data = sess.get(url)
     
    print data.content
     
    print "next line is humidity"
    
    humidity_msg = "The humidity value that you requested is: " + data.content + " Percentage"

    #return statement(data.content)
    return statement(humidity_msg)

# voice command is Alexa ask longview full status
# check any process variable on system
@ask.intent("FullStatusIntent")

def get_full_status():
    sess = requests.Session()

    url = 'https://phpcourse.000webhostapp.com/full-status.txt'

    '''
    /full-status.txt file content
    every three points at the end of each line means a little pause when Alexa is replying back

    Temperature: 30.25 Celsius...
    Humidity: 60.25 Percentage...
    Pressure: 300 Pascals...
    Flow: 200 Litres per second...
    '''

    data = sess.get(url)

    print data.content

    print type(data.content)

    full_status_msg = "The variable values that you requested are: " + data.content
    return statement(full_status_msg)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')