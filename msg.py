from twilio.rest import Client

def sendMessage(clientNumber):
    account_sid = 'AC722fba748e992463888ef58dd6bf2216'
    auth_token = '8970619b03e7cfbf1430bcb81bff73a9'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Imma take your momma to the Marriot and wear it out.",
                        from_='+19478004230',
                        to='+' + clientNumber
                    )

    print(message.sid)  

######################################

clientNumber = '13137278191'

# print('+' + clientNumber)

sendMessage(clientNumber)