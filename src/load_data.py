import pyodbc
from dotenv import dotenv_values,load_dotenv
import psycopg2
import datetime
from datetime import datetime
import os

def get_data(fecha_registro="2025-01-01",variedad="TODAS"):

    load_dotenv(os.path.join(os.getcwd(), ".env"))
    config = dotenv_values(".env")
    
    #RAW_DATA_CONDICION,LISTA_CAJAS = get_sqlServer_data(config,fecha_registro)

    #RAW_DATA_DETALLES= get_postgres_data(LISTA_CAJAS,config)

    RAW_DATA_CONDICION,RAW_DATA_DETALLES = get_postgres_data_test(fecha_registro,config,variedad)
    
    #print("Depurando")
    '''
    for i in RAW_DATA_CONDICION:
        #print(i)
        for j in RAW_DATA_DETALLES:
            #print(j)
            if j['Box_Id'] == i['box_id']:
                j['Evaluation_Date'] = i['fecha_registro']
    '''
    
    return RAW_DATA_CONDICION,RAW_DATA_DETALLES



# Prueba de datos
def cargar_datos_excel(path):
    
    return [
        {
            'box_id': '30395715', 'producer': 'PRIZE PROSERVICE', 'csg': '178244',
            'lot': '000384', 'variety': 'LAPINS', 'packing_date': '27-11-2025',
            'evaluation_date': '29-12-2025', 'package': 'CMD5A', 'label': 'DISNEY',
            'size': '2JD', 'image_url': 'https://data-scope.s3.amazonaws.com/images/2025/12/105444/3de4073a5a4daaf46fafac7449714d2a.jpg'
        },
        {
            'box_id': '30395716', 'producer': 'AGROFRUTA LTDA', 'csg': '192833',
            'lot': '000385', 'variety': 'SANTINA', 'packing_date': '28-11-2025',
            'evaluation_date': '30-12-2025', 'package': 'CMD5A', 'label': 'GENERIC',
            'size': 'J', 'image_url': 'https://data-scope.s3.amazonaws.com/images/2025/12/105444/6d89ce1263cc795f2f2b8fceb4f6efed.jpg'
        }
    ]
    


def get_postgres_data_test(fecha_registro,config,variedad):
    from psycopg2 import OperationalError


    print("Prueba conexión postgresql")
    # Check server connection
    try:
        connection = psycopg2.connect(database = config["DB_NAME_POST"],
                                  user = config["DB_USER_POST"],
                                  host = config["DB_HOST_POST"],
                                  password = config["DB_PASSWORD_POST"],
                                  port = config["DB_PORT_POST"]
                                 )
        print("Conexión exitosa!")
    except OperationalError as e:
        print(f"No fue posible conectarse a la base de datos. Detalles: {e}")
        return False

    # Generación y ejecución de query
    cur = connection.cursor()
    #print("Depurando")
    db_cmd = CONTRAMUESTRAS_query_gen(fecha_registro,variedad)

    print(f"Ejecutando query: {db_cmd}")
    print("Extrayendo cajas de la base de datos...")
    cur.execute(db_cmd)
    rows = cur.fetchall()
    print("Extracción completada !")
    
    LISTA_LOTES = []
    CONDITION_RAW = []
    DETAIL_RAW    = []

    LISTA_VARIEDADES = []

    condicion_fruta_empty = {'box_id':'',
                       'soft':'',
                       'wound':'',
                       'bruise':'',
                       'stain':'',
                       'cracking':'',
                       'no_stem':'',
                       'pitting':'',
                       'decay':'',
                       'avg_brix':'',
                       'Firmness':'',
                       'open':'',
                       'foto_open':'',
                       'foto_open2':'',
                       'foto_etiqueta': '',
                       'foto_bandeja':'',
                       'foto_frutapartida':'',
                       'foto_defecto1':'',
                       'foto_defecto2' : '',
                       'fecha_registro': ''
                }

    detalles_caja = {"Box_Id":"",
                     "Producer":"",
                     "csg":"",
                     "Lot":"",
                     "Variety":"",
                     "Packing_Date":"",
                     "Evaluation_Date":"",
                     "Package":"",
                     "Label":"",
                     "Size":""
         
                    }

    # Adición de datos al diccionario
    for dato in rows:
        #print(dato)
        # Copia de los diccionarios para no sobreescribir
        condicion_fruta = condicion_fruta_empty.copy()
        caja_detail = detalles_caja.copy()

        # CONDICION DE FRUTA
        # ==============================================================
        condicion_fruta['box_id']  = dato[15]
        condicion_fruta['soft']    = str(dato[31])+" %"
        condicion_fruta['wound']   = str(dato[32])+" %"
        condicion_fruta['bruise']  = str(dato[33])+" %"
        condicion_fruta['stain']   = str(dato[34])+" %"
        condicion_fruta['cracking']= str(dato[35])+" %"
        condicion_fruta['no_stem'] = str(dato[36])+" %"
        condicion_fruta['pitting'] = str(dato[37])+" %"
        condicion_fruta['decay']   = str(dato[38])+" %"
        condicion_fruta['avg_brix']= round(dato[43],2)
        
        condicion_fruta['foto_open']=dato[22]
        condicion_fruta['foto_open2']=dato[24]
        condicion_fruta['foto_bandeja']=dato[41]
        condicion_fruta['foto_etiqueta']=dato[42]
        condicion_fruta['foto_frutapartida']=dato[25]

        defectos = dato[40].split(" | ")
        
        condicion_fruta['foto_defecto1']= defectos[0]
        if len(defectos) == 2:    
            condicion_fruta['foto_defecto2'] = defectos[1]

        match dato[20]:
            case "BUENO":
                    condicion_fruta['Firmness']= "GOOD"
            case "REGULAR":
                    condicion_fruta['Firmness']= "FAIR"
            case "MALO":
                    condicion_fruta['Firmness']= "POOR"
        
        
        match dato[21]:
            case "BUENO":
                    condicion_fruta['open']= "GOOD"
            case "REGULAR":
                    condicion_fruta['open']= "FAIR"
            case "MALO":
                    condicion_fruta['open']= "POOR"

        condicion_fruta['fecha_registro'] = dato[12]

        # ==============================================================
        # ==============================================================

        # DETALLES CAJA
        # ==============================================================
        caja_detail["Box_Id"]            = dato[15]
        caja_detail["Producer"]          = "PRIZE PROSERVICE"
        caja_detail["csg"]               = ""                    # Se rellena despues
        caja_detail["Lot"]               = dato[47]
        caja_detail["Variety"]           = dato[51]              # Variedad Timbrada
        caja_detail["Packing_Date"]      = dato[45].strftime("%Y-%m-%d") if dato[45] is not None else dato[45]
        caja_detail["Evaluation_Date"]   = dato[12]                    # Se saca de postgres
        caja_detail["Package"] = dato[-1]                        # codConfeccion
        caja_detail["Label"] = dato[52]                          # Marca
        caja_detail["Size"] = dato[53]                           # Calibre Timbrado
        

        #Se agrega variedad a la lista
        LISTA_VARIEDADES.append(dato[51])

        DETAIL_RAW.append(caja_detail)
        CONDITION_RAW.append(condicion_fruta)
        LISTA_LOTES.append(dato[47])
        # ===============================================================


    query = query_postgres_recepciones(LISTA_LOTES)
    print(f"Ejecutando query: {query}")

    cur.execute(query)
    rows = cur.fetchall()

    print("Extracción completada!")

    for diccionario in DETAIL_RAW:
        for row in rows:        
            if int(diccionario["Lot"]) == row[0]:
                diccionario["csg"] = row[1]
        
        #Descomentar para depurar
        #print(diccionario["Lot"],diccionario["csg"])
            

    # Cerrar conexión
    connection.commit()
    connection.close()
    return CONDITION_RAW,DETAIL_RAW





def get_postgres_data(LISTA_CAJAS,config):
    from psycopg2 import OperationalError


    print("Prueba conexión postgresql")
    # Check server connection
    try:
        connection = psycopg2.connect(database = config["DB_NAME_POST"],
                                  user = config["DB_USER_POST"],
                                  host = config["DB_HOST_POST"],
                                  password = config["DB_PASSWORD_POST"],
                                  port = config["DB_PORT_POST"]
                                 )
        print("Conexión exitosa!")
    except OperationalError as e:
        print(f"No fue posible conectarse a la base de datos. Detalles: {e}")
        return False

    # Generación y ejecución de query
    cur = connection.cursor()
    #print("Depurando")
    db_cmd = query_generator_postgres(LISTA_CAJAS)

    print(f"Ejecutando query: {db_cmd}")
    print("Extrayendo cajas de la base de datos...")
    cur.execute(db_cmd)
    rows = cur.fetchall()
    print("Extracción completada !")
    DETALLES_CAJAS = []
    LISTA_LOTES = []
    detalles_caja = {"Box_Id":"",
                     "Producer":"",
                     "csg":"",
                     "Lot":"",
                     "Variety":"",
                     "Packing_Date":"",
                     "Evaluation_Date":"",
                     "Package":"",
                     "Label":"",
                     "Size":""
         
                    }

    # Adición de datos al diccionario
    for dato in rows:
        #print(dato)
        caja_detail = detalles_caja.copy()
        caja_detail["Box_Id"]            = dato[0]
        caja_detail["Producer"]          = "PRIZE PROSERVICE"
        caja_detail["csg"]               = ""                    # Se rellena despues
        caja_detail["Lot"]               = dato[3]
        caja_detail["Variety"]           = dato[14]              # Variedad Timbrada
        caja_detail["Packing_Date"]      = dato[38].strftime("%m-%d-%y") if dato[38] is not None else dato[38]
        caja_detail["Evaluation_Date"]   = ""                    # Se saca de postgres
        caja_detail["Package"] = dato[19]                        # codConfeccion
        caja_detail["Label"] = dato[23]                          # Marca
        caja_detail["Size"] = dato[25]                           # Calibre Timbrado
        
        DETALLES_CAJAS.append(caja_detail)
        LISTA_LOTES.append(dato[3])

    

    query = query_postgres_recepciones(LISTA_LOTES)
    print(f"Ejecutando query: {query}")

    cur.execute(query)
    rows = cur.fetchall()

    print("Extracción completada!")

    for diccionario in DETALLES_CAJAS:
        for row in rows:        
            if int(diccionario["Lot"]) == row[0]:
                diccionario["csg"] = row[1]
        
        #Descomentar para depurar
        #print(diccionario["Lot"],diccionario["csg"])
            

    # Cerrar conexión
    connection.commit()
    connection.close()
    return DETALLES_CAJAS




def get_sqlServer_data(config,fecha_registro):
    
    connection = pyodbc.connect(driver = "{SQL Server}",server=config["DB_HOST"],database = config["DB_NAME"],uid = config["DB_USER"],pwd = config["DB_PASSWORD"])
    cur = connection.cursor()

    # Descomentar para depurar
    print(fecha_registro)
    db_cmd = query_generator_sqlServer(fecha_registro)
    #db_cmd = f"SELECT * FROM dbo.v_CONTRAMUESTRAS where g_tipo_muestra = 'CONTRAMUESTRA' and d_codigo_caja != '' and foto_defecto != '' and fecha_registro= '{fecha_registro}'"
    res = cur.execute(db_cmd)

    RAW_DATA = []
    LISTA_CAJAS = []

    condicion_fruta_empty = {'box_id':'',
                       'soft':'',
                       'wound':'',
                       'bruise':'',
                       'stain':'',
                       'cracking':'',
                       'no_stem':'',
                       'pitting':'',
                       'decay':'',
                       'avg_brix':'',
                       'Firmness':'',
                       'open':'',
                       'foto_open':'',
                       'foto_open2':'',
                       'foto_etiqueta': '',
                       'foto_bandeja':'',
                       'foto_frutapartida':'',
                       'foto_defecto1':'',
                       'foto_defecto2' : '',
                       'fecha_registro': ''
                }

    for caja in res:
        
        condicion_fruta = condicion_fruta_empty.copy()
        condicion_fruta['box_id']  = caja[15]
        condicion_fruta['soft']    = str(caja[31])+" %"
        condicion_fruta['wound']   = str(caja[32])+" %"
        condicion_fruta['bruise']  = str(caja[33])+" %"
        condicion_fruta['stain']   = str(caja[34])+" %"
        condicion_fruta['cracking']= str(caja[35])+" %"
        condicion_fruta['no_stem'] = str(caja[36])+" %"
        condicion_fruta['pitting'] = str(caja[37])+" %"
        condicion_fruta['decay']   = str(caja[38])+" %"
        condicion_fruta['avg_brix']= round(caja[43],2)
        
        condicion_fruta['foto_open']=caja[22]
        condicion_fruta['foto_open2']=caja[24]
        condicion_fruta['foto_bandeja']=caja[41]
        condicion_fruta['foto_etiqueta']=caja[42]
        condicion_fruta['foto_frutapartida']=caja[25]

        defectos = caja[40].split(" | ")
        
        condicion_fruta['foto_defecto1']= defectos[0]
        if len(defectos) == 2:    
            condicion_fruta['foto_defecto2'] = defectos[1]

        match caja[20]:
            case "BUENO":
                    condicion_fruta['Firmness']= "GOOD"
            case "REGULAR":
                    condicion_fruta['Firmness']= "FAIR"
            case "MALO":
                    condicion_fruta['Firmness']= "POOR"
        
        
        match caja[21]:
            case "BUENO":
                    condicion_fruta['open']= "GOOD"
            case "REGULAR":
                    condicion_fruta['open']= "FAIR"
            case "MALO":
                    condicion_fruta['open']= "POOR"

        condicion_fruta['fecha_registro'] = caja[12]

        # Descomentar para depurar
        #print("foto 1: ",condicion_fruta['foto_defecto1'])
        #print("foto 2: ",condicion_fruta['foto_defect2'])
        RAW_DATA.append(condicion_fruta)

        # Se agrega id de caja a lista
        LISTA_CAJAS.append(caja[15])
    
    
    return RAW_DATA,LISTA_CAJAS




def query_postgres_recepciones(LISTA_LOTES):

    lote_csg = {}
    lote_0 = int(LISTA_LOTES[0])
    query = f"SELECT lote,csg FROM raw.all_recepciones ar WHERE cod_temporada = 'T16' and cod_especie = 'CH' and cod_zona='P' and "
    query2 = f"(ar.lote = {lote_0}"
    i = 1
    while i < len(LISTA_LOTES):
        query2 += f" or ar.lote = {int(LISTA_LOTES[i])}"
        #print(f"proceso: {i}")
        i+=1
    query2 += ")"

    query+= query2


    return query



# REVISAR...
def query_generator_postgres(DETALLE_CAJA):
    
    col_name = 'c."codCaja"'
    if len(DETALLE_CAJA) == 0:
          print("No hay cajas que extraer de la base de datos")
    elif len(DETALLE_CAJA) == 1:
        query = f"SELECT * FROM raw.cl_pck_unitec_cajas c WHERE {col_name} = '{DETALLE_CAJA[0]}'"
        return query
    else:
        query = f"SELECT * FROM raw.cl_pck_unitec_cajas c WHERE {col_name} = '{DETALLE_CAJA[0]}'"
        i = 1
        while i < len(DETALLE_CAJA):
            query += f" or {col_name} = '{DETALLE_CAJA[i]}'"
            i+=1
    
    query+= ' ORDER BY c."codCaja" ASC'
    return query



def query_generator_sqlServer(fecha_registro):
    
    query = f"SELECT * FROM dbo.v_CONTRAMUESTRAS where g_tipo_muestra = 'CONTRAMUESTRA' and d_codigo_caja != '' and foto_defecto != '' and (fecha_registro = '{fecha_registro[0]}'"
    i = 1
    while i<len(fecha_registro):
        query += f" or fecha_registro = '{fecha_registro[i]}'"
        i+=1
    query += ") ORDER BY d_codigo_caja ASC"
    
    return query


def CONTRAMUESTRAS_query_gen(fecha_registro,variedad):

    #seleccion = input("Desea filtrar por variedad? (y/n) : ")
    seleccion = ",".join(f"'{x}'" for x in variedad)
    if seleccion != None:
        #variedad = input("Escriba variedad a filtrar: ")
        #variedad = variedad.upper()
        col_name = '"VariedadReal"'
        query = f"SELECT * FROM raw.contramuestra_destino cd where g_tipo_muestra = 'CONTRAMUESTRA' and {col_name} in ({seleccion}) and d_codigo_caja != '' and foto_defecto != '' and (fecha_registro = '{fecha_registro[0]}'" 
    else:
        query = f"SELECT * FROM raw.contramuestra_destino cd where g_tipo_muestra = 'CONTRAMUESTRA' and d_codigo_caja != '' and foto_defecto != '' and (fecha_registro = '{fecha_registro[0]}'" 
    
    i = 1
    while i<len(fecha_registro):
        query += f" or fecha_registro = '{fecha_registro[i]}'"
        i+=1
    query+= ") ORDER BY fecha_registro DESC"

    return query