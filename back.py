

import numpy as np
import pandas as pd
import datetime

class Basededatos:
    def __init__(self, connector, cursor):
        self.connector = connector
        self.cargas = [item[0] for item in cursor.execute('SELECT DISTINCT carga_name FROM Carga;').fetchall()]
        self.descargas = [item[0] for item in cursor.execute('SELECT DISTINCT descarga_name FROM Descarga;').fetchall()]
        self.dates = {datetime.datetime.utcfromtimestamp(int(item[0])).strftime('%Y-%m-%d'):item[0] for item in cursor.execute('SELECT DISTINCT turno_day FROM Turno WHERE turno_day>0;').fetchall()}
       
    #Rutas
    def rutas(self):
        query = pd.read_sql_query('SELECT carga_name as Load, descarga_name as Dump, COUNT(*) as Cycles, ROUND(AVG(cicloload_travel_distance+ciclodump_travel_distance)/1000,2) as Distance_km,  ROUND(AVG(cicloload_queued_time + ciclodump_queued_time)/60,2) as Queue_time FROM CicloDump\
            INNER JOIN CicloLoad as cl ON cl.cicloload_id = CicloDump.ciclodump_prev_load_id INNER JOIN Carga ON Carga.carga_id = CicloDump.ciclodump_carga_id INNER JOIN Descarga ON Descarga.descarga_id = CicloDump.ciclodump_descarga_id\
            INNER JOIN Pala ON Pala.pala_id = ciclodump_pala_id\
            WHERE CicloDump.ciclodump_prev_load_id <> 0 GROUP BY carga_name, descarga_name;', self.connector)
        return pd.DataFrame(query)
    #Tiempos de ciclo :
    def cycle_time(self, carga, descarga):
        query = pd.read_sql_query('SELECT ROUND(AVG(ciclodump_travel_time)/60,2) as Tiempo_viaje_lleno, \
            ROUND(AVG(ciclodump_dumping_time)/60,2) as Tiempo_descarga, ROUND(AVG(cicloload_travel_time)/60,2) as Tiempo_viaje_vacio, \
            ROUND(AVG(cicloload_spot_time)/60,2) as Tiempo_Spot_Prom, ROUND(AVG(cicloload_loading_time)/60,2) as Tiempo_Carga_Prom, \
            ROUND(AVG(cicloload_queued_time + ciclodump_queued_time)/60,2) as Colas FROM CicloDump\
            INNER JOIN CicloLoad as cl ON cl.cicloload_id = CicloDump.ciclodump_prev_load_id INNER JOIN Carga ON Carga.carga_id = CicloDump.ciclodump_carga_id INNER JOIN Descarga ON Descarga.descarga_id = CicloDump.ciclodump_descarga_id\
            WHERE CicloDump.ciclodump_prev_load_id <> 0 AND carga_name = ? AND descarga_name = ?;', self.connector, params = (carga, descarga))
        return pd.DataFrame(query)
    #Distancias:
    def distancia_promedio(self):
        query = pd.read_sql_query('SELECT descargatype_name AS Descarga, ROUND(AVG(CicloDump.ciclodump_travel_distance)/1000,2) as Distancia_km, COUNT(*) AS Viajes FROM CicloDump\
                          INNER JOIN Descarga ON Descarga.descarga_id = CicloDump.ciclodump_descarga_id\
                          INNER JOIN DescargaType ON DescargaType.descargatype_id = Descarga.descarga_type\
                          GROUP BY descargatype_name;', self.connector)
        
        return pd.DataFrame(query)

    #Availability and UoD  - Trucks     
    def disp_uoa_trucks(self, turno):
        query = pd.read_sql_query('SELECT modelo_name as Truck_Model, ROUND(SUM(CASE WHEN if_indicador = "DISP" THEN if_valor ELSE 0 END)/SUM(CASE WHEN if_indicador = "NOM" THEN if_valor ELSe 1 END)*100,1) as Availability,\
            ROUND(SUM(CASE WHEN if_indicador = "EF" THEN if_valor ELSE 0 END)/SUM(CASE WHEN if_indicador = "DISP" THEN if_valor ELSE 1 END)*100,1) as UoD\
            FROM IndicadorFaena\
            INNER JOIN Camion on Camion.camion_id = IndicadorFaena.if_equipo_id AND IndicadorFaena.if_equipotype_id =1\
            INNER JOIN Modelo on Modelo.modelo_id = camion_modelo_id\
            INNER JOIN Turno on Turno.turno_id = IndicadorFaena.if_turno_id\
            WHERE turno_day = ?\
            GROUP BY modelo_name;', self.connector, params = [turno])
        return pd.DataFrame(query)
    #Displaying model time for trucks:
    def model_time_trucks(self, turno, modelo):
        query = pd.read_sql_query('SELECT ROUND(SUM(CASE WHEN if_indicador = "EF" THEN if_valor ELSE 0 END)/3600,1) AS EF, ROUND(SUM(CASE WHEN if_indicador = "DEMP" THEN if_valor ELSE 0 END)/3600,1) AS DEMP, ROUND(SUM(CASE WHEN if_indicador = "DEMNP" THEN if_valor ELSE 0 END)/3600,1) AS DEMNP,\
            ROUND(SUM(CASE WHEN if_indicador = "PO" THEN if_valor ELSE 0 END)/3600,1) AS PO, ROUND(SUM(CASE WHEN if_indicador = "RES" THEN if_valor ELSE 0 END)/3600,1) AS RES,\
            ROUND(SUM(CASE WHEN if_indicador = "MPRG" THEN if_valor ELSE 0 END)/3600,1) AS MPR, ROUND(SUM(CASE WHEN if_indicador = "MNPRG" THEN if_valor ELSE 0 END)/3600,1) AS MNP\
            FROM IndicadorFaena\
            INNER JOIN Camion on Camion.camion_id = IndicadorFaena.if_equipo_id AND IndicadorFaena.if_equipotype_id =1\
            INNER JOIN Modelo on Modelo.modelo_id = camion_modelo_id\
            INNER JOIN Turno on Turno.turno_id = IndicadorFaena.if_turno_id\
            WHERE turno_day = ? AND modelo_name = ?;', self.connector, params = [turno, modelo])
        return pd.DataFrame(query)
    #Availability - Shovels
    def disp_shovels(self, turno):
        query = pd.read_sql_query('SELECT pala_name as Shovel_name, ROUND(SUM(CASE WHEN if_indicador = "DISP" THEN if_valor ELSE 0 END)/SUM(CASE WHEN if_indicador = "NOM" THEN if_valor ELSe 1 END)*100,1) as Availability,\
            ROUND(SUM(CASE WHEN if_indicador = "EF" THEN if_valor ELSE 0 END)/SUM(CASE WHEN if_indicador = "DISP" THEN if_valor ELSE 1 END)*100,1) as UoD\
            FROM IndicadorFaena\
            INNER JOIN Pala on Pala.pala_id = IndicadorFaena.if_equipo_id AND IndicadorFaena.if_equipotype_id =2\
            INNER JOIN Modelo on Modelo.modelo_id = pala_modelo_id\
            INNER JOIN Turno on Turno.turno_id = IndicadorFaena.if_turno_id\
            WHERE turno_day = ?\
            GROUP BY pala_name;', self.connector, params = [turno])
        return pd.DataFrame(query)

    #Displaying model time for shovels    
    def model_time_shovels(self, turno, pala):
        query = pd.read_sql_query('SELECT ROUND(SUM(CASE WHEN if_indicador = "EF" THEN if_valor ELSE 0 END)/3600,1) AS EF, ROUND(SUM(CASE WHEN if_indicador = "DEMP" THEN if_valor ELSE 0 END)/3600,1) AS DEMP, ROUND(SUM(CASE WHEN if_indicador = "DEMNP" THEN if_valor ELSE 0 END)/3600,1) AS DEMNP,\
            ROUND(SUM(CASE WHEN if_indicador = "PO" THEN if_valor ELSE 0 END)/3600,1) AS PO, ROUND(SUM(CASE WHEN if_indicador = "RES" THEN if_valor ELSE 0 END)/3600,1) AS RES,\
            ROUND(SUM(CASE WHEN if_indicador = "MPRG" THEN if_valor ELSE 0 END)/3600,1) AS MPR, ROUND(SUM(CASE WHEN if_indicador = "MNPRG" THEN if_valor ELSE 0 END)/3600,1) AS MNP\
            FROM IndicadorFaena\
            INNER JOIN Pala on Pala.pala_id = IndicadorFaena.if_equipo_id AND IndicadorFaena.if_equipotype_id =2\
            INNER JOIN Modelo on Modelo.modelo_id = pala_modelo_id\
            INNER JOIN Turno on Turno.turno_id = IndicadorFaena.if_turno_id\
            WHERE turno_day = ? AND pala_name = ?;', self.connector, params = [turno, pala])
        return pd.DataFrame(query)