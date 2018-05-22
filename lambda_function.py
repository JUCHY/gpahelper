"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import data

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def calculategpa(intent,session):
    data.calculategpa();
    session_attributes = {}
    card_title = "Calculate"
    speech_output= "Your GPA is currently "+ data.personGPA
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def addclass1(intent,session):
    if 'class' in intent['slots']:
        newclass = intent['slots']['class']['value']
    session_attributes = {'class': newclass }
    card_title = "Add Class"
    speech_output= "What is your current GPA for this class?"
    reprompt_text = "What is your current GPA for this class?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def remclass(intent,session):
    session_attributes = {}
    card_title = "Welcome"
    if 'gone' in intent['slots']:
        yourclass = intent['slots']['gone']['value']
    data.removeclass(yourclass)
    data.calculategpa()
    speech_output = "The class "+yourclass+" has been removed"
    reprompt_text = "Do you need any more help?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


        
def tellgpa(intent,session):
    data.calculategpa()
    session_attributes = {}
    card_title = "Tell"
    speech_output= "Your GPA is currently "+ data.personGPA
    reprompt_text = "Is there anything else you want to know?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the GPA Helper. " \
                    "You may use commands such as tell me my GPA, or Add Class. " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "If you need any help, please ask Alexa for commands."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def addclass2(intent,session):
    card_title = "Add Class"
    should_end_session = False
    session_attributes = {}
    if session.get('attributes', {}) and "class" in session.get('attributes', {}):
        if 'one' and 'two' in intent['slots']:
            gpa1 = intent['slots']['one']['value']
            gpa2 = intent['slots']['two']['value']
            gpa = gpa1+'.'+gpa2
            newgpa = float(gpa)
            addingclass= session['attributes']['class']
            data.addclass(addingclass,newgpa)
            data.calculategpa()
            speech_output= "The class, "+addingclass+" has been added, with a GPA of "+ gpa
            reprompt_text = ""
            
    else:
        speech_output= "Your GPA is currently "+ data.personGPA
        reprompt_text = "Is there anything else you want to know?"
       
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        


def handle_session_end_request():
    data.savefunction()
    data.calculategpa()
    data.savefunction()
    card_title = "Session Ended"
    speech_output = "Thank you for trying out the GPA Helper. " \
                    "Your current info has been saved, have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "calculategpa":
        return calculategpa(intent, session)
    elif intent_name == "gpateller":
        return tellgpa(intent, session)
    elif intent_name=="addclass":
        return addclass1(intent,session)
    elif intent_name=="setGPA":
        return addclass2(intent,session)
    elif intent_name =="removeclass":
        return remclass(intent,session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
