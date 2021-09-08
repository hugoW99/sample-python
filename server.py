import io
import time
import threading
import random

import remi.gui as gui
from remi import start, App

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

import sys

from matplotlib import rc
import matplotlib.ticker
from matplotlib.font_manager import FontProperties

import mysql.connector as mysql
from mysql.connector import Error

import matplotlib.dates as md
import numpy as np
import pandas as pd
import datetime as dt
import time

from tkscrolledframe import ScrolledFrame
from tkcalendar import Calendar

from datetime import date


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)
    
    #def idle(self):
    #    self.counter.set_text('Running Time: ' + str(self.count))
    #    self.progress.set_value(self.count%100)
    
    def main(self):
        mainContainer = gui.Container(width='100%', margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        welcomeContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        averagedContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        
        self.img = gui.Image("c:\\users\\hugo whelan\\desktop\\python\\MOS_Logo_HQ.jpg", height=100, margin='10px')
        self.title_lbl = gui.Label('Douglas Park Bridges Monitoring System Data', width='100%', height=30, margin='10px')
        
        self.welcome_lbl = gui.Label('Welcome to the Douglas Park Bridges Monitoring System Database. The page contains daily averaged data and diagnostic information. Full data overviews are shown at the bottom of the page.', width='100%', height=30, margin='10px')
        
        welcomeContainer.append([self.img, self.title_lbl, self.welcome_lbl])
        
        # Average data
        self.lbl_avg = gui.Label('Averagd Data', width='100%', height=30, margin='10px')
        self.avg_txt = gui.Label('The following section contains the daily averaged data. Please select the dates and sensor(s) you would like to access. All data is relative to time. If you want the unaveraged data, please scroll down to the second section.', width='100%', height=30, margin='10px')
        
        self.start_date = gui.Date(width=200, height=20)
        self.end_date = gui.Date(width=200, height=20)
        
        self.check_s_nb_s2w = gui.CheckBoxLabel('S_NB_S2W', False, width=200, height=30)
        self.check_s_nb_s2e = gui.CheckBoxLabel('S_NB_S2E', False, width=200, height=30)
        self.check_s_nb_s1e = gui.CheckBoxLabel('S_NB_S1E', False, width=200, height=30)
        self.check_s_nb_s1w = gui.CheckBoxLabel('S_NB_S1W', False, width=200, height=30)
        self.check_t_nb_s2w = gui.CheckBoxLabel('T_NB_S2W', False, width=200, height=30)
        self.check_t_nb_s2e = gui.CheckBoxLabel('T_NB_S2E', False, width=200, height=30)
        self.check_t_nb_s1e = gui.CheckBoxLabel('T_NB_S1E', False, width=200, height=30)
        self.check_t_nb_s1w = gui.CheckBoxLabel('T_NB_S1W', False, width=200, height=30)
        self.check_tp_nb_s2w = gui.CheckBoxLabel('TP_NB_S2W', False, width=200, height=30)
        self.check_tp_nb_s2e = gui.CheckBoxLabel('TP_NB_S2E', False, width=200, height=30)
        self.check_tp_nb_s1e = gui.CheckBoxLabel('TP_NB_S1E', False, width=200, height=30)
        self.check_tp_nb_s1w = gui.CheckBoxLabel('TP_NB_S1W', False, width=200, height=30)
        
        self.check_s_sb_s2w = gui.CheckBoxLabel('S_SB_S2W', False, width=200, height=30)
        self.check_s_sb_s2e = gui.CheckBoxLabel('S_SB_S2E', False, width=200, height=30)
        self.check_s_sb_s1e = gui.CheckBoxLabel('S_SB_S1E', False, width=200, height=30)
        self.check_s_sb_s1w = gui.CheckBoxLabel('S_SB_S1W', False, width=200, height=30)
        self.check_t_sb_s2w = gui.CheckBoxLabel('T_SB_S2W', False, width=200, height=30)
        self.check_t_sb_s2e = gui.CheckBoxLabel('T_SB_S2E', False, width=200, height=30)
        self.check_t_sb_s1e = gui.CheckBoxLabel('T_SB_S1E', False, width=200, height=30)
        self.check_t_sb_s1w = gui.CheckBoxLabel('T_SB_S1W', False, width=200, height=30)
        self.check_tp_sb_s2w = gui.CheckBoxLabel('TP_SB_S2W', False, width=200, height=30)
        self.check_tp_sb_s2e = gui.CheckBoxLabel('TP_SB_S2E', False, width=200, height=30)
        self.check_tp_sb_s1e = gui.CheckBoxLabel('TP_SB_S1E', False, width=200, height=30)
        self.check_tp_sb_s1w = gui.CheckBoxLabel('TP_SB_S1W', False, width=200, height=30)
        
        
        avg_sensors = [self.check_s_nb_s2w, self.check_s_nb_s2e, self.check_s_nb_s1e,
        self.check_s_nb_s1w, self.check_t_nb_s2w, self.check_t_nb_s2e, self.check_t_nb_s1e,
        self.check_t_nb_s1w, self.check_tp_nb_s2w, self.check_tp_nb_s2e, self.check_tp_nb_s1e,
        self.check_tp_nb_s1w, self.check_s_sb_s2w, self.check_s_sb_s2e, self.check_s_sb_s1e,
        self.check_s_sb_s1w, self.check_t_sb_s2w, self.check_t_sb_s2e, self.check_t_sb_s1e,
        self.check_t_sb_s1w, self.check_tp_sb_s2w, self.check_tp_sb_s2e, self.check_tp_sb_s1e,
        self.check_tp_sb_s1w]
        
        self.go_avg = gui.Button('Go', width=200, height=30, margin='10px')
        self.go_avg.onclick.do(self.get_selected_avg)
        
        averagedContainer.append([self.lbl_avg, self.avg_txt, self.start_date, self.end_date, avg_sensors, self.go_avg])
        
        # Unaveraged data
        unaveragedContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        
        self.lbl_unavg = gui.Label('Unaveraged Data', width='100%', height=30, margin='10px')
        self.unavg_txt = gui.Label('The following section contains the daily unaveraged data. Please select the dates and sensors(s) you would like to access. All data is relative to time.', width='100%', height=30, margin='10px')
        
        self.start_unavg = gui.Date(width=200, height=20)
        self.end_unavg = gui.Date(width=200, height=20)
        
        self.check_s_nb_s2w_unavg = gui.CheckBoxLabel('S_NB_S2W', False, width=200, height=30)
        self.check_s_nb_s2e_unavg = gui.CheckBoxLabel('S_NB_S2E', False, width=200, height=30)
        self.check_s_nb_s1e_unavg = gui.CheckBoxLabel('S_NB_S1E', False, width=200, height=30)
        self.check_s_nb_s1w_unavg = gui.CheckBoxLabel('S_NB_S1W', False, width=200, height=30)
        self.check_t_nb_s2w_unavg = gui.CheckBoxLabel('T_NB_S2W', False, width=200, height=30)
        self.check_t_nb_s2e_unavg = gui.CheckBoxLabel('T_NB_S2E', False, width=200, height=30)
        self.check_t_nb_s1e_unavg = gui.CheckBoxLabel('T_NB_S1E', False, width=200, height=30)
        self.check_t_nb_s1w_unavg = gui.CheckBoxLabel('T_NB_S1W', False, width=200, height=30)
        self.check_tp_nb_s2w_unavg = gui.CheckBoxLabel('TP_NB_S2W', False, width=200, height=30)
        self.check_tp_nb_s2e_unavg = gui.CheckBoxLabel('TP_NB_S2E', False, width=200, height=30)
        self.check_tp_nb_s1e_unavg = gui.CheckBoxLabel('TP_NB_S1E', False, width=200, height=30)
        self.check_tp_nb_s1w_unavg = gui.CheckBoxLabel('TP_NB_S1W', False, width=200, height=30)
        
        self.check_s_sb_s2w_unavg = gui.CheckBoxLabel('S_SB_S2W', False, width=200, height=30)
        self.check_s_sb_s2e_unavg = gui.CheckBoxLabel('S_SB_S2E', False, width=200, height=30)
        self.check_s_sb_s1e_unavg = gui.CheckBoxLabel('S_SB_S1E', False, width=200, height=30)
        self.check_s_sb_s1w_unavg = gui.CheckBoxLabel('S_SB_S1W', False, width=200, height=30)
        self.check_t_sb_s2w_unavg = gui.CheckBoxLabel('T_SB_S2W', False, width=200, height=30)
        self.check_t_sb_s2e_unavg = gui.CheckBoxLabel('T_SB_S2E', False, width=200, height=30)
        self.check_t_sb_s1e_unavg = gui.CheckBoxLabel('T_SB_S1E', False, width=200, height=30)
        self.check_t_sb_s1w_unavg = gui.CheckBoxLabel('T_SB_S1W', False, width=200, height=30)
        self.check_tp_sb_s2w_unavg = gui.CheckBoxLabel('TP_SB_S2W', False, width=200, height=30)
        self.check_tp_sb_s2e_unavg = gui.CheckBoxLabel('TP_SB_S2E', False, width=200, height=30)
        self.check_tp_sb_s1e_unavg = gui.CheckBoxLabel('TP_SB_S1E', False, width=200, height=30)
        self.check_tp_sb_s1w_unavg = gui.CheckBoxLabel('TP_SB_S1W', False, width=200, height=30)
        
        
        unavg_sensors = [self.check_s_nb_s2w_unavg, self.check_s_nb_s2e_unavg,
        self.check_s_nb_s1e_unavg, self.check_s_nb_s1w_unavg, self.check_t_nb_s2w_unavg,
        self.check_t_nb_s2e_unavg, self.check_t_nb_s1e_unavg, self.check_t_nb_s1w_unavg,
        self.check_tp_nb_s2w_unavg, self.check_tp_nb_s2e_unavg, self.check_tp_nb_s1e_unavg,
        self.check_tp_nb_s1w_unavg, self.check_s_sb_s2w_unavg, self.check_s_sb_s2e_unavg,
        self.check_s_sb_s1e_unavg, self.check_s_sb_s1w_unavg, self.check_t_sb_s2w_unavg,
        self.check_t_sb_s2e_unavg, self.check_t_sb_s1e_unavg, self.check_t_sb_s1w_unavg,
        self.check_tp_sb_s2w_unavg, self.check_tp_sb_s2e_unavg, self.check_tp_sb_s1e_unavg,
        self.check_tp_sb_s1w_unavg]
        
        self.go_unavg = gui.Button('Go', width=200, height=30, margin='10px')
        self.go_unavg.onclick.do(self.get_selected_unavg)
        
        unaveragedContainer.append([self.lbl_unavg, self.unavg_txt, self.start_unavg, self.end_unavg, unavg_sensors, self.go_unavg])
        
        # FBG health
        fbgContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        
        self.lbl_fbg = gui.Label('FBG Health', width='100%', height=30, margin='10px')
        self.fbg_txt = gui.Label('This section shows the FBG peak range and power level for the specified dates. This information is used to understand whether there is a risk of erroneous data from FBGs being too close to each other, and whether an FBG peak level is deteriorating over time. All data is relative to time.', width='100%', height=30, margin='10px')
        
        self.start_fbg = gui.Date(width=200, height=20)
        self.end_fbg = gui.Date(width=200, height=20)
        
        self.check_s_nb_s2w = gui.CheckBoxLabel('S_NB_S2W', False, width=200, height=30)
        self.check_s_nb_s2e = gui.CheckBoxLabel('S_NB_S2E', False, width=200, height=30)
        self.check_s_nb_s1e = gui.CheckBoxLabel('S_NB_S1E', False, width=200, height=30)
        self.check_s_nb_s1w = gui.CheckBoxLabel('S_NB_S1W', False, width=200, height=30)
        self.check_t_nb_s2w = gui.CheckBoxLabel('T_NB_S2W', False, width=200, height=30)
        self.check_t_nb_s2e = gui.CheckBoxLabel('T_NB_S2E', False, width=200, height=30)
        self.check_t_nb_s1e = gui.CheckBoxLabel('T_NB_S1E', False, width=200, height=30)
        self.check_t_nb_s1w = gui.CheckBoxLabel('T_NB_S1W', False, width=200, height=30)
        self.check_tp_nb_s2w = gui.CheckBoxLabel('TP_NB_S2W', False, width=200, height=30)
        self.check_tp_nb_s2e = gui.CheckBoxLabel('TP_NB_S2E', False, width=200, height=30)
        self.check_tp_nb_s1e = gui.CheckBoxLabel('TP_NB_S1E', False, width=200, height=30)
        self.check_tp_nb_s1w = gui.CheckBoxLabel('TP_NB_S1W', False, width=200, height=30)
        
        self.check_s_sb_s2w = gui.CheckBoxLabel('S_SB_S2W', False, width=200, height=30)
        self.check_s_sb_s2e = gui.CheckBoxLabel('S_SB_S2E', False, width=200, height=30)
        self.check_s_sb_s1e = gui.CheckBoxLabel('S_SB_S1E', False, width=200, height=30)
        self.check_s_sb_s1w = gui.CheckBoxLabel('S_SB_S1W', False, width=200, height=30)
        self.check_t_sb_s2w = gui.CheckBoxLabel('T_SB_S2W', False, width=200, height=30)
        self.check_t_sb_s2e = gui.CheckBoxLabel('T_SB_S2E', False, width=200, height=30)
        self.check_t_sb_s1e = gui.CheckBoxLabel('T_SB_S1E', False, width=200, height=30)
        self.check_t_sb_s1w = gui.CheckBoxLabel('T_SB_S1W', False, width=200, height=30)
        self.check_tp_sb_s2w = gui.CheckBoxLabel('TP_SB_S2W', False, width=200, height=30)
        self.check_tp_sb_s2e = gui.CheckBoxLabel('TP_SB_S2E', False, width=200, height=30)
        self.check_tp_sb_s1e = gui.CheckBoxLabel('TP_SB_S1E', False, width=200, height=30)
        self.check_tp_sb_s1w = gui.CheckBoxLabel('TP_SB_S1W', False, width=200, height=30)
        
        
        fbg_sensors = [self.check_s_nb_s2w, self.check_s_nb_s2e, self.check_s_nb_s1e,
        self.check_s_nb_s1w, self.check_t_nb_s2w, self.check_t_nb_s2e, self.check_t_nb_s1e,
        self.check_t_nb_s1w, self.check_tp_nb_s2w, self.check_tp_nb_s2e, self.check_tp_nb_s1e,
        self.check_tp_nb_s1w, self.check_s_sb_s2w, self.check_s_sb_s2e, self.check_s_sb_s1e,
        self.check_s_sb_s1w, self.check_t_sb_s2w, self.check_t_sb_s2e, self.check_t_sb_s1e,
        self.check_t_sb_s1w, self.check_tp_sb_s2w, self.check_tp_sb_s2e, self.check_tp_sb_s1e,
        self.check_tp_sb_s1w]
        
        self.go_avg = gui.Button('Go', width=200, height=30, margin='10px')
        self.go_avg.onclick.do(self.get_selected_avg)
        
        fbgContainer.append([self.lbl_fbg, self.fbg_txt, self.start_fbg, self.end_fbg, fbg_sensors, self.go_avg])
        
        mainContainer.append([welcomeContainer, averagedContainer, unaveragedContainer, fbgContainer])
        
        self.stop_flag = False
        
        return mainContainer
    
    def query(self, table, sensors):
        conn = mysql.connect(host='localhost', database='douglas park bridges', username='root', password='zk89peTN')
        
        cursor = conn.cursor()
        
        select = ', '.join(sensors)
        query = f"SELECT timestamp, {select} from {table}"
        print(query)
        
        cursor.execute(query)
        records = cursor.fetchall()
        
        timestamp = []
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        i = []
        j = []
        k = []
        l = []
        m = []
        n = []
        o = []
        p = []
        q = []
        r = []
        s = []
        t = []
        u = []
        v = []
        w = []
        x = []
        
        alphabet = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x]
        
        for row in records:
            timestamp.append(row[0])
            i = 1
            while i < len(row):
                alphabet[i].append(row[i])
                i += 1
        
        filled = []
        for lst in alphabet:
            if len(lst) > 0:
                filled.append(lst)
        
        print(filled)
    
    def get_selected_avg(self, something):
        avg_sensors = [self.check_s_nb_s2w, self.check_s_nb_s2e, self.check_s_nb_s1e,
        self.check_s_nb_s1w, self.check_t_nb_s2w, self.check_t_nb_s2e, self.check_t_nb_s1e,
        self.check_t_nb_s1w, self.check_tp_nb_s2w, self.check_tp_nb_s2e, self.check_tp_nb_s1e,
        self.check_tp_nb_s1w, self.check_s_sb_s2w, self.check_s_sb_s2e, self.check_s_sb_s1e,
        self.check_s_sb_s1w, self.check_t_sb_s2w, self.check_t_sb_s2e, self.check_t_sb_s1e,
        self.check_t_sb_s1w, self.check_tp_sb_s2w, self.check_tp_sb_s2e, self.check_tp_sb_s1e,
        self.check_tp_sb_s1w]
        
        sensors = ['s_nb_s2w', 's_nb_s2e', 's_nb_s1e', 's_nb_s1w', 't_nb_s2w',
                   't_nb_s2e', 't_nb_s1e', 't_nb_s1w', 'tp_nb_s2w', 'tp_nb_s2e',
                   'tp_nb_s1e', 'tp_nb_s1w', 's_nb_s2w', 's_nb_s2e', 's_nb_s1e',
                   's_nb_s1w', 't_nb_s2w','t_nb_s2e', 't_nb_s1e', 't_nb_s1w',
                   'tp_nb_s2w', 'tp_nb_s2e', 'tp_nb_s1e', 'tp_nb_s1w']
        avg_selected = []
        count = 0
        for sensor in avg_sensors:
            if sensor.get_value() == True:
                avg_selected.append(sensors[count])
            count += 1
        
        self.query('averaged', avg_selected)
    
    def get_selected_unavg(self, something):
        unavg_sensors = [self.check_s_nb_s2w_unavg, self.check_s_nb_s2e_unavg,
        self.check_s_nb_s1e_unavg, self.check_s_nb_s1w_unavg, self.check_t_nb_s2w_unavg,
        self.check_t_nb_s2e_unavg, self.check_t_nb_s1e_unavg, self.check_t_nb_s1w_unavg,
        self.check_tp_nb_s2w_unavg, self.check_tp_nb_s2e_unavg, self.check_tp_nb_s1e_unavg,
        self.check_tp_nb_s1w_unavg, self.check_s_sb_s2w_unavg, self.check_s_sb_s2e_unavg,
        self.check_s_sb_s1e_unavg, self.check_s_sb_s1w_unavg, self.check_t_sb_s2w_unavg,
        self.check_t_sb_s2e_unavg, self.check_t_sb_s1e_unavg, self.check_t_sb_s1w_unavg,
        self.check_tp_sb_s2w_unavg, self.check_tp_sb_s2e_unavg, self.check_tp_sb_s1e_unavg,
        self.check_tp_sb_s1w_unavg]
        
        sensors = ['s_nb_s2w', 's_nb_s2e', 's_nb_s1e', 's_nb_s1w', 't_nb_s2w',
                   't_nb_s2e', 't_nb_s1e', 't_nb_s1w', 'tp_nb_s2w', 'tp_nb_s2e',
                   'tp_nb_s1e', 'tp_nb_s1w', 's_nb_s2w', 's_nb_s2e', 's_nb_s1e',
                   's_nb_s1w', 't_nb_s2w','t_nb_s2e', 't_nb_s1e', 't_nb_s1w',
                   'tp_nb_s2w', 'tp_nb_s2e', 'tp_nb_s1e', 'tp_nb_s1w']
        unavg_selected = []
        count = 0
        for sensor in unavg_sensors:
            if sensor.get_value() == True:
                unavg_selected.append(sensors[count])
            count += 1
        
        self.query('unaveraged', unavg_selected)
    
    def on_close(self):
        super(MyApp, self).on_close()

if __name__ == '__main__':
    start(MyApp, debug=True, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True)
