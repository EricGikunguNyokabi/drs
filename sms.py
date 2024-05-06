import africastalking # pip install africastalking # https://africastalking.com/

# africastalking.initialize(username="ericnyokabi", api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a")
africastalking.initialize(username="DRS", api_key="8e109d02d94c78fb9da72cb0d3cc1972c7853565230fd9e06dcc700f9d3eec7d")


sms = africastalking.SMS
def send_sms( phone, message):
    recipients = [phone]
    sender = "AFRICASTKNG"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as error:
        print(error)


# send_sms("+254706758430","Your Document was Retrieved Successfully, Login to get more info at, https://egn.pythonanywhere.com/")