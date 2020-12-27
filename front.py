import streamlit as st
import numpy as np
import pandas as pd
import plotly.subplots as make_subplot
import plotly.express as px
import plotly.graph_objects as go 
import back
import tempfile
from contextlib import contextmanager
import pathlib
import uuid
import os
import sqlite3 
def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.image('sss.jpg')
    st.sidebar.write('Bring your database here:')
    data = st.sidebar.file_uploader('*Upload or drop your db file, maxsize = 1GB:', type = 'odb')
    if data:
        with Loading_file(data) as datos:
        #with Loading_file(data) as datos:
            if st.sidebar.checkbox('Average distance (Do not use)'):
                st.success('Loading... Average distance')
                st.dataframe(datos.dist_prom().style.format({'Distance': '{:.2f}'}))
            if st.sidebar.checkbox('Cycle time'):
                st.success('Loading cycle routes:')
                st.dataframe(datos.rutas().style.format({'Distance_km': '{:.2f}', 'Queue_time': '{:.2f}'}))
                carga = st.selectbox('Loading zone:', datos.data.cargas)
                descarga = st.selectbox('Dumping zone', datos.data.descargas)
                if carga != 'Desconocido' and descarga != 'Desconocido':
                    st.success('Loading... Cycle time:')
                    try:
                        st.plotly_chart(datos.cycle_time(carga, descarga))
                    except:
                        st.write('No existen ciclos')
    
            if st.sidebar.checkbox('Queue + Hang + Match Pala - Camión:'):
                st.success('Proximamente.....')
            if st.sidebar.checkbox('Availability + UoD'):
                date = st.sidebar.radio('Dates:', list(datos.data.dates.keys()))
                #converting date:
                date_use = datos.data.dates[date]
                if date:
                    #Trucks data 
                    st.success('Loading... Availability and UoD - Trucks')
                    #saving Trucks Availability and UoD 
                    trucks_a_uod = datos.a_uod_trucks(date_use)
                    st.dataframe(trucks_a_uod.style.format({'Availability':'{:.1f}','UoD':'{:.1f}'}))
                    if st.checkbox('Display trucks model time:'):
                        model_truck = st.radio('Trucks models', trucks_a_uod['Truck_Model'])
                        st.plotly_chart(datos.model_time_trucks(date_use, model_truck))
                    #Shovel data
                    st.success('Loading... Availability and UoD - Shovels')
                    shovels_a_uod = datos.a_shovels(date_use)
                    st.dataframe(shovels_a_uod.style.format({'Availability':'{:.1f}','UoD':'{:.1f}'}))
                    if st.checkbox('Display shovels model time:'):
                        pala_name = st.radio('Pala names', shovels_a_uod['Shovel_name'])
                        st.plotly_chart(datos.model_time_shovels(date_use, pala_name))
                    
                    
                            
#Bringing everything from back.py
class Loading_file:
    def __init__(self, data):
        self.bytes = data.getvalue()
        self.data = None
        self.fp = None
    
    def __enter__(self):
        """Called when entering a `with` block."""
        self.fp = pathlib.Path(str(uuid.uuid4()))
        self.fp.write_bytes(self.bytes)
        self.connector = sqlite3.connect(str(self.fp))
        self.cursor = self.connector.cursor()
        self.data = back.Basededatos(self.connector,self.cursor)
        # We return the current object
        return self  
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Run on `with` block exit."""
        # Here we just have to remove the temporary database file
        self.connector.close()
        self.fp.unlink()
    

    def rutas(self):
        return self.data.rutas()

    def cycle_time(self, carga, descarga):
        df = self.data.cycle_time(carga, descarga) 
        total = round(sum(df.T[0].to_list()),2)
        fig = go.Figure(go.Waterfall(orientation='v', measure = ["relative","relative","relative","relative","relative","relative","total"],
                             textposition= 'outside',
                            text = [str(number)+ " ("+str(round(number*100/total))+"%)" for number in df.T[0].to_list()+[total]],
                             increasing = {"marker":{"color":"Teal"}},
                             totals = {"marker":{"color":"deep sky blue", "line":{"color":"blue", "width":3}}},
                             x = df.columns.to_list()+ ['total'], y= df.T[0].to_list()+[None]))
        fig.update_layout(title = 'Cycle Time from '+ carga +  " to " + descarga, margin = dict(b=35, t=35))
        return fig

    def dist_prom(self):
        return self.data.distancia_promedio()

    #Calling dispo_uoa_trucks
    def a_uod_trucks(self, turno):
        return self.data.disp_uoa_trucks(turno)
    #Calling model_time_trucks
    def model_time_trucks(self, turno, modelo):
        df = self.data.model_time_trucks(turno, modelo)
        total_disp = round(sum(df.T[0].to_list()[:5]),2)
        total_nom = round(sum(df.T[0].to_list()),2)
        text_1 = [str(number)+ " ("+str(round(number*100/total_disp))+"%)" for number in df.T[0].to_list()[:5]]
        text_2 = [str(number)+ " ("+str(round(number*100/total_nom))+"%)" for number in [total_disp]+df.T[0].to_list()[5:7]+[total_nom]]
        fig = go.Figure(go.Waterfall(orientation='v', measure = ["relative", "relative","relative","relative","relative", "total", "relative","relative","total"],
                            textposition= 'outside', textfont = dict(size=12),
                            text = text_1 + text_2, 
                            increasing = {"marker":{"color":"Teal"}},
                            totals = {"marker":{"color":"deep sky blue", "line":{"color":"blue", "width":3}}},
                            x = df.columns.to_list()[:5]+ ['Total_Disp.']+ df.columns.to_list()[5:7]+ ['Total_Nom'], y= df.T[0].to_list()[:5]+[None]+df.T[0].to_list()[5:] + [None]))
        fig.update_layout(title = modelo + 'Model Time Distribution', margin = dict(b=45, t=45, r= 0, l = 0))
        #fig.update_traces(insidetextfont_size = 16, selector=dict(type='waterfall'))
        fig.update_xaxes(title_text='Time Model')
        fig.update_yaxes(title_text='Time in Hours (hrs)')
        return fig

    #Calling dispo_shovels
    def a_shovels(self, turno):
        return self.data.disp_shovels(turno)
    #Calling model_time_shovels
    def model_time_shovels(self, turno, pala):
        df = self.data.model_time_shovels(turno, pala)
        total_disp = round(sum(df.T[0].to_list()[:5]),2)
        total_nom = round(sum(df.T[0].to_list()),2)
        text_1 = [str(number)+ " ("+str(round(number*100/total_disp))+"%)" for number in df.T[0].to_list()[:5]]
        text_2 = [str(number)+ " ("+str(round(number*100/total_nom))+"%)" for number in [total_disp]+df.T[0].to_list()[5:7]+[total_nom]]
        fig = go.Figure(go.Waterfall(orientation='v', measure = ["relative", "relative","relative","relative","relative", "total", "relative","relative","total"],
                            textposition= 'outside', textfont = dict(size=12),
                            text = text_1 + text_2, 
                            increasing = {"marker":{"color":"Teal"}},
                            totals = {"marker":{"color":"deep sky blue", "line":{"color":"blue", "width":3}}},
                            x = df.columns.to_list()[:5]+ ['Total_Disp.']+ df.columns.to_list()[5:7]+ ['Total_Nom'], y= df.T[0].to_list()[:5]+[None]+df.T[0].to_list()[5:] + [None]))
        fig.update_layout(title = pala + 'Model Time Distribution', margin = dict(b=45, t=45, r= 0, l = 0))
        #fig.update_traces(insidetextfont_size = 16, selector=dict(type='waterfall'))
        fig.update_xaxes(title_text='Time Model')
        fig.update_yaxes(title_text='Time in Hours (hrs)')
        return fig
          

if __name__ == '__main__':
    main()