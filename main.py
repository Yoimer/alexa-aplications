import logging

import random
#from random import randint
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
#Alexa, launch longview system

# launch skill
@ask.launch
# read welcome message from template.yaml file
def launch_app():

    welcome_msg = render_template('welcome')

    #return statement(welcome_msg)
    return question(welcome_msg)


##########stop skill##########
# voice commands are:
# stop
#Alexa, stop

# stop skill
#@ask.intent("StopIntent")
@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping the skill, thanks for using")

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


##########ask for help##########
# voice commands are:
#help (when welcoming)
#Alexa ask longview system for help (anytime)

# ask for help when welcoming or anytime
@ask.intent("AMAZON.HelpIntent")
def help():

    help_list = [

                    "temperature say... alexa give me temperature from longview system...",

                    "humidity say... alexa give me humidity from longview system...",

                    "the whole variable process say... alexa give me full status from longview system..."
                ]

    # say a radom msg from help_list
    help_msg = "To ask for " + help_list[random.randint(0,(len(help_list) - 1))]
    reprompt_msg = "...Please" + help_msg
    reprompt_msg += "or. say... stop to close the skill"
    #return statement(help_msg)
    return question(help_msg).reprompt(reprompt_msg)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')