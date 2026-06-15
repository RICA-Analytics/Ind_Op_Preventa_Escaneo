WITH consulta AS (
 
	SELECT 
		LTRIM(RTRIM([Centro])) AS [Centro]
      	,LTRIM(RTRIM([Modelo_ruta])) AS [Modelo_ruta]
        ,CONCAT ('P',LTRIM(RTRIM([Ruta_preventa]))) AS [Ruta_preventa]
      	,RIGHT(REPLICATE('0', 10) + CAST([Solicitante] AS VARCHAR(10)), 10) AS [Solicitante]
        ,LTRIM(RTRIM([Visitado])) AS [Visitado]
        ,CONVERT(date, Fecha_operacion) AS [Fecha_operacion]
      	,YEAR (Fecha_operacion) AS Anio
		,CASE 
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
		,CASE 
			WHEN DAY (Fecha_operacion) <= 15 THEN 'Qna 1'
			ELSE 'Qna 2'
		END AS [Quincena]
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
    ,MAX([Fecha_operacion]) OVER (
        PARTITION BY Solicitante, Quincena
    ) AS [Ultima_fecha_operacion_quincena]
    ,[Anio]
    ,[Mes]
	,[Quincena]
    ,[Num_Eq_Cte]
    ,CASE 
		WHEN [Geolocalizacion] = 'En Cliente' THEN [Escaneo_refri]
		ELSE 0
	END AS [Escaneo_refri_ant]
    ,[Motivo_No_Escaneo]
    ,ROW_NUMBER() OVER (
		PARTITION BY Solicitante, Quincena
		ORDER BY Num_Eq_Cte DESC, Escaneo_refri DESC
	) AS rn
 
FROM consulta
 
), arreglando_escaneo AS (
SELECT 
	Solicitante
	,Quincena
	,SUM(Escaneo_refri_ant) AS [Escaneo_refri]
	FROM consulta_agrupada
	GROUP BY Solicitante, Quincena
 
), consulta_final AS (
 
SELECT
	[Centro]
    ,[Modelo_ruta]
    ,[Ruta_preventa]
    ,ca.[Solicitante]
    ,[Visitado]
    ,[Ultima_fecha_operacion_quincena]
    ,(SELECT 
		CONVERT(date, MAX(Fecha_operacion)) AS UltimaFecha
	FROM [Comercial].[dbo].[Ind_Op]
    WHERE Tipo_conexion = 'Salesforce Preventa' AND Fecha_operacion BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    ) AS [Fecha_corte]
    ,[Anio]
    ,[Mes]
	,ca.[Quincena]
    ,[Num_Eq_Cte] AS [Num_eq_cte]
    ,[Escaneo_refri] AS [Total_escaneos]
	,CASE	
		WHEN [Escaneo_refri] > [Num_Eq_Cte] THEN [Num_Eq_Cte]
		ELSE [Escaneo_refri]
	END AS [Check_escaneos]
    ,[Motivo_No_Escaneo] AS [Motivo_no_escaneo]
FROM consulta_agrupada AS ca
LEFT JOIN arreglando_escaneo AS ae ON ca.Solicitante = ae.Solicitante AND ca.Quincena = ae.Quincena
WHERE rn = 1
 
), consulta_objetivo AS (
 
SELECT 
    Centro,
    Ruta_preventa,
    Solicitante,
	MAX(CASE WHEN Quincena = 'Qna 1' THEN Ultima_fecha_operacion_quincena END) AS Ultima_fecha_operacion_qna1,
	MAX(CASE WHEN Quincena = 'Qna 2' THEN Ultima_fecha_operacion_quincena ELSE Fecha_corte END) AS Ultima_fecha_operacion_qna2,
	Fecha_corte,
    Anio,
    Mes,
    SUM(CASE WHEN Quincena = 'Qna 1' THEN CAST(Num_eq_cte AS INT) ELSE 0 END) AS Num_eq_cte_qna1,
    SUM(CASE WHEN Quincena = 'Qna 1' THEN CAST(Check_escaneos AS INT) ELSE 0 END) AS Check_escaneos_qna1,
	SUM(CASE WHEN Quincena = 'Qna 2' THEN CAST(Num_eq_cte AS INT) ELSE 0 END) AS Num_eq_cte_qna2,
    SUM(CASE WHEN Quincena = 'Qna 2' THEN CAST(Check_escaneos AS INT) ELSE 0 END) AS Check_escaneos_qna2,
	SUM(
    CASE 
        WHEN Quincena = 'Qna 1' THEN CAST(Num_eq_cte AS INT) 
        ELSE 0 
    END
    +
    CASE 
        WHEN Quincena = 'Qna 2' THEN CAST(Num_eq_cte AS INT) 
        ELSE 0 
    END
	) AS Objetivo_escaneos,
	SUM(
    CASE 
        WHEN Quincena = 'Qna 1' THEN CAST(Check_escaneos AS INT) 
        ELSE 0 
    END
    +
    CASE 
        WHEN Quincena = 'Qna 2' THEN CAST(Check_escaneos AS INT) 
        ELSE 0 
    END
	) AS Logro_escaneos
FROM consulta_final
GROUP BY 
    Centro, Ruta_preventa, Solicitante, Fecha_corte, Anio, Mes
 
)
 
SELECT 
	Centro
	,Ruta_preventa
	,Solicitante
	,Ultima_fecha_operacion_qna1
	,Ultima_fecha_operacion_qna2
	,Fecha_corte
	,Anio
	,Mes
	,Num_eq_cte_qna1
	,Check_escaneos_qna1
	,Num_eq_cte_qna2
	,Check_escaneos_qna2
	,Objetivo_escaneos
	,Logro_escaneos
	,CASE
		WHEN Logro_escaneos = 0 THEN 0
		ELSE 
			CASE
				WHEN Logro_escaneos >= Objetivo_escaneos THEN 1
				ELSE 0
			END
	END AS Exito
FROM consulta_objetivo
WHERE Objetivo_escaneos <> 0