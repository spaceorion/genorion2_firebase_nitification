from datetime import datetime
from myapp.serializers import *
from myapp.models import *
from myapp.serializers import *
import json


def pinschedule():
    dd = pinschedule.objects.filter(d_id = "khfy6767")
    for a in dd:
        print(a)
        now = datetime.now()
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        # second = '{:02d}'.format(now.second)
        day_month_year = '{}-{}-{}'.format(year, month, day)
        hour_minute_second = '{}:{}:00'.format(hour, minute)
        print(day_month_year)
        print(hour_minute_second)
        data1 = pinschedule.objects.all()
        data1Json = pinscheduleSerializers(data1, many=True)
        dataJson = pinscheduleTimeSerializers(data1, many=True)
        for data in data1Json.data:
            _date = data["date1"]
            _timing = data["timing1"]
            _id = data['id']
            var1 = data['pin1Status']
            var2 = data['pin2Status']
            var3 = data['pin3Status']
            var4 = data['pin4Status']
            var5 = data['pin5Status']
            var6 = data['pin6Status']
            var7 = data['pin7Status']
            var8 = data['pin8Status']
            var9 = data['pin9Status']
            var10 = data['pin10Status']
            var11 = data['pin11Status']
            var12 = data['pin12Status']
            var13 = data['pin13Status']
            var14 = data['pin14Status']
            var15 = data['pin15Status']
            var16 = data['pin16Status']
            d_idvar = data['d_id']
            print(var1)
            print(var2)
            print(_date)
            print(_timing)
            print("asdff",d_idvar)

            if _date<=day_month_year and _timing<=hour_minute_second:
                print("nono1")
                if pinschedule.objects.filter(id=_id):
                    print("nono2")
                    if (var1 != None):
                        print("nono3")
                        BASE_URL = f'https://127.0.0.1:8000/getpostdevicePinStatus/?d_id={d_idvar}'#'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id=DIDM12932021AAAAAA'
                        print("xxxxxxx1")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json',
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin1Status':var1}
                        print("xxx1")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var2 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx2")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin2Status':var2}
                        print("xxx2")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx2")
                        auth_response.text
                        print(auth_response)
                        print("delete")
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var3 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx3")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin3Status':var3}
                        print("xxx3")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx3")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var4 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx4")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin4Status':var4}
                        print("xxx4")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx4")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var5 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin5Status':var5}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var6 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin6Status':var6}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var7 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin7Status':var7}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var8 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin8Status':var8}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var9 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin9Status':var9}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var10 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin10Status':var10}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var11 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin11Status':var11}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var12 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin12Status':var12}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var13 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin13Status':var13}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var14 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin14Status':var14}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var15 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin15Status':var15}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
                    elif (var16 != None):
                        BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                        print("xxxxxxx")
                        token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                        headers =  {'content-type' : 'application/json', 
                                    'Authorization': "Token {}".format(token)}
                        data = {"put":"yes",'d_id':d_idvar,'pin16Status':var16}
                        print("xxx")
                        auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                        print("xxergadfgx")
                        auth_response.text
                        print(auth_response)
                        data2 = pinschedule.objects.filter(id=_id)
                        print("matched")
                        data2.delete()
                        print("delete")
            else:
                print("not matched")