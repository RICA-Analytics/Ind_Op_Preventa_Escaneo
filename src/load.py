from DAToolKit import db
import pandas as pd

def load_ind_op(df_ind_op, anio, mes ,quincenas_delete):
    db.create_engine(f'DA4-Comercial', trusted_connection=True)
    db.insert_delete(df=df_ind_op, 
                     alias=f'DA4-Comercial', 
                     table_name='Ind_Op_Preventa_Escaneo', 
                     schema='dbo',
                     where_clause=f"Anio = {anio} AND Mes = {mes} AND Quincena IN ({quincenas_delete})")