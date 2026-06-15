from DAToolKit import db
import pandas as pd

def load_table(alias_servidor_destino, trusted_connection_destino, esquema_destino, tabla_destino, df, anio_delete, mes_delete ):
    db.create_engine(alias_servidor_destino, trusted_connection=trusted_connection_destino)
    db.insert_delete(df=df, 
                     alias=alias_servidor_destino, 
                     table_name=tabla_destino, 
                     schema=esquema_destino,
                     where_clause=f"[Anio] = {anio_delete} AND [Mes] = '{mes_delete}'")   