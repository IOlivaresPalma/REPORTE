import os
import sys

# --- IMPORTACIÓN DE MÓDULOS PROPIOS ---
# Aseguramos que Python encuentre la carpeta 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

# Se importan archivos desde el file

try:
    # Intenta importar tus módulos si ya creaste los archivos
    from load_data import cargar_datos_excel,get_data
    from get_image import obtener_imagen_procesada
    from report_generator import generate_word,generate_directory
except ImportError:
    # FALLBACK: Si aún no creas los archivos en /src, usamos estas funciones dummy
    # para que el script corra sin errores ahora mismo.
    print("⚠️ ALERTA: Usando funciones de prueba (Módulos src no encontrados)")




def main():

    fecha_filtro = input("Ingrese fecha de registro en formato YYYY-MM-DD: ")
    
    # 1. CONFIGURACIÓN DE RUTAS
    # Usamos rutas relativas para que funcione en cualquier PC
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Rutas de entrada
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'datos_calidad.xlsx') # Tu excel real
    
    
    print("--- INICIANDO PROCESO DE GENERACIÓN DE REPORTE ---")


    # 2. CARGA DE DATOS
    try:
        print(f"📥 Cargando datos...")
        # Si usas el Excel real, descomenta la siguiente línea y asegúrate que el archivo existe
        # datos_crudos = cargar_datos_excel(DATA_PATH) 
        
        # Por ahora usamos el fallback/simulación si no hay excel
        RAW_DATA = get_data(fecha_filtro)
        
        print(f"   ✅ Se cargaron {len(RAW_DATA)} registros.")
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return

    
    generate_word(BASE_DIR,RAW_DATA)

    print("Informe generado - prueba v0.1.1")
    
    
if __name__ == "__main__":
    main()




