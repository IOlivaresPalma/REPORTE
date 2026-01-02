import pyodbc
import dotenv

def get_data():

    connection = pyodbc.connect(driver = "{SQL Server}",server="10.10.2.55\QBIZ_TEST",database = "datascope",uid = "calidad_datascope",pwd = "Temp#Calidad2025!")
    cur = connection.cursor()
    db_cmd = "SELECT * FROM dbo.v_CONTRAMUESTRAS"
    res = cur.execute(db_cmd)
    for r in res:
        print(r)

    return

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
    