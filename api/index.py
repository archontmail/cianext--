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
#from bs4 import BeautifulSoup
import re

app = FastAPI()
orderlist = 'https://mdevelopeur.retailcrm.ru/api/v5/orders?apiKey=nHY0H7zd7UWwcEiwN0EbwhXz2eGY9o9G'
retailCRM = 'https://mdevelopeur.retailcrm.ru/api/v5/orders/create?apiKey=nHY0H7zd7UWwcEiwN0EbwhXz2eGY9o9G'
apikey = 'X-API-KEY
hook = 'https://hook.eu2.make.com/qk5rqffp5iphdj0k5v7dbqvr3v5jp3kg'
hostName = "localhost"
serverPort = 8080
#url = 'https://b24-002xma.bitrix24.ru/rest/1/ofz3113rxnyv8qfv/'

url = 'https://b24-mhfw1p.bitrix24.ru/rest/1/etnwm06bccntmdyo/'

headers = {
  'Accept' : 'application/json',
  'Content-Type': 'application/json'
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
  
# Глобальная переменная для pipeline_id
pipeline_id = 8412118

class Lead(BaseModel):
    name: str | None = None
    user_id: int | None = None
    address: str | None = None
    price: int | None = None  # Убедитесь, что price — это целое число
    phone: str | None = None
    link: str | None = None
    seller: str | None = None
    lead_id: int | None = None
    action: str | None = None

async def get_body(request: Request):
    return await request.json()

async def task(data, type, lead, start):
    async with httpx.AsyncClient() as client:
        if data and data.lead_id:
            tasks = [patch_lead(client, data)]
        elif data:
            tasks = [post_lead(client, data) for i in range(1)]
        elif type == 'users':
            tasks = [get_users(client) for i in range(1)]
        elif type == 'leads':
            tasks = [get_leads(client, start) for i in range(1)]
        elif type == 'filter':
            tasks = [check_mail(client) for i in range(1)]
        result = await asyncio.gather(*tasks)
        return result

@app.post('/api')
async def handle_request(request: Request):
    data = await request.json()
    lead = Lead(**data)
    start = time()
    output = await task(lead, None, None, None)
    print("time: ", time() - start)
    return output

@app.get('/api')
async def users(type: str | None = None, lead: str | None = None, start: str | None = None):
    #start = time()
    output = await task(None, type, lead, start)
    #print("time: ", time() - start)
    return output
