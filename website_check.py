'''
Vk оповещение о падении сайта
by ArtAnichkin
2021
Реализовано: отслеживание доступности сайта с помощью icmp протокола
На случай если icmp трафик отключен реализована проверка GET-запроом
При фиксации падения/старта сервера отправляестя сообщение в вк с соответствующим статусом и небольшой сводкой
Отправка сообщения реализуется по Vk API через бота на личную страницу
'''

import time
import vk_api
import requests
from icmplib import ping
from random import randint

url = 'https://sci-hub.ru/' #адрес сайта  
token = 'token'  #token группы вк, которая будет отправлять сообщение  
vk_user_id = 'vk_id'  #id vk куда будет отправляться сообщение  

time_sleep = 60 * 5 #интервал проверки доступности в секундах


vk = vk_api.VkApi(token = token)

def write_vk_msg(vk_user_id, message):
    vk.method('messages.send', {
        'user_id' : vk_user_id,
        'message'  : message,
        'random_id': randint(0, 10**8)
        })

def url_ok(url):
    r = requests.get(url)
    return r.status_code == 200

def icmp_ok(url):
    n = url.index('/') + 2
    return ping(url[n:]).is_alive

def dead():
    vk_message = f'Сайт не доступен \n{time.asctime()}'
    write_vk_msg(vk_user_id, vk_message)

def main():
    flag = False
    while True:
        try:
            time.sleep(time_sleep)
            if not icmp_ok(url) and not flag:
                if url_ok(url):
                    continue
                flag = True
                dead()

            elif (icmp_ok(url) or url_ok(url)) and flag:
                flag = False
                vk_message = f'Сайт снова доступен \n{time.asctime()}'
                write_vk_msg(vk_user_id, vk_message)

        except requests.exceptions.ConnectionError:
            if not flag:
                flag = True 
                dead()


if __name__ == "__main__":
    main()