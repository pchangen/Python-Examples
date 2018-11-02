#!/usr/bin/env python
# coding: utf-8

# 예제 내용
# * QWebEngineView를 이용한 웹 위젯 사용

import sys

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly
import urllib

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QBoxLayout

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

__author__ = "Deokyu Lim <hong18s@gmail.com>"


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.form_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        self.setLayout(self.form_layout)
        self.init_widget()
        

    def init_widget(self):
        self.setWindowTitle("QWebEngineView")
        # QWebEngineView 를 이용하여 웹 페이지를 표출

        plotly.tools.set_credentials_file(username='LDH', api_key='UMzOKvaMsNeDuUSyK7eF')

        url = "https://raw.githubusercontent.com/plotly/datasets/master/spectral.csv"
        f = urllib.request.urlopen(url)
        spectra=np.loadtxt(f, delimiter=',')

        traces = []
        y_raw = spectra[:, 0] # wavelength
        sample_size = spectra.shape[1]-1 
        for i in range(1, sample_size):
            z_raw = spectra[:, i]
            x = []
            y = []
            z = []
            ci = int(255/sample_size*i) # ci = "color index"
            for j in range(0, len(z_raw)):
                z.append([z_raw[j], z_raw[j]])
                y.append([y_raw[j], y_raw[j]])
                x.append([i*2, i*2+1])
            traces.append(dict(
                z=z,
                x=x,
                y=y,
                colorscale=[ [i, 'rgb(%d,%d,255)'%(ci, ci)] for i in np.arange(0,1.1,0.1) ],
                showscale=False,
                type='surface',
            ))

        fig = { 'data':traces, 'layout':{'title':'Ribbon Plot'} }
        url = py.iplot(fig, filename='ribbon-plot-python')
        web = QWebEngineView()
        web.setUrl(QUrl(url.resource))
        self.form_layout.addWidget(web)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())