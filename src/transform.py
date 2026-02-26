import pandas as pd
from DAToolKit import db, Send_email, EmpDup, ErrorHandler, cron, cl

def definir_quincena (df_ind_op, campo_fecha):

    df_ind_op[campo_fecha] = pd.to_datetime(df_ind_op[campo_fecha], errors="coerce")
    
    df_ind_op["Quincena"] = df_ind_op[campo_fecha].apply(
        lambda x: "Qna 1" if 1 <= x.day <= 15 else "Qna 2"
    )
    
    return df_ind_op

def aplicar_orden_columnas (df_ind_op):

    columnas= [         
        "Centro"
        ,"Modelo_ruta"
        ,"Ruta_preventa"
        ,"Solicitante"
        ,"Visitado"
        ,"Fecha_operacion"
        ,"Anio"
        ,"Mes"
        ,"Quincena"
        ,"Num_Eq_Cte"
        ,"Escaneo_refri"
        ,"Motivo_No_Escaneo"

      ]
    
    columnas_insertar = [col for col in columnas if col in df_ind_op.columns]
    df_ind_op = df_ind_op[columnas_insertar]

    return df_ind_op

def buscar_coincidencias_refri_hist (df_ind_op, df_refri_hist):

    df_filtrado = df_ind_op[df_ind_op["Solicitante"].isin(df_refri_hist["Solicitante"])]

    return df_filtrado