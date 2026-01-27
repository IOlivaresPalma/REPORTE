import os
import sys

# --- IMPORTACIÓN DE MÓDULOS PROPIOS ---

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

# Se importan archivos desde el file

try:
    # Importar codigos src
    from src.load_data import cargar_datos_excel,get_data
    from src.get_image import obtener_imagen_procesada
    from src.report_generator import generate_word,generate_directory
except ImportError:
    
    print("ALERTA: Usando funciones de prueba (Módulos src no encontrados)")


def generador(fechas_seleccionadas, filtro_var,especie,callback_progreso):

    print(fechas_seleccionadas, filtro_var, especie)
    
    lista_fechas = fechas_seleccionadas
    

    # 1. CONFIGURACIÓN DE RUTAS
    # Usamos rutas relativas para que funcione en cualquier PC
    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Detectar si estamos en el ejecutable o en desarrollo
    if getattr(sys, 'frozen', False):
        # Si es .exe, usamos la carpeta temporal interna (_MEIPASS)
        BASE_DIR = sys._MEIPASS
    else:
        # Si es desarrollo, usamos la ruta del archivo actual
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Rutas de entrada
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'datos_calidad.xlsx') # Tu excel real
    
    
    print("--- INICIANDO PROCESO DE GENERACIÓN DE REPORTE ---")


    # 2. CARGA DE DATOS
    try:
        print(f" Cargando datos...")
        # Cargar datos de condicion de fruta y detalle de cajas
        RAW_DATA_CONDICION,RAW_DATA_DETALLES = get_data(lista_fechas,filtro_var)
        
        print(f"    Se cargaron {len(RAW_DATA_CONDICION)} registros.")
    except Exception as e:
        print(f" Error cargando datos: {e}")
        return

    
    generate_word(BASE_DIR,RAW_DATA_CONDICION,RAW_DATA_DETALLES,callback_progreso)

    #print("Informe generado - prueba v0.1.1")
    
    
'''
if __name__ == "__main__":
    main()
    print("Proceso finalizado.")
    input("Presiona ENTER para salir...")

'''

