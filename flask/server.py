from flask import Flask
from flask import request
import flask
from twilio import twiml
from twilio.rest import TwilioRestClient
from flask import redirect
from flask_cors import CORS, cross_origin
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import pdb
import requests


auth = Oauth1Authenticator(
    consumer_key="Ybgxn8fAjGVLNvjh-DGnrg",
    consumer_secret="HS8MmSHy7yYis_dkiJhyd5Kk6pI",
    token="xXQ3qCZr9vkRKZ-nqmem3w0bOORK_s5w",
    token_secret="4soDIWMkyD83RbWdl8SgcvtOdAk"
)


client = Client(auth)


wikiinfo = ""


app = Flask(__name__)
CORS(app)

@app.route("/hello", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    resp = twiml.Response()
    resp.say("Hello Monkey")

    return str(resp)

def sms_utility(lan, lon):

    geocoord = str(lan) + "%7C" + str(lon)

    wikiGeo = "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=10000&gslimit=2&prop=extracts&format=json&gscoord="


    f = requests.get(wikiGeo + geocoord)
    pageid = str(json.loads(f.text)['query']['geosearch'][0]['pageid'])

    wikiPageId = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids=';

    re = requests.get(wikiPageId + pageid)
    print(re.text)
    return json.loads(re.text)['query']['pages'][pageid]['extract']




def transform_yelp(resp):

    d = []

    for business in resp.businesses:

        b = {}
        b["name"] = business.name
        b["image_url"] = business.image_url
        b["categories"] = business.categories
        b["rating"] = business.rating
        b["snippet_text"] = business.snippet_text
        #business = client.get_business(business.id)

        d.append(b)

    return d

def eucledian(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1**2 + y2**2))**1/2


def define_routes(starting_point, businesses):

    #Calculate distances
    s = starting_point





@app.route("/test", methods=['GET', 'POST'])
def test():
    """Respond to incoming requests."""
    data = json.loads(request.data)

    for key in data:
        if(data[key] == "true"):
            prefs[key] = True

    #Yelp search
    params = {
        'lang': 'en',
        'categories_list' : ",".join(data["preferences"])
    }

    res = client.search_by_coordinates(float(data["lat"]), float(data["long"]), **params)

    res = transform_yelp(res)

    return  json.dumps(res)




CORS(app)
@app.route("/getInfo", methods=['GET', 'POST'])
def getInfo():
    """Respond to incoming requests."""
    data = json.loads(request.data)
    prefs = {}
    for key in data:
        if(data[key] == "true"):
            prefs[key] = True

    #Yelp search
    params = {
        'lang': 'en'    
        }

    print(params)
    res = client.search_by_coordinates(float(data["lat"]), float(data["long"]), **params)

    res = transform_yelp(res)

    return  json.dumps(res)

@app.route("/getRoute", methods=['GET', 'POST'])
def getRoute():
    data = json.loads(request.data)
    prefs = {}
    for key in data:
        if(data[key] == "true"):
            prefs[key] = True

    #Yelp search
    params = {
        'lang': 'en'    
        }

    res = client.search_by_coordinates(float(data["lat"]), float(data["long"]), **params)

    res = transform_yelp(res)

    return  json.dumps(res)
   

@app.route("/response", methods=['GET', 'POST'])
def response():
    global wikinfo
    request = twiml.Response()
    print(wikiinfo)
    request.say(wikiinfo)
    return str(request)




@app.route("/sms", methods=['GET', 'POST'])
def sms():
    global wikiinfo
    """Respond to incoming requests."""
    data = request.values["Body"]
    number = request.values["From"]

    ACCOUNT_SID = "ACb8f2edb06564d5c27d01cfd9b6100883"
    AUTH_TOKEN = "2df6fc24e8550c6a431a6eda1318c496"
    tclient = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


    coords = data.strip().split(",")
    resp = sms_utility(coords[0], coords[1])

    wikiinfo = resp

    call = tclient.calls.create(url="http://b3afb221.ngrok.io/response", to=number, from_="+4915735984082")


    print("Received sms!!!")
    print(data)

    return str("Cool!")


if __name__ == "__main__":
    app.run(debug=True)