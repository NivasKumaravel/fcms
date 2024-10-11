import requests
import json

def send_fcm_notification(fcm_token, title, message):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=YOUR_SERVER_KEY'  # Replace this with your actual server key from Firebase
    }
    payload = {
        'to': fcm_token,
        'notification': {
            'title': title,
            'body': message
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()
