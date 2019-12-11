# -*- coding: UTF-8 -*-

#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from DAI import RunDevice,weather
import queue
import threading
import random
import time
import random, requests
import DAN

line_bot_api = LineBotApi('36IJiXrBpwOzcnzF1NBNWsRfj00i3ZiQpu3M+/ANnEyDAL5FJ/xs28d7w+oB5ysYrDudZzTzc5GuTLuDCYRz5UaTh1lTChLFUrHY8bVJL13B2KQ9pHx/ectbM4F3dgRJ80c86MIynaSDS7MDzjcJdAdB04t89/1O/w1cDnyilFU=') #LineBot's Channel access token
handler = WebhookHandler('43c246216e8f45424ae69ad6712f7b98')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)


def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))
    DAN.push('MSG-I',Msg)

    #Line_Temp=DAN.pull('MSG-O')
    #Line_Temp=str(Line_Temp)
    #Line_Temp=Line_Temp.replace("[","")
    #Line_Temp=Line_Temp.replace("]","")
    #Line_Temp=Line_Temp.replace("'","")

    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='hello')))   # Reply API example
    
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)


def Print(user_id_set):
    while True:
        try:
            Line_Temp=DAN.pull('MSG-O')
            print(Line_Temp)
            Line_Temp=str(Line_Temp)
            Line_Temp=Line_Temp.replace("[","")
            Line_Temp=Line_Temp.replace("]","")
            Line_Temp=Line_Temp.replace("'","")
            for userId in user_id_set:
                if Line_Temp != 'None':
                    line_bot_api.push_message(userId, TextSendMessage(text=Line_Temp))  # Push API example
            time.sleep(5)
        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)    
        
    
if __name__ == "__main__":
    
    ServerURL = 'https://6.iottalk.tw' #with SSL connection
    Reg_addr = 'qwgigfiwffuyfigffgfgf' #if None, Reg_addr = MAC address

    DAN.profile['dm_name']='M0858605'
    DAN.profile['df_list']=['MSG-I','MSG-O']

    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='再見'))  # Push API example
    except Exception as e:
        print(e)
    ##Thread
    t = threading.Thread(target=Print(user_id_set))
    t.daemon = True     # this ensures thread ends when main process ends
    t.start()
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

    

