from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from myapp.views import *
import schedule
from django.shortcuts import render
import time
import urllib

# print("in")


def start():
    print("in")
    def f():
        while True:
            schedule.run_pending()
    import threading
    threading.Thread(target=f).start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(ready)
    scheduler.start()


def ready():
    # from myapp import updater
    # updater.start()
    print("I am running in 2 second: ")
    
    # from selenium import webdriver
    
    x = "genorion1.herokuapp.com"
    refreshrate = 2
    refreshrate = int(refreshrate)
    # driver = webdriver.Firefox()
    get = ("http://"+x)

    while True:
        time.sleep(refreshrate)
        get.refresh()
schedule.every(2).seconds.do(ready)

# def ready():
#     # from myapp import updater
#     # updater.start()
#     print("I am running in 2 second: ")

# schedule.every(2).seconds.do(ready)
# # schedule.every(1).seconds.do(MyappConfig)
    # time.sleep(1)
