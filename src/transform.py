import pandas as pd
from datetime import datetime
import csv
from pathlib import Path
import subprocess
import os
import glob

def quitar_acentos(texto):
        if pd.isna(texto):
            return texto
        texto = str(texto)

        reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "ñ": "n", "Ñ": "N",
        "ü": "u", "Ü": "U"
        }

        for acento, normal in reemplazos.items():
            texto = texto.replace(acento, normal)
        return texto

def calcular_shipto(row):

    if row['Source_Ship_To_Code'].startswith('P'):
        return 'IS P'
    elif row['Source_Ship_To_Code'].startswith('S'):
        return 'IS SOL'
    else:
        return 'NOT P'

def calcular_shiptoKO_All_P_SinP(row):
    if  calcular_shipto(row) == "IS P":
        return row['Source_Ship_To_Code'][1:]  
    return row['Source_Ship_To_Code'] 

def mid(cadena, inicio, longitud):
    return cadena[inicio-1:inicio-1+longitud] 

def safe_char(text, index):
    return text[index] if len(text) > index else ""

def calcular_ShiptoKO_All(row):

    if row ['Ship_To_Type'] != "Resto del Mercado":
        return row['Source_Ship_To_Code']
    
    else:

        if calcular_shipto(row) == 'IS P':

            shipto_sinp = calcular_shiptoKO_All_P_SinP(row).strip()

            extP_1 = mid(shipto_sinp, 1, 1)
            extP_2 = mid(shipto_sinp, 2, 1)
            extP_3 = mid(shipto_sinp, 3, 1)
            extP_4 = mid(shipto_sinp, 4, 1) or None
            extP_5 = mid(shipto_sinp, 5, 1) or None
            extP_6 = mid(shipto_sinp, 6, 1) or None

            if extP_4 is None:
                extP_4 = { "1": "8", "2": "7", "3": "1", "4": "2", "5": "6", "6": "5", "7": "9", "8": "0", "9": "3", "0": "4"}.get(extP_3, None)

            if extP_5 is None:
                extP_5 = { "1": "6", "2": "3", "3": "0", "4": "1", "5": "8", "6": "4", "7": "2", "8": "9", "9": "7", "0": "5"}.get(extP_4, None)
                
            if extP_6 is None:
                extP_6_nr = { "1": "4", "2": "5", "3": "8", "4": "0", "5": "9", "6": "1", "7": "3", "8": "7", "9": "6", "0": "2"}.get(extP_5, None)
            
            rdm_1_map = {"1": "7", "2": "1", "3": "6", "4": "3", "5": "0", "6": "9", "7": "5", "8": "8", "9": "2", "0": "4"}
            rdm_2_map = {"1": "2", "2": "7", "3": "5", "4": "8", "5": "9", "6": "1", "7": "4", "8": "0", "9": "6", "0": "3"}
            rdm_3_map = {"1": "3", "2": "9", "3": "4", "4": "7", "5": "2", "6": "5", "7": "0", "8": "7", "9": "1", "0": "6"}
            rdm_4_map = {"1": "0", "2": "4", "3": "7", "4": "5", "5": "8", "6": "2", "7": "9", "8": "6", "9": "3", "0": "1"}
            rdm_5_map = {"1": "5", "2": "0", "3": "1", "4": "9", "5": "3", "6": "7", "7": "6", "8": "2", "9": "4", "0": "8"}
            rdm_6_map = {"1": "6", "2": "3", "3": "2", "4": "1", "5": "7", "6": "4", "7": "8", "8": "9", "9": "5", "0": "0"}

            rdm_1 = rdm_1_map.get(extP_1, None)
            rdm_2 = rdm_2_map.get(extP_2, None)
            rdm_3 = rdm_3_map.get(extP_3, None)
            rdm_4 = rdm_4_map.get(extP_4, None)
            rdm_5 = rdm_5_map.get(extP_5, None)
            rdm_6 = rdm_6_map.get(extP_6, None)

            if extP_6 is None:
                ShiptoKO_All_P = f"{rdm_4}{rdm_3}{extP_1}{rdm_1}{rdm_5}{rdm_6}{rdm_2}"

            else:
                ShiptoKO_All_P = f"{rdm_4}{rdm_3}{extP_1}{rdm_1}{rdm_5}{rdm_6}{rdm_2}"

            prefix_map = {'02429': '005', '02805': '006'}
            prefix = prefix_map.get(row['Source_Ship_From_Code'], "")
            return prefix + ShiptoKO_All_P
        
        elif calcular_shipto(row) == 'IS SOL':
            #Calculo de las variables
            extSol_1 = row['Source_Ship_To_Code'][0]   # MID(Solicitante, 1, 1)
            extSol_2 = row['Source_Ship_To_Code'][1]   # MID(Solicitante, 2, 1)
            extSol_3 = row['Source_Ship_To_Code'][2]   # MID(Solicitante, 3, 1)
            extSol_4 = row['Source_Ship_To_Code'][3]   # MID(Solicitante, 4, 1)
            extSol_5 = row['Source_Ship_To_Code'][4]   # MID(Solicitante, 5, 1)
            extSol_6 = row['Source_Ship_To_Code'][5]   # MID(Solicitante, 6, 1)
            extSol_7 = row['Source_Ship_To_Code'][6]   # MID(Solicitante, 7, 1)

            rdmSol_1_map = {"A": "8", "B": "6", "C": "6", "D": "1", "E": "0", "F": "9", "G": "9", 
            "H": "6", "I": "4", "J": "0", "K": "1", "L": "9", "M": "4", "N": "1", 
            "Ñ": "2", "O": "6", "P": "1", "Q": "0", "R": "4", "S": "2", "T": "2", 
            "U": "7", "V": "6", "W": "2", "X": "5", "Y": "5", "Z": "7", "a": "5", 
            "b": "0", "c": "6", "d": "7", "e": "7", "f": "5", "g": "8", "h": "4", 
            "i": "4", "j": "2", "k": "5", "l": "0", "m": "0", "n": "8", "ñ": "4", 
            "o": "7", "p": "3", "q": "2", "r": "7", "s": "5", "t": "8", "u": "8", 
            "v": "6", "w": "3", "x": "6", "y": "4", "z": "0", "1": "1", "2": "6", 
            "3": "0", "4": "4", "5": "4", "6": "7", "7": "9", "8": "1", "9": "7", 
            "0": "8"}

            rdmSol_2_map = {"A": "9", "B": "3", "C": "7", "D": "6", "E": "5", "F": "6", "G": "9", 
            "H": "9", "I": "8", "J": "5", "K": "3", "L": "1", "M": "0", "N": "9", 
            "Ñ": "6", "O": "6", "P": "6", "Q": "2", "R": "8", "S": "2", "T": "3", 
            "U": "5", "V": "3", "W": "5", "X": "2", "Y": "6", "Z": "9", "a": "1", 
            "b": "4", "c": "2", "d": "3", "e": "4", "f": "9", "g": "9", "h": "9", 
            "i": "3", "j": "5", "k": "3", "l": "5", "m": "0", "n": "3", "ñ": "2", 
            "o": "2", "p": "2", "q": "3", "r": "1", "s": "7", "t": "8", "u": "6", 
            "v": "7", "w": "4", "x": "7", "y": "7", "z": "2", "1": "4", "2": "3", 
            "3": "2", "4": "5", "5": "5", "6": "2", "7": "7", "8": "5", "9": "8", 
            "0": "3"}

            rdmSol_3_map = {"A": "5", "B": "6", "C": "6", "D": "3", "E": "1", "F": "6", "G": "1", 
            "H": "7", "I": "7", "J": "4", "K": "5", "L": "6", "M": "7", "N": "0", 
            "Ñ": "8", "O": "1", "P": "9", "Q": "8", "R": "5", "S": "1", "T": "9", 
            "U": "2", "V": "5", "W": "4", "X": "9", "Y": "0", "Z": "3", "a": "0", 
            "b": "8", "c": "8", "d": "4", "e": "2", "f": "2", "g": "9", "h": "8", 
            "i": "4", "j": "0", "k": "2", "l": "0", "m": "0", "n": "1", "ñ": "1", 
            "o": "3", "p": "5", "q": "2", "r": "0", "s": "6", "t": "7", "u": "1", 
            "v": "8", "w": "3", "x": "4", "y": "3", "z": "1", "1": "1", "2": "8", 
            "3": "0", "4": "1", "5": "4", "6": "8", "7": "7", "8": "3", "9": "2", 
            "0": "1"}

            rdmSol_4_map = {"A": "6", "B": "9", "C": "7", "D": "0", "E": "1", "F": "0", "G": "1", 
            "H": "3", "I": "0", "J": "9", "K": "6", "L": "8", "M": "0", "N": "0", 
            "Ñ": "3", "O": "3", "P": "1", "Q": "8", "R": "5", "S": "5", "T": "4", 
            "U": "7", "V": "2", "W": "5", "X": "1", "Y": "9", "Z": "0", "a": "4", 
            "b": "8", "c": "4", "d": "6", "e": "5", "f": "9", "g": "1", "h": "6", 
            "i": "0", "j": "9", "k": "2", "l": "6", "m": "2", "n": "5", "ñ": "3", 
            "o": "8", "p": "2", "q": "1", "r": "2", "s": "8", "t": "6", "u": "6", 
            "v": "9", "w": "6", "x": "1", "y": "0", "z": "6", "1": "6", "2": "6", 
            "3": "2", "4": "5", "5": "4", "6": "4", "7": "0", "8": "2", "9": "3", 
            "0": "2"}

            rdmSol_5_map = {"A": "5", "B": "2", "C": "0", "D": "5", "E": "9", "F": "0", "G": "1", 
            "H": "9", "I": "3", "J": "7", "K": "9", "L": "6", "M": "2", "N": "5", 
            "Ñ": "0", "O": "0", "P": "6", "Q": "8", "R": "1", "S": "6", "T": "1", 
            "U": "3", "V": "4", "W": "9", "X": "9", "Y": "5", "Z": "7", "a": "3", 
            "b": "5", "c": "7", "d": "7", "e": "9", "f": "3", "g": "5", "h": "7", 
            "i": "9", "j": "1", "k": "7", "l": "8", "m": "4", "n": "8", "ñ": "7", 
            "o": "3", "p": "7", "q": "9", "r": "2", "s": "5", "t": "0", "u": "5", 
            "v": "8", "w": "6", "x": "5", "y": "2", "z": "5", "1": "2", "2": "3", 
            "3": "8", "4": "0", "5": "1", "6": "5", "7": "4", "8": "0", "9": "4", 
            "0": "3"}

            rdmSol_6_map = {"A": "5", "B": "6", "C": "0", "D": "9", "E": "1", "F": "3", "G": "4", 
            "H": "3", "I": "0", "J": "5", "K": "7", "L": "0", "M": "0", "N": "7", 
            "Ñ": "1", "O": "2", "P": "0", "Q": "3", "R": "2", "S": "7", "T": "5", 
            "U": "7", "V": "9", "W": "6", "X": "9", "Y": "8", "Z": "4", "a": "7", 
            "b": "4", "c": "6", "d": "0", "e": "4", "f": "7", "g": "4", "h": "0", 
            "i": "2", "j": "7", "k": "0", "l": "0", "m": "8", "n": "1", "ñ": "5", 
            "o": "7", "p": "2", "q": "9", "r": "4", "s": "2", "t": "9", "u": "0", 
            "v": "1", "w": "5", "x": "9", "y": "1", "z": "5", "1": "7", "2": "8", 
            "3": "7", "4": "9", "5": "8", "6": "0", "7": "1", "8": "6", "9": "0", 
            "0": "9"}

            rdmSol_7_map = {"A": "4", "B": "5", "C": "5", "D": "6", "E": "5", "F": "4", "G": "2", 
            "H": "8", "I": "1", "J": "7", "K": "2", "L": "6", "M": "8", "N": "3", 
            "Ñ": "9", "O": "6", "P": "4", "Q": "0", "R": "2", "S": "9", "T": "8", 
            "U": "8", "V": "5", "W": "7", "X": "5", "Y": "4", "Z": "9", "a": "7", 
            "b": "6", "c": "5", "d": "4", "e": "7", "f": "3", "g": "6", "h": "2", 
            "i": "6", "j": "1", "k": "7", "l": "1", "m": "9", "n": "4", "ñ": "6", 
            "o": "7", "p": "1", "q": "3", "r": "9", "s": "2", "t": "4", "u": "8", 
            "v": "6", "w": "1", "x": "9", "y": "8", "z": "7", "1": "4", "2": "6", 
            "3": "2", "4": "1", "5": "6", "6": "8", "7": "1", "8": "7", "9": "4", 
            "0": "1"}    

            rdmSol_1 = rdmSol_1_map.get(extSol_1, None)
            rdmSol_2 = rdmSol_2_map.get(extSol_2, None)
            rdmSol_3 = rdmSol_3_map.get(extSol_3, None)
            rdmSol_4 = rdmSol_4_map.get(extSol_4, None)
            rdmSol_5 = rdmSol_5_map.get(extSol_5, None)
            rdmSol_6 = rdmSol_6_map.get(extSol_6, None)
            rdmSol_7 = rdmSol_7_map.get(extSol_7, None)

            rdmSol_1
            rdmSol_2
            rdmSol_3
            rdmSol_4
            rdmSol_5
            rdmSol_6
            rdmSol_7

            ShiptoKO_All_Sol = f"{rdmSol_3}{rdmSol_7}{rdmSol_1}{rdmSol_4}{rdmSol_2}{rdmSol_5}{rdmSol_6}"

            prefix_map = {'02429': '005', '02805': '006'}
            prefix = prefix_map.get(row['Source_Ship_From_Code'], "")
            return prefix + ShiptoKO_All_Sol
    
        elif calcular_shipto(row) == 'NOT P':

            long_1 = row ['Source_Ship_To_Code'][:5] # Trae los primeros 5 caracteres
            long_2 = row ['Source_Ship_To_Code'][:7]
            long_3 = row ['Source_Ship_To_Code'][:9]

            long_1_v = long_1[-2:]
            long_2_v = long_2[-2:]
            long_3_v = long_3[-2:]
            long_4_v = row ['Source_Ship_To_Code'][-1:]

            ShiptoKO_All_NotP = f"{long_4_v}{long_2_v}{long_1_v}{long_3_v}"
            
            prefix_map = {'02429': '005', '02805': '006'}
            prefix = prefix_map.get(row['Source_Ship_From_Code'], "")
            return prefix + ShiptoKO_All_NotP
        
def encriptar_solicitantes (df):

    df['Source_Ship_To_Code_Encrypt'] = df.apply(calcular_ShiptoKO_All, axis=1)

    return df

def primer_orden_shipto (df_shipto):

    columnas_shipto = [
       "Source_Ship_From_Code"            
      ,"Source_Ship_To_Code" # Se elimina para el reporte final
      ,"Source_Ship_To_Code_Encrypt"
      ,"Vending_Machine_Code"
      ,"Vending_Machine_Location_Code"
      ,"Source_Ship_To_Desc"
      ,"Source_Channel_Code"
      ,"Source_Customer_Code"
      ,"Ship_To_Type" # Se elimina para el reporte final
      ,"Ship_To_Adress_1"
      ,"Attribute_2"
      ,"Ship_To_Oficial_Number"
      ,"Ship_To_City"
      ,"Ship_To_State"
      ,"Ship_To_Country"
      ,"Ship_To_Postal_Code"
      ,"Ship_To_Latitude"
      ,"Ship_To_Longitude"
      ]
    
    columnas_insertar_shipto = [col for col in columnas_shipto if col in df_shipto.columns]
    df_shipto = df_shipto[columnas_insertar_shipto]

    return df_shipto

def segundo_orden_shipto (df_shipto):

    columnas_shipto = [         
      "Source_Ship_To_Code_Encrypt"
      ,"Vending_Machine_Code"
      ,"Vending_Machine_Location_Code"
      ,"Source_Ship_To_Desc"
      ,"Source_Customer_Code"
      ,"Ship_To_Adress_1"
      ,"Attribute_2"
      ,"Ship_To_Oficial_Number"
      ,"Ship_To_City"
      ,"Ship_To_State"
      ,"Ship_To_Country"
      ,"Ship_To_Postal_Code"
      ,"Ship_To_Latitude"
      ,"Ship_To_Longitude"
      ]
    
    columnas_insertar_shipto = [col for col in columnas_shipto if col in df_shipto.columns]
    df_shipto = df_shipto[columnas_insertar_shipto]

    return df_shipto