import stripe
import os
import hashlib
import time, requests

stripe.api_key = os.getenv('Stripe_TEST_KEY')
CAPI_access_token = os.getenv('CAPI_ACCESS_TOKEN')
pixel_id = os.getenv('PIXEL_ID', 3459339171001375)


def get_billing_data():
    data = stripe.Charge.list(limit=1)["data"]

    email = data[0]["billing_details"]["email"]
    hashed_email = hash(email)
    id = data[0]["id"]

    send_conversion_api(hashed_email, id)

def send_conversion_api(email, event_id):
    url = 'https://graph.facebook.com/v16.0/{PIXEL_ID}/events?access_token={TOKEN}'.format(PIXEL_ID = pixel_id, TOKEN = CAPI_access_token)

    obj = {
        "data": [
            {
                "event_name": "Purchase",
                "event_time": int(time.time()),
                "event_id": event_id,
                "action_source": "website",
                "user_data": {
                    "em": [
                        email
                    ],
                },
                "custom_data": {
                    "currency": "SGD",
                    "value": "11.0"
                }
            }
        ],
    }
    x = requests.post(url, json = obj)

def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()
