import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

ASK_APPLICATION_ID = 'amzn1.ask.skill.2d740502-1149-44a2-98d2-3544fc24cb72'
ASK_VERIFY_REQUESTS = True
ASK_VERIFY_TIMESTAMP_DEBUG = True


@ask.intent("dress_recommender")
def main_function():
    return dress_recommender()

	
@ask.intent("AMAZON.StopIntent")
def stop_function():
    return statement("See you tomorrow")

	
@ask.intent("AMAZON.CancelIntent")
def cancel_function():
    return statement("See you tomorrow")


@ask.launch
def launched():
    return dress_recommender()

@ask.session_ended
def session_ended():
    return "{}", 200

# --------------- Main handler ------------------
def lambda_handler(event, context):
    if event['session']['application']['applicationId'] != "amzn1.ask.skill.2d740502-1149-44a2-98d2-3544fc24cb72":
        print("wrong app id")
        return ''
    print("event.session.application.applicationId=" +
          str(event['session']['application']['applicationId']))
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


# --------------- Response handler ------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
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
    jj = {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    return app.response_class(json.dumps(jj), content_type='application/json')


# --------------- Events ------------------
def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "quotationOfTheDay":
        return dress_recommender()


#--------------- App Functions ------------------------
def dress_recommender():
    session_attributes = {}
    card_title = "Quotation Of The Day"
    quotation = get_dress()
    speech_output = quotation
    reprompt_text = quotation
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_dress():
    now = datetime.datetime.now()
    day = now.day
    return quotation_list[int(day)%8]


#---------------- Dress List ----------------------------
quotation_list = ("Nicely fitted tops and blouses, although shirts should never be tight or revealing.", "Slacks or skirts in more casual fabrics, such as cotton. If denim is permitted, dark-wash only. Avoid overly casual denim cuts, like cutoffs or flare jeans.", "Skirts should remain at knee-length.", "Open-toed shoes are permitted. Avoid casual shoes such as sneakers or flip-flops.", "Casual accessories, such as scarves. Larger rings, bracelets, earrings, and necklaces are fine, and may be of any quality.", "More leeway with hair length, style, and color. More adventurous styles and colors are typically fine.", "Nails can be painted in brighter colors, or with any type of pattern. Avoid novelty characters or designs, or limit “louder” designs to one nail only.")


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
	app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.2d740502-1149-44a2-98d2-3544fc24cb72'
	app.config['ASK_VERIFY_REQUESTS'] = True
	app.config['ASK_VERIFY_TIMESTAMP_DEBUG'] = True
    app.run(debug=True)

