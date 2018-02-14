import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

######################################
from flask import Flask

import json

import requests

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


######################################
# Skill name: longview
# Invocation Name : longview system


##########launch skill##########
# voice commands are:
#Alexa, start longview system
#Alexa, open longview system

# launch skill
@ask.launch
# read welcome message from template.yaml file
def launch_app():

    welcome_msg = render_template('welcome')

    #return statement(welcome_msg)
    return question(welcome_msg)


##########stop skill##########
# voice commands are:
#Alexa, stop

# stop skill
@ask.intent("StopIntent")
def stop():
    return statement("Stopping the skill, thanks for using")

##########turn on device##########
# voice commands are:
#Alexa, tell longview system turn on
#Alexa, ask longview system to turn on

# turn system on
@ask.intent("OnIntent")

def turn_on():

    sess = requests.Session()

    # read actual(lastest) value on db
    #url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?'
    url = 'https://phpcourse.000webhostapp.com/alexa.php?'
     
    data = sess.get(url)
     
    print data.content

    # check whether system is ON already
    if 'ON' in data.content:

        turn_on_msg = "Relay is already turned on. Not action taken."

        print(turn_on_msg)

        return statement(turn_on_msg)

    # save ON in db to be read by nodemcu
    else:
        sess = requests.Session()

        # sent ON to Nodemcu by sending 7 to db on castillolk
        #url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?sw=7'
        url = 'https://phpcourse.000webhostapp.com/alexa.php?value=7'

        data = sess.get(url)

        print data.content

        print "next line is the statement"

        turn_on_msg = "Turning Relay ON... It might take a few seconds, please wait."

        print(turn_on_msg)

        return statement(turn_on_msg)


##########turn off device##########
# voice commands are:
#Alexa, tell longview system to turn off
#Alexa, ask longview system to turn off

# turn system off
@ask.intent("OffIntent")

def turn_off():

    sess = requests.Session()

    # read actual(lastest) value on db
    #url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?'
    url = 'https://phpcourse.000webhostapp.com/alexa.php?'
     
    data = sess.get(url)
     
    print data.content

    # check whether system is OFF already
    if 'OFF' in data.content:

        turn_off_msg = "Relay is already turned off. Not action taken."

        print(turn_off_msg)

        return statement(turn_off_msg)

    # save OFF in db to be read by nodemcu
    else:
        sess = requests.Session()

        # sent OFF to Nodemcu by sending 8 to db on castillolk
        #url = 'http://castillolk.com.ve/proyectos/sms/alexa.php?sw=8'
        url = 'https://phpcourse.000webhostapp.com/alexa.php?value=8'
     
        data = sess.get(url)

        print data.content
     
        print "next line is the statement"

        turn_on_msg = "Turning Relay OFF... It might take a few seconds, please wait."

        print(turn_on_msg)
     
        return statement(turn_on_msg)


##########ask for temperature##########
# voice commands are:
#Alexa, ask longview system for temperature
#Alexa, give me temperature from longview system

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



##########ask for humidity##########
# voice commands are:
#Alexa, ask longview system for humidity
#Alexa, give me humidity from longview system

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


##########ask for full process variable status##########
# voice commands are:
#Alexa, ask longview system for full status
#Alexa, give me full status from longview system

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