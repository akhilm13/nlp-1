import json
import requests
import time
import urllib
import os
import mysql.connector
import subject_extraction as sub


TOKEN = "589997916:AAGUxpZOou9AY1SC1WicB94dGXKzr0NjQxg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        print(text)
        if (text == "/start"):
               print('Started')
        elif (text.startswith( 'tag' ) or text.startswith( 'Tag' )):
               #THIS TAG text.split()[1] should be used to query the database and return a list of artciles
               #REMOVE THIS LINE BELOW AND CODE TO CONNECT TO DATABASE. SEND THE RESULT USING SEND_MESSAGE
               res = get_articles_by_tag(text.split()[1]);
               for a in res:
                   for b in a:
                       send_message("Articles stuff: "+b, chat);
               return
        else:
               value = sub.get_subject(text)
               send_message(" Article added under "+value[0], chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def get_articles_by_tag(tag): #returns the list of articles corresponding to the tags
    res = []
    cnx = mysql.connector.connect(user='user', host='127.0.0.1', password="", database='db', port=3306)
    cursor = cnx.cursor()
    cursor.execute("select title,content,link from linked_view where tag = '"+tag+"';")
    for (title, content, link) in cursor:
        res.append([title, content, link])
    cnx.commit()
    #cnx.close()
    return res

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
	main()
