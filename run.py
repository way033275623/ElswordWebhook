import requests
from bs4 import BeautifulSoup
import time
import googletrans
import logging

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO , format='%(asctime)s %(message)s')

translator = googletrans.Translator()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
webhookAddress = "https://discordapp.com/api/webhooks/997084652185600051/sLIR_R64n3lW7UKu4UJSYejEYhleTsANw3C31K_bo5E70tDNK_ucSvfgbGhqvRfgVuru"
oldarticle=[]

firstrun=True
logging.info('Start')

def webhook(message):
    titlech = translator.translate(message['title'], dest='zh-tw').text
    content = titlech + '\n' + message['link']
    json = {'username': '韓服公告','content':content}
    requests.post(webhookAddress,json=json)
    logging.info(titlech)

while(1):
    try:
        response = requests.get("https://elsword.nexon.com/News/Notice/List" ,headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        with open('file.html', 'w') as file:
            file.write(response.text)

        board_list = soup.find(class_="board_list")
        titles = board_list.find_all("li")
        data=[]

        for title in titles:
            temp={}
            temp['type']=str(title.find("strong").getText())
            temp['title']=str(title.select_one(".subject").getText())
            temp['link']=str(title.select_one("a")['href'])
            data.append(temp)

        if(len(oldarticle)>0):
        
            for x in data:
                if(x['link'] not in oldarticle):
                    webhook(x)

            time.sleep(60)

            
        else:
            for x in data:
                #webhook(x)
                oldarticle.append(x['link'])
    except Exception as e:
        logging.error(e)
        time.sleep(60)

