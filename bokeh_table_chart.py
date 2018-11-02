import numpy as np
import pandas as pd

from datetime import date
from random import randint

from bokeh.core.properties import value
from bokeh.plotting import figure
from bokeh.transform import dodge

from bokeh.layouts import layout,column
from bokeh.models import CustomJS, Slider, ColumnDataSource, WidgetBox
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter

output_file('dashboard.html')

tools = 'pan,wheel_zoom,zoom_in,zoom_out,reset'
data = {}

def dataChart():
    global data
    listData = data
    ho = list(map(str, listData['roomNo']))
    Legacy_1 = list(map(str, listData['firstMethod']))
    Legacy_2 = list(map(str, listData['secondMethod']))
    Proposed = list(map(str, listData['proposed']))
    ElectroFee = list(map(str, listData['electroFee']))

    chartData = {'ho' : ho,
            'Legacy_1'   : Legacy_1,
            'Legacy_2'   : Legacy_2,
            'Proposed'   : Proposed,
            'ElectroFee'   : ElectroFee,}

    source = ColumnDataSource(chartData)

    p = figure(x_range=ho, y_range=(0, 4000), plot_height=350, title="Crossroad Apartment",
               toolbar_location="below", tools=tools)

    p.vbar(x=dodge('ho', -0.25, range=p.x_range), top='Legacy_1', width=0.2, source=source,
           color="#c9d9d3", legend=value("Legacy_1"))

    p.vbar(x=dodge('ho',  0.0,  range=p.x_range), top='Legacy_2', width=0.2, source=source,
           color="#718dbf", legend=value("Legacy_2"))

    p.vbar(x=dodge('ho',  0.25, range=p.x_range), top='Proposed', width=0.2, source=source,
           color="#e84d60", legend=value("Proposed"))

    p.line(x=ho, y = ElectroFee, color="red", line_width=2.5)

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.xaxis.axis_label = 'House'
    p.yaxis.axis_label = 'Fee Charged($)'

    return p

def dataTable():
    elecData = pd.read_csv('test1.csv')
    tableCount = len(elecData.index)
    global data
    data = dict(
        aptNo = [elecData['AprtNo'][i] for i in range(tableCount)],
        roomNo= [elecData['RoomNo'][i] for i in range(tableCount)],
        peopleNo = [elecData['PeopleNo'][i] for i in range(tableCount)],
        electroFee = [elecData['ElectroFee'][i] for i in range(tableCount)],
        useElectro = [elecData['UseElectro'][i] for i in range(tableCount)],
        firstMethod = [elecData['FirstMethod'][i] for i in range(tableCount)],
        secondMethod = [elecData['SecondMethod'][i] for i in range(tableCount)],
        proposed = [elecData['Proposed'][i] for i in range(tableCount)]
    )
    source = ColumnDataSource(data)
    
    template="""
                <div style="background:<%= 
                    (function colorfromint(){
                        if(firstMethod > secondMethod ){
                            return("green")}
                        }()) %>; 
                    color: <%= 
                        (function colorfromint(){
                            if(firstMethod > secondMethod){return('yellow')}
                            }()) %>;"> 
                    <%= value %>
                    </font>
                </div>
                """
    formatter =  HTMLTemplateFormatter(template=template)
    columns = [
        TableColumn(field="aptNo", title="AptNo"),
        TableColumn(field="roomNo", title="RoomNo"),
        TableColumn(field="peopleNo", title="PeopleNo"),
        TableColumn(field="electroFee", title="ElectroFee"),
        TableColumn(field="useElectro", title="UseElectro"),
        TableColumn(field="firstMethod", title="FirstMethod", formatter=formatter),
        TableColumn(field="secondMethod", title="SecondMethod", formatter=formatter),
        TableColumn(field="proposed", title="Proposed"),
        ]
    data_table = DataTable(source=source, columns=columns)
    

    return data_table

l = layout([
    column(dataTable(),
        dataChart()
    )
], sizing_mode='stretch_both')
show(l)