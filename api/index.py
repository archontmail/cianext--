from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from time import time
import httpx
import asyncio
import json
import imaplib
import email
from email.header import decode_header
import base64
import re

app = FastAPI()
url = 'https://mdevelopeur.retailcrm.ru/api/v5/orders'
apikey = 'nHY0H7zd7UWwcEiwN0EbwhXz2eGY9o9G'
hook = 'https://hook.eu2.make.com/qk5rqffp5iphdj0k5v7dbqvr3v5jp3kg'
hostName = "localhost"
serverPort = 8080

headers = {
  'Accept' : 'application/json',
  'Content-Type': 'application/json',
  'X-API-KEY' : apikey
}

password = "zrAUqnFWgD14Ygkq13VK"
username = "kworktestbox@mail.ru"
imap_server = "imap.mail.ru"

async def check_mail(client):
    print('checking started')
    list = await client.get(orderlist)
    print(list)
    try: 
        print('trying to post')
        response = await client.post(retailCRM, data={'order': '{"lastName":"ghhv@mail.ru"}'})
    except Exception as e:
        print(repr(e))
    print(response.content)
    return response.content
    imap = imaplib.IMAP4_SSL(imap_server)
    print(imap)
    print(imap.login(username, password))
    imap.select("INBOX")
    result, data = imap.uid('search', None, "UNSEEN")
    if result == 'OK':
        #payload = { order: '"lastName":"ghhv@mail.ru"}'}
        #response = await client.post(retailCRM, payload)
        
        #data = json.dumps(data)
        
        print('OK', data)
        for num in data[0].split():
            print(num)
            result, data = imap.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][1])
                print('From:' + email_message['From'])
                print('To:' + email_message['To'])
                print('Date:' + email_message['Date'])
                print('Subject:' + str(email_message['Subject']))
                response = await client.post(retailCRM, payload)
                
                print(response)
                return response
    return None
  
async def task(data, type, lead, start):
    async with httpx.AsyncClient() as client:
        tasks = [check_mail(client) for i in range(1)]
        result = await asyncio.gather(*tasks)
        return result

@app.get('/api')
async def main():
    #start = time()
    output = await task()
    #print("time: ", time() - start)
    return output
