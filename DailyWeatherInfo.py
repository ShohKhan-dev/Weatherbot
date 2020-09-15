import requests
import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
import time
import schedule

harorat = arr = []
today = main_info = None

def Data():

    global harorat, arr, today, main_info
    
    URL = "https://obhavo.uz/andijan"
    page = urllib.request.urlopen(URL)
    soup = BeautifulSoup(page, 'html.parser')

    main = soup.find('div', class_ = "padd-block")


    for item in main.find('div', class_ = "current-day"):
        today = item
        
    tempra = main.find('div', class_ = "current-forecast")
    
    for span in tempra.find_all('span', recursive=False):
        for it in span:
            if it != '\n':
                harorat.append(it)


    for hah in main.find('div', class_ = "current-forecast-desc"):
        main_info = hah

    arr = []
    for deta in main.find('div', class_ = "current-forecast-details"):
        for ikir in deta:
            for d in ikir:
                if d != '\n':
                    arr.append(d)



def msg_send():
    token = "<Your bot token>"
    chat_id = 'your ID'

    Data()
    

    rasm = harorat[0].get('src')
    minimum = harorat[2]
    for it in harorat[1]:
        maximum = it

    details = '\n'.join(arr)
    

    text = today + "\nKunduzi: " + maximum + " Kechasi: " + minimum + '\n' + main_info + "\n\nBATAFSIL:\n"  + details
    
    
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage"+"?chat_id=" + chat_id + "&text="+ text
    results = requests.get(url_req)
    return results.json()


#schedule.every(1).minutes.do(msg_send)  ## you can test with this
schedule.every().day.at("07:00").do(msg_send)
schedule.every().day.at("12:00").do(msg_send)


while True:
    schedule.run_pending()
    time.sleep(1)
