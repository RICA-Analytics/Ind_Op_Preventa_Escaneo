from DAToolKit import db
import pandas as pd
from sqlalchemy import text
from datetime import datetime

def get_ind_op_primer_quincena(fecha_inicio, fecha_fin):

    db.create_engine('DA2-Comercial', trusted_connection=True)
    
    query_ind_op = f"""
      WITH consulta AS (
      	SELECT 
      	  LTRIM(RTRIM([Centro])) AS [Centro]
      	  ,LTRIM(RTRIM([Modelo_ruta])) AS [Modelo_ruta]
          ,CONCAT ('P',LTRIM(RTRIM([Ruta_preventa]))) AS [Ruta_preventa]
      		,RIGHT(REPLICATE('0', 10) + CAST([Solicitante] AS VARCHAR(10)), 10) AS [Solicitante]
          ,LTRIM(RTRIM([Visitado])) AS [Visitado]
      		,[Fecha_operacion]
      	  ,YEAR (Fecha_operacion) AS Anio
      	   , CASE 
      	    	WHEN MONTH (Fecha_operacion) = 1 THEN 'Ene'
      	    	WHEN MONTH (Fecha_operacion) = 2 THEN 'Feb'
      	    	WHEN MONTH (Fecha_operacion) = 3 THEN 'Mar'
      	    	WHEN MONTH (Fecha_operacion) = 4 THEN 'Abr'
      	    	WHEN MONTH (Fecha_operacion) = 5 THEN 'May'
      	    	WHEN MONTH (Fecha_operacion) = 6 THEN 'Jun'
      	    	WHEN MONTH (Fecha_operacion) = 7 THEN 'Jul'
      	    	WHEN MONTH (Fecha_operacion) = 8 THEN 'Ago'
      	    	WHEN MONTH (Fecha_operacion) = 9 THEN 'Sep'
      	    	WHEN MONTH (Fecha_operacion) = 10 THEN 'Oct'
      	    	WHEN MONTH (Fecha_operacion) = 11 THEN 'Nov'
      	    	WHEN MONTH (Fecha_operacion) = 12 THEN 'Dic'
      	   	END AS [Mes]
          ,LTRIM(RTRIM([Num_Eq_Cte])) AS [Num_Eq_Cte]
          ,SUM ([Escaneo_refri]) AS [Escaneo_refri]
          ,CASE
      			WHEN [Motivo_No_Escaneo] IS NULL THEN ''
      			ELSE [Motivo_No_Escaneo]
      	   END AS [Motivo_No_Escaneo]
           ,[Geolocalizacion]
      	FROM [Comercial].[dbo].[Ind_Op]
          WHERE Tipo_conexion = 'Salesforce Preventa' AND Fecha_operacion BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
          GROUP BY [Centro], [Modelo_ruta] ,[Ruta_preventa], [Solicitante], [Visitado], [Fecha_operacion], [Num_Eq_Cte], [Motivo_No_Escaneo], [Geolocalizacion]

      ), consulta_agrupada AS (

        SELECT
        	[Centro]
        	,[Modelo_ruta]
            ,[Ruta_preventa]
            ,[Solicitante]
            ,[Visitado]
        	,[Anio]
        	,[Mes]
        	,[Num_Eq_Cte]
        	,CASE 
				WHEN [Geolocalizacion] = 'En Cliente' THEN [Escaneo_refri]
				ELSE 0
			END AS [Escaneo_refri]
        	,[Motivo_No_Escaneo]
            ,ROW_NUMBER() OVER (
				PARTITION BY Solicitante
				ORDER BY Num_Eq_Cte DESC, Escaneo_refri DESC
			) AS rn
        FROM consulta

      )

      SELECT
      	[Centro]
      	,[Modelo_ruta]
          ,[Ruta_preventa]
          ,[Solicitante]
          ,[Visitado]
      	,(SELECT 
      	      CONVERT(date, MAX(Fecha_operacion)) AS UltimaFecha
            FROM [Comercial].[dbo].[Ind_Op]
      	  WHERE Tipo_conexion = 'Salesforce Preventa' AND Fecha_operacion BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
      	  ) AS [Fecha_operacion]
      	,[Anio]
      	,[Mes]
      	,[Num_Eq_Cte]
      	,SUM ([Escaneo_refri]) AS [Escaneo_refri]
      	,[Motivo_No_Escaneo]
      FROM consulta_agrupada
      WHERE rn = 1
      GROUP BY [Centro], [Modelo_ruta], [Ruta_preventa], [Solicitante], [Visitado], [Anio], [Mes], [Num_Eq_Cte], [Motivo_No_Escaneo]

    """

    df_ind_op = pd.read_sql(query_ind_op, 
                              db.get_engine('DA2-Comercial'), 
                              dtype_backend='pyarrow')
    
    return df_ind_op

def get_ind_op_segunda_quincena(fecha_inicio, fecha_fin):

    db.create_engine('DA2-Comercial', trusted_connection=True)
    
    query_ind_op = f"""
    WITH consulta AS (
      	SELECT 
      	  LTRIM(RTRIM([Centro])) AS [Centro]
      	  ,LTRIM(RTRIM([Modelo_ruta])) AS [Modelo_ruta]
          ,CONCAT ('P',LTRIM(RTRIM([Ruta_preventa]))) AS [Ruta_preventa]
      		,RIGHT(REPLICATE('0', 10) + CAST([Solicitante] AS VARCHAR(10)), 10) AS [Solicitante]
          ,LTRIM(RTRIM([Visitado])) AS [Visitado]
      		,[Fecha_operacion]
      	  ,YEAR (Fecha_operacion) AS Anio
      	   , CASE 
      	    	WHEN MONTH (Fecha_operacion) = 1 THEN 'Ene'
      	    	WHEN MONTH (Fecha_operacion) = 2 THEN 'Feb'
      	    	WHEN MONTH (Fecha_operacion) = 3 THEN 'Mar'
      	    	WHEN MONTH (Fecha_operacion) = 4 THEN 'Abr'
      	    	WHEN MONTH (Fecha_operacion) = 5 THEN 'May'
      	    	WHEN MONTH (Fecha_operacion) = 6 THEN 'Jun'
      	    	WHEN MONTH (Fecha_operacion) = 7 THEN 'Jul'
      	    	WHEN MONTH (Fecha_operacion) = 8 THEN 'Ago'
      	    	WHEN MONTH (Fecha_operacion) = 9 THEN 'Sep'
      	    	WHEN MONTH (Fecha_operacion) = 10 THEN 'Oct'
      	    	WHEN MONTH (Fecha_operacion) = 11 THEN 'Nov'
      	    	WHEN MONTH (Fecha_operacion) = 12 THEN 'Dic'
      	   	END AS [Mes]
          ,LTRIM(RTRIM([Num_Eq_Cte])) AS [Num_Eq_Cte]
          ,SUM ([Escaneo_refri]) AS [Escaneo_refri]
          ,CASE
      			WHEN [Motivo_No_Escaneo] IS NULL THEN ''
      			ELSE [Motivo_No_Escaneo]
      	   END AS [Motivo_No_Escaneo]
           ,[Geolocalizacion]
      	FROM [Comercial].[dbo].[Ind_Op]
          WHERE Tipo_conexion = 'Salesforce Preventa' AND Fecha_operacion BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
          GROUP BY [Centro], [Modelo_ruta] ,[Ruta_preventa], [Solicitante], [Visitado], [Fecha_operacion], [Num_Eq_Cte], [Motivo_No_Escaneo], [Geolocalizacion]

      ), consulta_agrupada AS (

        SELECT
        	[Centro]
        	,[Modelo_ruta]
            ,[Ruta_preventa]
            ,[Solicitante]
            ,[Visitado]
        	,[Anio]
        	,[Mes]
        	,[Num_Eq_Cte]
        	,CASE 
				WHEN [Geolocalizacion] = 'En Cliente' THEN [Escaneo_refri]
				ELSE 0
			END AS [Escaneo_refri]
        	,[Motivo_No_Escaneo]
            ,ROW_NUMBER() OVER (
				PARTITION BY Solicitante
				ORDER BY Num_Eq_Cte DESC, Escaneo_refri DESC
			) AS rn
        FROM consulta

      )

      SELECT
      	[Centro]
      	,[Modelo_ruta]
          ,[Ruta_preventa]
          ,[Solicitante]
          ,[Visitado]
      	,(SELECT 
      	      CONVERT(date, MAX(Fecha_operacion)) AS UltimaFecha
            FROM [Comercial].[dbo].[Ind_Op]
      	  WHERE Tipo_conexion = 'Salesforce Preventa' AND Fecha_operacion BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
      	  ) AS [Fecha_operacion]
      	,[Anio]
      	,[Mes]
      	,[Num_Eq_Cte]
      	,SUM ([Escaneo_refri]) AS [Escaneo_refri]
      	,[Motivo_No_Escaneo]
      FROM consulta_agrupada
      WHERE rn = 1
      GROUP BY [Centro], [Modelo_ruta], [Ruta_preventa], [Solicitante], [Visitado], [Anio], [Mes], [Num_Eq_Cte], [Motivo_No_Escaneo]
    """

    df_ind_op = pd.read_sql(query_ind_op, 
                              db.get_engine('DA2-Comercial'), 
                              dtype_backend='pyarrow')
    
    return df_ind_op

def get_solicitantes_ref_hist (fecha_inicio, fecha_fin):

    db.create_engine('DA4-Comercial', trusted_connection=True)

    query_refri_hist = f"""
        SELECT DISTINCT Solicitante
        FROM [Comercial].[dbo].[Refrigeracion_Hist]
        WHERE [Fecha_Carga] BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    """

    df_refri_hist = pd.read_sql(query_refri_hist, 
                              db.get_engine('DA4-Comercial'), 
                              dtype_backend='pyarrow')

    return df_refri_hist

def get_fecha_inicio():
    fecha = datetime.now()

    if fecha.day == 1:
        # Si es día 1, tomamos la segunda quincena del mes anterior
        dia_inicio = 16
        if fecha.month == 1:  # Caso especial: enero
            mes = 12
            anio = fecha.year - 1
        else:
            mes = fecha.month - 1
            anio = fecha.year
        fecha_inicio = f"{anio}-{str(mes).zfill(2)}-{str(dia_inicio).zfill(2)}"

    elif 2 <= fecha.day <= 15:
        dia_inicio = 1
        fecha_inicio = f"{fecha.year}-{str(fecha.month).zfill(2)}-{str(dia_inicio).zfill(2)}"

    else:  # día >= 16
        dia_inicio = 16
        fecha_inicio = f"{fecha.year}-{str(fecha.month).zfill(2)}-{str(dia_inicio).zfill(2)}"

    return fecha_inicio


def get_fecha_fin (anio_fin, mes_num_fin):
    db.create_engine('DA2-Comercial', trusted_connection=True)
    
    query_ultima_fecha = f"""
      SELECT 
	      CONVERT(date, MAX(Fecha_operacion)) AS UltimaFecha
      FROM [Comercial].[dbo].[Ind_Op]
      WHERE YEAR (Fecha_operacion) = {anio_fin} AND MONTH (Fecha_operacion) = {mes_num_fin}

    """

    df_ultima_fecha = pd.read_sql(query_ultima_fecha, 
                              db.get_engine('DA2-Comercial'), 
                              dtype_backend='pyarrow')
    
    fecha_fin = df_ultima_fecha['UltimaFecha'].unique()[0]
    
    return fecha_fin

def get_quincena (df_ind_op):
    
    quincenas_delete = df_ind_op['Quincena'].unique().tolist()
    valores_sql = ",".join(f"'{q}'" for q in quincenas_delete)

    return valores_sql

def get_mes_delete (df_ind_op):
    
    mes_delete = df_ind_op['Mes'].unique().tolist()
    mes_sql = ",".join(f"'{q}'" for q in mes_delete)

    return mes_sql