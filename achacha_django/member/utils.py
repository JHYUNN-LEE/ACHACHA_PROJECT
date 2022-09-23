import hashlib
import hmac
import base64

def make_signature(timestamp):
    access_key = 'D3HFVghtWIESI6SSXmlE' 
    secret_key = 'R3e0ANNSxEQy3Sx3a15OVzOCgUj65B9jJ2aecV8Z' 

    secret_key = bytes(secret_key, 'UTF-8')

    uri = "/sms/v2/services/ncp:sms:kr:292968693103:achacha_auth/messages"
    
    message = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

