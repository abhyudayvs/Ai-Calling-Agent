import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
my_number = os.getenv('MY_PHONE_NUMBER')

ngrok_url = "https://shemeka-unchary-mirtha.ngrok-free.dev" 

client = Client(account_sid, auth_token)

print(f"Calling {my_number} from {twilio_number}...")

call = client.calls.create(
    to=my_number,
    from_=twilio_number,
    url=f"{ngrok_url}/start-call"
)

print(f"Call initiated! SID: {call.sid}")