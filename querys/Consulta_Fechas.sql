
SELECT 
	CONVERT(date, {operador}(Fecha_operacion)) AS Fecha
  FROM [Comercial].[dbo].[Ind_Op]
  WHERE YEAR (Fecha_operacion) = {anio} AND MONTH (Fecha_operacion) = {mes}