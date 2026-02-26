import logging
from DAToolKit import db, Send_email, EmpDup, ErrorHandler, cron, SQLutils

from regex import D

from logging_config import setup_logging
from extract import get_ind_op_primer_quincena, get_ind_op_segunda_quincena, get_fecha_inicio, get_fecha_fin, get_quincena, get_mes_delete, get_solicitantes_ref_hist
from transform import definir_quincena, aplicar_orden_columnas, buscar_coincidencias_refri_hist
from load import load_ind_op
from datetime import datetime

def main():
    logger = logging.getLogger(__name__)
    
    logger.info("Inicio del proceso Ind_Op_Preventa_Escaneo")
    
    try:
    
        # variables
        # tipo_procesamiento = 'Manual'
        tipo_procesamiento = 'Automatico'
        fecha_inicio_manual = '2026-02-16'
        fecha_fin_manual = '2026-02-24'

        if tipo_procesamiento == 'Automatico':
            fecha_inicio = get_fecha_inicio ()
            fecha_inicio_formato = datetime.strptime(fecha_inicio,"%Y-%m-%d").date()
            anio_fin = fecha_inicio_formato.year
            mes_num_fin = fecha_inicio_formato.month
            fecha_fin = get_fecha_fin (anio_fin=anio_fin, mes_num_fin=mes_num_fin)
        else:
            fecha_inicio = fecha_inicio_manual
            fecha_fin = fecha_fin_manual

        fecha_fin_formato = datetime.strptime(fecha_fin,"%Y-%m-%d").date()
        anio = fecha_fin_formato.year
        mes_num = fecha_fin_formato.month

        
        logger.info(
            "Parámetros | fecha_inicio=%s | fecha_fin=%s | Procesamiento=%s",
            fecha_inicio, fecha_fin, tipo_procesamiento
        )
        
        # funciones
        logger.info("Extrayendo información")

        if fecha_fin_formato.day >= 16:
            print ("Se procesara la segunda quincena")
            df_ind_op = get_ind_op_segunda_quincena (fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        else:
            print ("Se procesara la primer quincena")
            df_ind_op = get_ind_op_primer_quincena (fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        
        df_refri_hist = get_solicitantes_ref_hist(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

        # print(SQLutils.CreateTable(df_ind_op, 'Ind_Op_Preventa_Escaneo'))

        logger.info("Aplicando transformación a data")
        df_ind_op = definir_quincena(df_ind_op=df_ind_op, campo_fecha='Fecha_operacion')
        df_ind_op = aplicar_orden_columnas (df_ind_op=df_ind_op) 
        quincenas_delete = get_quincena (df_ind_op=df_ind_op)
        mes = get_mes_delete (df_ind_op=df_ind_op)
        # df_ind_op = buscar_coincidencias_refri_hist (df_ind_op=df_ind_op, df_refri_hist=df_refri_hist)
        
        logger.info(f"Cargando información a RDA4-Comercial")
        load_ind_op(df_ind_op=df_ind_op, anio=anio, mes=mes, quincenas_delete=quincenas_delete)

        logger.info("Proceso finalizado correctamente")
        
    except Exception:
        logger.exception("Error durante la ejecución del proceso")
        raise
        
if __name__ == "__main__":
    setup_logging()
    main()