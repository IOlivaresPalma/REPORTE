import os
import sys
from datetime import datetime
from docxtpl import DocxTemplate,InlineImage
import requests
from docx.shared import Cm, Mm, Inches  # Para definir el tamaño
import io

# --- IMPORTACIÓN DE MÓDULOS PROPIOS ---
# Aseguramos que Python encuentre la carpeta 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)
'''
try:
    # Intenta importar tus módulos si ya creaste los archivos
    from data_loader import cargar_datos_excel
    from image_handler import obtener_imagen_procesada
except ImportError:
    # FALLBACK: Si aún no creas los archivos en /src, usamos estas funciones dummy
    # para que el script corra sin errores ahora mismo.
    print("⚠️ ALERTA: Usando funciones de prueba (Módulos src no encontrados)")
'''
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
    
def obtener_imagen_procesada(doc, url, width=40):


    return " [FOTO] " # Placeholder si no tienes image_handler.py aun

def main():

    # 1. CONFIGURACIÓN DE RUTAS
    # Usamos rutas relativas para que funcione en cualquier PC
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Rutas de entrada
    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates', 'master_template.docx')
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'datos_calidad.xlsx') # Tu excel real
    
    # Rutas de salida (creamos carpeta con fecha actual para orden)
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output', fecha_hoy)
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, f'Reporte_Calidad_{fecha_hoy}.docx')

    # Verificar existencia de plantilla
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ ERROR: No se encontró la plantilla en: {TEMPLATE_PATH}")
        print("   Por favor crea la carpeta 'templates' y pon tu archivo 'master_template.docx' ahí.")
        return

    # Crear directorio de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("--- INICIANDO PROCESO DE GENERACIÓN DE REPORTE ---")


    # 2. CARGA DE DATOS
    try:
        print(f"📥 Cargando datos...")
        # Si usas el Excel real, descomenta la siguiente línea y asegúrate que el archivo existe
        # datos_crudos = cargar_datos_excel(DATA_PATH) 
        
        # Por ahora usamos el fallback/simulación si no hay excel
        datos_crudos = cargar_datos_excel(None) 
        
        print(f"   ✅ Se cargaron {len(datos_crudos)} registros.")
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return

    # 3. CARGA DE LA PLANTILLA
    try:
        doc = DocxTemplate(TEMPLATE_PATH)
    except Exception as e:
        print(f"❌ Error abriendo la plantilla Word: {e}")
        return

    # 4. PROCESAMIENTO DE IMÁGENES
    # Iteramos sobre los datos para convertir URLs en objetos de imagen de Word
    print("🖼️ Procesando imágenes (esto puede tardar unos segundos)...")
    
    items_para_reporte = []
    
    for idx, item in enumerate(datos_crudos):
        # Creamos una copia del diccionario para no modificar la data original
        item_procesado = item.copy()
        
        # Obtenemos la URL de la columna 'image_url' (ajusta este nombre según tu Excel)
        url_imagen = item.get('image_url', '')
        response = requests.get(url_imagen)

        if response.status_code == 200:
            image_stream = io.BytesIO(response.content)
            imagen_objeto = InlineImage(doc, image_stream, width=Cm(5))

        # Llamamos a tu función de image_handler
        # Ajusta ancho_mm según el ancho de tu columna en Word
        #imagen_objeto = obtener_imagen_procesada(doc, url_imagen)
        
        # Guardamos el objeto imagen en una nueva clave que usarás en Word: {{ item.imagen_renderizada }}
        item_procesado['imagen_renderizada'] = imagen_objeto
        
        items_para_reporte.append(item_procesado)
        print(f"   - Procesado item {idx+1}/{len(datos_crudos)}: {item.get('box_id', 'Sin ID')}")

    # 5. RENDERIZADO
    context = {
        'titulo': 'REPORTE DE CONTROL DE CALIDAD',
        'fecha_generacion': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'usuario': 'Analista BI',
        'items': items_para_reporte,  # Esta es la clave que usas en el loop {%tr for item in items %}
    }

    print("⚙️ Renderizando documento Word...")
    doc.render(context)
        
    # 6. GUARDADO
    doc.save(OUTPUT_FILE)
    print(f"✅ ¡ÉXITO! Reporte guardado en:\n   {OUTPUT_FILE}")
    
    # Opcional: Abrir la carpeta automáticamente (solo Windows)
    os.startfile(OUTPUT_DIR)
    '''
    try:
        doc.render(context)
        
        # 6. GUARDADO
        doc.save(OUTPUT_FILE)
        print(f"✅ ¡ÉXITO! Reporte guardado en:\n   {OUTPUT_FILE}")
        
        # Opcional: Abrir la carpeta automáticamente (solo Windows)
        os.startfile(OUTPUT_DIR)
        
    except Exception as e:
        print(f"❌ Error al guardar el documento final: {e}")
        print("   (Sugerencia: Cierra el archivo Word si lo tienes abierto)")
    '''
if __name__ == "__main__":
    main()
