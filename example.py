# -*- coding:utf-8 -*-
# py-echarts
from flask import Flask, render_template
import json
from models import Chart

app = Flask(__name__)

@app.route("/")
def index():
    chart1 = Chart().pie("torta", data={
            u"camisa": 100,
            u"suéter": 360,
            u"camisa de chiffon": 120,
            u"calças": 500,
            u"Sapatos de salto alto": 300
        })
    chart2 = Chart() \
             .legend(data=[u"temperatura mais alta", u"temperatura mínima"]) \
             .x_axis(data=[u"segunda-feira", u"terça-feira", u"quarta-feira", u"quinta-feira", u"sexta-feira", u"sábado", u"domingo"]) \
             .y_axis(formatter="{value} C") \
             .line(u"temperatura mais alta", [10, 20, 30, 40, 30, 20, 10], mark_max_point=True, show_item_label=True) \
             .bar(u"temperatura mínima", [5, 10, 5, 10, 5, 6, 7]) \
             .pie(name="teste", data={"Java": 50, "PHP": 50, "Python": 100}, center=["20%", "30%"], radius="15%")


    print json.dumps(chart2, indent=2)

    render = {
        "title": u"teste de título",
        "templates": [
            {"type": "radio"},
            {"type": "table"},
            {"type": "chart", "option": json.dumps(chart1, indent=2)},
            {"type": "chart", "option": json.dumps(chart2, indent=2)}
        ]
    }
    return render_template("main.html", **render)



@app.route("/update")
def update():
    chart1 = Chart().pie("torta", data={
            u"camisa": 100,
            u"suéter": 360,
            u"camisa de chiffon": 120,
            u"calças": 500,
            u"Sapatos de salto alto": 300
        })
    chart2 = Chart() \
             .legend(data=[u"temperatura mais alta", u"temperatura mínima"]) \
             .x_axis(data=[u"segunda-feira", u"terça-feira", u"quarta-feira", u"quinta-feira", u"sexta-feira", u"sábado", u"domingo"]) \
             .y_axis(formatter="{value} C") \
             .line(u"temperatura mais alta", [10, 20, 30, 40, 30, 20, 10], mark_max_point=True, show_item_label=True) \
             .bar(u"temperatura mínima", [5, 10, 5, 10, 5, 6, 7]) \
             .pie(name="teste", data={"Java": 50, "PHP": 50, "Python": 100}, center=["20%", "30%"], radius="15%")


    print json.dumps(chart2, indent=2)

    render = {
        "title": u"teste de título",
        "templates": [
            {"type": "radio"},
            {"type": "table"},
            {"type": "chart", "option": json.dumps(chart1, indent=2)},
            {"type": "chart", "option": json.dumps(chart2, indent=2)}
        ]
    }
    return render_template("main.html", **render)



if __name__ == "__main__":

    app.run(debug=True,host="0.0.0.0",port=8080)
