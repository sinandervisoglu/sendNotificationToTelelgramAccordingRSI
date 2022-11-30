import requests

def telegramBotSendText(botMessage,id):
    botToken="botToken" #BotFather'!
    url="https://api.telegram.org/bot"+botToken+"/sendMessage?chat_id="+str(id)+"&parse_mode=Markdown&text="+botMessage
    response=requests.get(url)
    return response.json()
