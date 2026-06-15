import logging
from math import ceil

from logging_config import setup_logging
from extract import *
from transform import *
from load import *
from DAToolKit import db, Send_email, EmpDup, ErrorHandler, cron, cl, SQLutils
from datetime import datetime
from pathlib import Path
import glob
import os

def main():
    logger = logging.getLogger(__name__)
    
    logger.info("Inicio del proceso Ind_Op_Preventa_Escaneo")
    # Implementacion Runner_ prubea3

    alias_servidor_origen = 'DA2-Comercial'
    trusted_connection_origen = True

    alias_servidor_destino = 'DA4-Comercial'
    trusted_connection_destino = True
    esquema_destino = 'dbo'
    # tabla_destino_1 = 'Ind_Op_Prev_Escaneo_Seguimiento'
    tabla_destino_2 = 'Ind_Op_Prev_Escaneo_Logro'

    anio_manual = 2025
    mes_abrev_manual = 'Ago'
    fecha_inicio_manual = '2025-08-01'
    fecha_fin_manual = '2025-08-31'

    # tipo_procesamiento = 'manual'
    tipo_procesamiento = 'automatico'

    if tipo_procesamiento == 'manual':
        anio = anio_manual
        mes_abrev = mes_abrev_manual
        fecha_inicio = fecha_inicio_manual
        fecha_fin = fecha_fin_manual
    elif tipo_procesamiento == 'automatico':
        anio, mes_abrev, fecha_inicio, fecha_fin = get_periodo(alias_servidor_origen=alias_servidor_origen, trusted_connection_origen=trusted_connection_origen)
    
    try:
        
        # variables
        fecha = datetime.now()
        
        logger.info(
            "Parámetros | fecha_ejecucion=%s | tipo_procesamiento=%s | anio=%s | mes_abrev=%s | fecha_inicio=%s | fecha_fin=%s",
            fecha, tipo_procesamiento, anio, mes_abrev, fecha_inicio, fecha_fin
        )

        logger.info("Extrayendo información")
        # df_seguimiento = get_seguimiento(alias_servidor_origen=alias_servidor_origen, trusted_connection_origen=trusted_connection_origen, fecha_inicio = fecha_inicio, fecha_fin=fecha_fin)
        df_logro = get_logro(alias_servidor_origen=alias_servidor_origen, trusted_connection_origen=trusted_connection_origen, fecha_inicio = fecha_inicio, fecha_fin=fecha_fin)

        # print(SQLutils.CreateTable(df_seguimiento, 'Ind_Op_Prev_Escaneo_Seguimiento'))
        # print(SQLutils.CreateTable(df_logro, 'Ind_Op_Prev_Escaneo_Logro'))
        
        logger.info(f"Cargando información a {alias_servidor_destino}")
        # load_table(alias_servidor_destino=alias_servidor_destino, trusted_connection_destino=trusted_connection_destino, esquema_destino=esquema_destino, tabla_destino=tabla_destino_1, df=df_seguimiento, anio_delete=anio, mes_delete=mes_abrev )
        load_table(alias_servidor_destino=alias_servidor_destino, trusted_connection_destino=trusted_connection_destino, esquema_destino=esquema_destino, tabla_destino=tabla_destino_2, df=df_logro, anio_delete=anio, mes_delete=mes_abrev )
        
        logger.info("Proceso finalizado correctamente")
        
    except Exception:
        logger.exception("Error durante la ejecución del proceso")
        raise
        
if __name__ == "__main__":
    setup_logging()
    main()