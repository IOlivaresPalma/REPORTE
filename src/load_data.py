import pyodbc
from dotenv import dotenv_values

def get_data():

    config = dotenv_values(".env")
    
    connection = pyodbc.connect(driver = "{SQL Server}",server=config["DB_HOST"],database = config["DB_NAME"],uid = config["DB_USER"],pwd = config["DB_PASSWORD"])
    cur = connection.cursor()
    db_cmd = "SELECT * FROM dbo.v_CONTRAMUESTRAS where g_tipo_muestra = 'CONTRAMUESTRA' and d_codigo_caja != '' and foto_defecto != '' and fecha_registro= '2025-12-31'"
    res = cur.execute(db_cmd)

    RAW_DATA = []

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
                       'foto_defecto2' : ''
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
        condicion_fruta['avg_brix']= caja[43]
        
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


        # Descomentar para depurar
        #print("foto 1: ",condicion_fruta['foto_defecto1'])
        #print("foto 2: ",condicion_fruta['foto_defect2'])
        RAW_DATA.append(condicion_fruta)
    
    return RAW_DATA

def cargar_datos_excel(path):
    # Datos simulados basados en tu captura de pantalla
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
    