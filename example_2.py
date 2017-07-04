# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask import request
import json
from options import Chart
from zabbix_api import ZabbixAPI
import datetime
from datetime import  timedelta
import time
from pprint import pprint
import json
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
app = Flask(__name__)



zapi = ZabbixAPI(config['url'])
zapi.login(config['auth']['user'], config['auth']['password'])

def dt(u):


    return datetime.datetime.fromtimestamp(int(u)).strftime('%H:%M')

@app.route("/update" , methods=['GET'])
def update_date():
    number=request.args['number']
    time_from = time.mktime((datetime.datetime.now() + timedelta(hours=-3)).timetuple())
    time_till = time.mktime(datetime.datetime.now().timetuple())

    saida = zapi.history.get({
    "itemids": [
    "35422"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })

    entrada = zapi.history.get({
    "itemids": [
    "35370"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })

    umidade = zapi.history.get({
    "itemids": [
    "36042"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })

    temp = zapi.history.get({
    "itemids": [
    "36041"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })

    if number == "1":
        chart = Chart() \
                 .legend(data=["Entrada", "Saida"]) \
                 .x_axis(formatter="{value}",data=[ dt(v['clock']) for v in saida]) \
                 .y_axis(formatter="{value} MB") \
                 .line("Entrada", [ int(int(v['value'])/1024/1024) for v in entrada], mark_max_point=True, show_item_label=True) \
                 .line("Saida", [ int(int(v['value'])/1024/1024) for v in saida], mark_max_point=True, show_item_label=True)

    elif  number == "2":
        chart = Chart() \
                 .legend(data=["Umidade", "Temperatura"]) \
                 .x_axis(formatter="{value}",data=[ dt(v['clock']) for v in umidade]) \
                 .y_axis(formatter="{value} C") \
                 .line("Umidade", [ int(v['value']) for v in umidade], mark_max_point=True, show_item_label=True) \
                 .line("Temperatura", [ int(v['value']) for v in temp], mark_max_point=True, show_item_label=True)



    return json.dumps( {"name" : number ,"type": "chart", "option": chart})

   # return render_template("main.html", **render)

@app.route("/")
def index():

    time_from = time.mktime((datetime.datetime.now() + timedelta(hours=-2)).timetuple())
    time_till = time.mktime(datetime.datetime.now().timetuple())

    saida = zapi.history.get({
    "itemids": [
    "35422"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })

    entrada = zapi.history.get({
    "itemids": [
    "35370"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })

    umidade = zapi.history.get({
    "itemids": [
    "36042"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })

    temp = zapi.history.get({
    "itemids": [
    "36041"
    ],
    "events": 0,
    "output": "extend",
    "time_from": time_from,
    "time_till": time_till
    })


    chart1 = Chart() \
             .legend(data=["Entrada", "Saida"]) \
             .x_axis(formatter="{value}",data=[ dt(v['clock']) for v in saida]) \
             .y_axis(formatter="{value} MB") \
             .line("Entrada", [ int(int(v['value'])/1024/1024) for v in entrada], mark_max_point=True, show_item_label=True) \
             .line("Saida", [ int(int(v['value'])/1024/1024) for v in saida], mark_max_point=True, show_item_label=True)

    chart2 = Chart() \
             .legend(data=["Umidade", "Temperatura"]) \
             .x_axis(formatter="{value}",data=[ dt(v['clock']) for v in umidade]) \
             .y_axis(formatter="{value} C") \
             .line("Umidade", [ int(v['value']) for v in umidade], mark_max_point=True, show_item_label=True) \
             .line("Temperatura", [ int(v['value']) for v in temp], mark_max_point=True, show_item_label=True)


    #print (json.dumps(chart, indent=2))

    render = {
        "title": "Dashboard",
        "templates": [

                        {"type": "chart", "option": json.dumps(chart1, indent=2)},
                        {"type": "chart", "option": json.dumps(chart2, indent=2)}
        ]
    }
    return render_template("zabbix.html", **render)




if __name__ == "__main__":

    app.run(debug=True,host="0.0.0.0",port=8080)
