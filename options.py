# -*- coding: utf-8 -*-

import json
import functools

class Chart(dict):
    """
    modelo de gráfico
    """
    def __init__(self):
        super(Chart, self).__init__()
        self["calculable"] = True
        self["tooltip"] = {"show": True}
        self["toolbox"] = {
            "show": True,
            "x": "left",
            'feature': dict(mark = dict(show=1),
           dataView = dict(show= 1, readOnly= 0, title='Dados',
                lang=['Dados','voltar','atualizar']),
           magicType = dict(show= 1, type= ['line', 'bar'],
           title=dict(
	            line= 'linha',
	            bar= 'barra',
	            stack= 'pilha',
	            tiled='telha'
	        )),
            dataZoom = dict(
                    show = 1,
                    title = dict(
                        back= "Voltar",
                        zoom='zoom'
                    )
                ),
            restore = dict(show= 1,title='atualizar'),
            saveAsImage = dict(show= 1,title='salvar'))
        }
        self["legend"] = {
            "show": True,
            "data": []
        }
        self["series"] = []

    def title(self, x="center", **kwargs):
        """
        Defina o título do gráfico
        """
        self["title"].update({
            "x": x
        })
        self["title"].update(kwargs)
        return self

    def tooltip(self, show=True, trigger='axis', formatter=None, **kwargs):
        """
        mensagem de configuração
        """
        self["tooltip"].update({
            "show": show,
            "trigger": trigger
        })
        if formatter is not None:
            self["tooltip"].update({"formatter": formatter})
        self["tooltip"].update(kwargs)
        return self

    def legend(self, show=True, data=None, orient='horizontal', **kwargs):
        """
        legenda
        `data`: [" legenda 1", "legenda2", " legenda 3"]
        `orient`: "vertical"|"horizontal"
        """
        data = [] if data is None else data
        self["legend"].update({
            "show": show,
            "data": data,
            "orient": orient
        })
        self["legend"].update(kwargs)
        return self

    def toolbox(self, show=True, x='left', **kwargs):
        """
        Configurar Toolbox
        """
        self["toolbox"].update({
            "show": show,
            "x": x
        })
        self["toolbox"].update(kwargs)
        return self

    def pie(self, name, data=None, radius="55%", center=None, auto_legend=True, **kwargs):
        """
        Adicionar um gráfico de pizza
        `data`: { "nome": 100}, "nome2": 200}
        """
        center = ["50%", "60%"] if center is None else center
        data = {} if data is None else data
        self["series"].append(self.__merge_dict({
            "type": "pie",
            "name": name,
            "radius": radius,
            "center": center,
            "data": [{"name": n, "value": v} for n, v in data.items()]
        }, kwargs))
        if auto_legend:
            legend_data = self["legend"]["data"]
            [legend_data.append(x) for x in data if x not in legend_data]
        return self

    def bar(self, name, data=None, auto_legend=True, y_axis_index=0, **kwargs):
        """
        Adiciona um Barra
        `data`: [10, 20, 30, 40]
        `auto_legend`: geração automática de legenda
        """
        data = [] if data is None else data
        self["series"].append(self.__merge_dict({
            "type": "bar",
            "name": name,
            "data": data,
            "yAxisIndex": y_axis_index
        }, kwargs))
        if "yAxis" not in self:
            self.y_axis()
        if name not in self["legend"]["data"] and auto_legend:
            self["legend"]["data"].append(name)
        return self

    def line(self, name, data=None, mark_max_point=False, mark_min_point=False, show_item_label=False, auto_legend=True, y_axis_index=0, **kwargs):
        """
        Adicionar um gráfico de linhas
        `data`: [10, 20, 30, 40]
        """
        data = [] if data is None else data
        mark_point = []
        if mark_max_point:
            mark_point.append({"type": "max", "name": "Max"})
        if mark_min_point:
            mark_point.append({"type": "min", "name": "min"})
        self["series"].append(self.__merge_dict({
            "type": "line",
            "name": name,
            "data": data,
            "markPoint": {
                "data":mark_point
            },
            "itemStyle": {
                "normal": {
                    "label": {"show": show_item_label}
                }
            },
            "yAxisIndex": y_axis_index
        }, kwargs))
        if "yAxis" not in self:
            self.y_axis()
        if name not in self["legend"]["data"] and auto_legend:
            self["legend"]["data"].append(name)
        return self

    def x_axis(self, data=None, type_="category", name="", **kwargs):
        """
        Adicionar eixo x
        """
        data = [] if data is None else data
        if "xAxis" not in self:
            self["xAxis"] = []
        self["xAxis"].append(self.__merge_dict({
            "type": type_,
            "name": name,
            "data": data
        }, kwargs))
        return self

    def y_axis(self, data=None, type_="value", name="", formatter=None, **kwargs):
        """
        Adicionar eixo y
        """
        if "yAxis" not in self:
            self["yAxis"] = []
        self["yAxis"].append(self.__merge_dict({
            "type": type_,
            "name": name,
        }, {"axisLabel": {"formatter": formatter}} if formatter is not None else {}, kwargs))
        if data is not None:
            self["yAxis"] = data
        return self

    @staticmethod
    def __merge_dict(*args):
        """
        Mesclar vários dicionários e retornos
        """
        reduce = functools.reduce
        return reduce(lambda x, y: dict(list(x.items()) + list(y.items())), args)


def main():
    c = Chart().tooltip()
   # print (json.dumps(c))

if __name__ == "__main__":
    main()
