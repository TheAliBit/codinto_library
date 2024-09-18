from melipayamak import Api
from decouple import config


def send_sms(number, message):
    username = config('SMS_USERNAME')
    password = config('SMS_PASSWORD')
    api = Api(username, password)
    sms = api.sms()

    _from = config('SMS_HOST')
    to = number
    text = message

    try:
        response = sms.send(to, _from, text)
        return response
    except Exception as e:
        return str(e)
