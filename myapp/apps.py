from django.apps import AppConfig
import schedule
import time




class MyappConfig(AppConfig):
    name = 'myapp'


    # def ready(self):
    #     if 'runserver' not in sys.argv:
    #         return True
    #     # you must import your modules here 
    #     # to avoid AppRegistryNotReady exception 
    #     from .models import MyModel


# time.sleep(5)

    # def ready(self):
    #     from myapp import updater
    #     updater.start()
    
