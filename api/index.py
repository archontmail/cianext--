from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from time import time
import httpx
import asyncio
import json
import imaplib
import email
from imap_tools import MailBox, AND
from email.header import decode_header
import base64
import re
import retailcrm

app = FastAPI()
url = 'https://mdevelopeur.retailcrm.ru/api/v5/'
apikey = 'nHY0H7zd7UWwcEiwN0EbwhXz2eGY9o9G'
hook = 'https://hook.eu2.make.com/qk5rqffp5iphdj0k5v7dbqvr3v5jp3kg'
hostName = "localhost"
serverPort = 8080

headers = {
  'X-API-KEY' : apikey
}

password = "zrAUqnFWgD14Ygkq13VK"
username = "kworktestbox@mail.ru"
imap_server = "imap.mail.ru"

async def main(client):
    messages = await get_mail(username, password, imap_server)
    for msg in messages : 
        result = await post_order(client, msg.first_name, msg.last_name, msg.email, msg.text, msg.html, msg.attchments)
        return result    

async def post_order(client, first_name, last_name, email, subject, text, html, attachments):
    print('posting...')
    result = await client.post(url + 'files/upload', data = attachments[0].payload, headers = headers)
    print('result': result)
    return result 
async def get_mail(username, password, imap_server):
    array = []
    print('connecting to imap server...')
    with MailBox(imap_server).login(username, password) as mailbox:
        print('fetching...')
        for msg in mailbox.fetch(AND(seen=False)):
            attachments = []
            for a in msg.attachments:
                print(a.filename)
                #print(a.payload)
                attachments.append(a)
            print(len(attachments))
            name = re.search('(.*) <' + msg.from_ + '>', msg.from_values.full).group(1).split(' ')
            print(name)
            lastName = name[-1]
            name.pop(-1)
            firstName = ' '.join(name)
            print(firstName, lastName)
            data = {"email": msg.from_, "first_name": firstName, "last_name": lastName, "subject": msg.subject, "text": msg.text, "html": msg.html, "attachments": attachments}
            print(data["email"])
            print(msg.date, msg.from_, msg.subject, msg.from_values,name, len(msg.text or msg.html))
            array.append(data)
        return array

async def task():
    async with httpx.AsyncClient() as client:
        tasks = [main(client) for i in range(1)]
        result = await asyncio.gather(*tasks)
        return result

@app.get('/api')
async def api():
    #start = time()
    output = await task()
    #print("time: ", time() - start)
    return output
