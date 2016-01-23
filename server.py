import os
from flask import Flask, request, json
from twilio.util import TwilioCapability
import twilio.twiml

#import json

# Account Sid and Auth Token can be found in your account dashboard
ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

# TwiML app outgoing connections will use
APP_SID = 'APZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'

CALLER_ID = '+12345678901'
CLIENT = 'jenny'

app = Flask(__name__)

@app.route('/token', methods=['GET', 'POST'])
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
  app_sid = os.environ.get("APP_SID", APP_SID)

  capability = TwilioCapability(account_sid, auth_token)

  # This allows outgoing connections to TwiML application
  if request.values.get('allowOutgoing') != 'false':
     capability.allow_client_outgoing(app_sid)

  # This allows incoming connections to client (if specified)
  client = request.values.get('client')
  if client != None:
    capability.allow_client_incoming(client)

  # This returns a token to use with Twilio based on the account and capabilities defined above
  #return capability.generate()
  #return "%s({'twilioToken':capability.generate() })" % _GET_PARAMS('callback')
  #import json
  #json_data = json.dumps({'twilioToken': capability.generate()})
  #return "callback(%s);" % json_data
  
  #print 'Content-Type: application/json\n\n'
  
  twilphonetoken = capability.generate()
  #json_data = json.dumps({'twilioToken': twilphonetoken)})
  #json_data = '{"twilioToken":' + twilphonetoken + '}'
  #json_data = json.dumps({'{"twilioToken":' + twilphonetoken + '}'})
  #json_data = json.dumps({'{"twilioToken":' + twilphonetoken + '}'})
  json_data = 'callback({"twilioToken":' + twilphonetoken + ', mimetype="application/json"})'
  
  
  

  #callback_name = input(callback='callback').callback
  #web.header('Content-Type', 'application/json') 
  #return '%s(%s)' % (callback_name, twilphonetoken)
  
  return json_data
  #return "callback(%s);" % json_data
  
  #return "%s(%s)" % "callback(%s);", json_data , mimetype="application/json"
  #return response
  #return json_data
  
  #b = dumps({'twilioToken': twilphonetoken })
  
  #callback_name = web.input(callback='callback').callback
  #header('Content-Type', 'application/javascript') 
  #web.header('Content-Type', 'application/javascript') 
  #return '%s(%s)' % (b)
  #return '%s(%s)' % (callback_name, json)
  
  #return "callback(%s);" % ({'twilioToken': twilphonetoken})
  #return "%s({'twilioToken':" twilphonetoken })" % _GET_PARAMS('callback')

@app.route('/call', methods=['GET', 'POST'])
def call():
  """ This method routes calls from/to client                  """
  """ Rules: 1. From can be either client:name or PSTN number  """
  """        2. To value specifies target. When call is coming """
  """           from PSTN, To value is ignored and call is     """
  """           routed to client named CLIENT                  """
  resp = twilio.twiml.Response()
  from_value = request.values.get('From')
  to = request.values.get('To')
  if not (from_value and to):
    return str(resp.say("Invalid request"))
  from_client = from_value.startswith('client')
  caller_id = os.environ.get("CALLER_ID", CALLER_ID)
  if not from_client:
    # PSTN -> client
    resp.dial(callerId=from_value).client(CLIENT)
  elif to.startswith("client:"):
    # client -> client
    resp.dial(callerId=from_value).client(to[7:])
  else:
    # client -> PSTN
    resp.dial(to, callerId=caller_id)
  return str(resp)

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
