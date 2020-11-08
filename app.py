# FLASK CHAT APP SALESFORCE LIVEAGENT API
import requests
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def home():
    session_id, affinity_token, key = getSessionId()
    print(session_id)
    getChasitorInit(session_id, affinity_token, key)
    sendChatMessage(session_id, affinity_token, key)
    getMessages(session_id, affinity_token, key)
    return render_template('index.html')


def getSessionId():
    url = "https://d.la2-c2-ukb.salesforceliveagent.com/chat/rest/System/SessionId"

    payload = {}
    headers = {
        'X-LIVEAGENT-AFFINITY': 'null',
        'X-LIVEAGENT-API-VERSION': '50',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = response.json()
    session_id = response_dict['id']
    affinity_token = response_dict['affinityToken']
    key = response_dict['key']
    return session_id, affinity_token, key


def getChasitorInit(session_id, affinity_token, key):
    url = "https://d.la2-c2-ukb.salesforceliveagent.com/chat/rest/Chasitor/ChasitorInit"

    payload = "{\n  \"sessionId\": \""+session_id+"\",\n  \"organizationId\": \"00D2w000000kcVU\",\n  \"deploymentId\": \"5722w000000UL5h\",\n  \"buttonId\": \"5732w000000UO2n\",\n  \"userAgent\": \"\",\n  \"language\": \"en-US\",\n  \"screenResolution\": \"1900x1080\",\n  \"visitorName\": \"Test Visitor\",\n  \"prechatDetails\": [],\n  \"prechatEntities\": [],\n  \"receiveQueueUpdates\": true,\n  \"isPost\": true\n}"

    headers = {
        'X-LIVEAGENT-AFFINITY': affinity_token,
        'X-LIVEAGENT-API-VERSION': '50',
        'X-LIVEAGENT-SESSION-KEY': key,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("getChasitorInit")
    print(response.status_code)


def getMessages(session_id, affinity_token, key):
    while True:
        url = "https://d.la2-c2-ukb.salesforceliveagent.com/chat/rest/System/Messages"
        payload = {}
        headers = {
            'X-LIVEAGENT-AFFINITY': affinity_token,
            'X-LIVEAGENT-API-VERSION': '50',
            'X-LIVEAGENT-SESSION-KEY': key,

        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print("getMessages")
        print(response.status_code)
        if response.status_code == 200:
            print(response.json())
        else:
            print('204 empty resp')


def sendChatMessage(session_id, affinity_token, key):
    url = "https://d.la2-c2-ukb.salesforceliveagent.com/chat/rest/Chasitor/ChatMessage"
    payload = "{\n\"text\": \"I have a question about my account.\"\n}"

    headers = {
        'X-LIVEAGENT-AFFINITY': affinity_token,
        'X-LIVEAGENT-API-VERSION': '50',
        'X-LIVEAGENT-SESSION-KEY': key,

    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("getChatMessage")
    print(response.reason)


if __name__ == "__main__":
    app.run()

# Endpoint https://d.la2-c2-ukb.salesforceliveagent.com/chat/rest/
