from calendar import month
from DAToolKit import db
import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from transform import *
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "querys"

def get_seguimiento (alias_servidor_origen, trusted_connection_origen, fecha_inicio, fecha_fin):
    db.create_engine(alias_servidor_origen, trusted_connection=trusted_connection_origen)
    query = (PATH / "Ind_Op_Preventa_Escaneo_Seguimiento.sql").read_text(encoding="latin-1")
    query = query.format(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    df = pd.read_sql(query, db.get_engine(alias=alias_servidor_origen))
    return df

def get_logro (alias_servidor_origen, trusted_connection_origen, fecha_inicio, fecha_fin):
    db.create_engine(alias_servidor_origen, trusted_connection=trusted_connection_origen)
    query = (PATH / "Ind_Op_Preventa_Escaneo_Objetivo_Escaneo.sql").read_text(encoding="latin-1")
    query = query.format(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    df = pd.read_sql(query, db.get_engine(alias=alias_servidor_origen))
    return df

def get_periodo (alias_servidor_origen, trusted_connection_origen):
    db.create_engine(alias_servidor_origen, trusted_connection=trusted_connection_origen)
    fecha = datetime.now()

    if fecha.day == 1:
        if fecha.month == 1:
            anio = fecha.year - 1
            mes = 12
        else:
            anio = fecha.year
            mes = fecha.month - 1    
    else:
        anio = fecha.year
        mes = fecha.month

    meses = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    mes_abrev = meses[mes]

    query_inicio = (PATH / "Consulta_Fechas.sql").read_text(encoding="latin-1")
    query_inicio = query_inicio.format(operador='MIN', anio = anio, mes = mes)
    df_inicio = pd.read_sql(query_inicio, db.get_engine(alias=alias_servidor_origen))
    fecha_inicio = df_inicio['Fecha'].iloc[0]

    query_fin = (PATH / "Consulta_Fechas.sql").read_text(encoding="latin-1")
    query_fin = query_fin.format(operador='MAX', anio = anio, mes = mes)
    df_fin = pd.read_sql(query_fin, db.get_engine(alias=alias_servidor_origen))
    fecha_fin = df_fin['Fecha'].iloc[0]
    
    return anio, mes_abrev, fecha_inicio, fecha_fin