from docxtpl import DocxTemplate,InlineImage
from docx.shared import Cm, Mm, Inches  # Para definir el tamaño
import os
from datetime import datetime
import requests
import io


def generate_word(BASE_DIR,RAW_DATA):

    # Rutas de entrada
    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates', 'master_template.docx')
    
    OUTPUT_DIR,OUTPUT_FILE = generate_directory(BASE_DIR,TEMPLATE_PATH)

    # 3. CARGA DE LA PLANTILLA
    try:
        doc = DocxTemplate(TEMPLATE_PATH)
    except Exception as e:
        print(f"❌ Cannot open Word Template: {e}")
        return

    ########################################
    # 4. PROCESAMIENTO DE IMÁGENES
    # Iteramos sobre los datos para convertir URLs en objetos de imagen de Word
    print("🖼️ Procesando imágenes (esto puede tardar unos segundos)...")
    
    items_para_reporte = []
    
    for idx, item in enumerate(RAW_DATA):
        # Creamos una copia del diccionario para no modificar la data original
        item_procesado = item.copy()
        
        # Obtenemos la URL de la columna 'image_url' (ajusta este nombre según tu Excel)
        url_imagen = item.get('image_url', '')
        

        # Llamamos a la función de process_image
        # Ajustar tamaño de imagen en Cm
        size = 3

        image_obj = process_image(url_imagen,doc,size)
        # Guardamos el objeto imagen en una nueva clave que usarás en Word: {{ item.imagen_renderizada }}
        item_procesado['imagen_renderizada'] = image_obj
        
        items_para_reporte.append(item_procesado)
        print(f"   - Procesado item {idx+1}/{len(RAW_DATA)}: {item.get('box_id', 'Sin ID')}")

    # 5. RENDERIZADO
    context = {
        'titulo': 'QUALITY CONTROL',
        'fecha_generacion': datetime.now().strftime("%d-%m-%Y"),
        'usuario': 'Analista BI',
        'items': items_para_reporte,  # Esta es la clave que usas en el loop {%tr for item in items %}
    }

    print("⚙️ Renderizando documento Word...")
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
    
    return

def generate_directory(BASE_DIR,TEMPLATE_PATH):
    
    # Verificar existencia de plantilla
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ ERROR: No se encontró la plantilla en: {TEMPLATE_PATH}")
        print("   Por favor crea la carpeta 'templates' y pon tu archivo 'master_template.docx' ahí.")
        return
    else:
        # Rutas de salida (creamos carpeta con fecha actual para orden)
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        OUTPUT_DIR = os.path.join(BASE_DIR, 'output', fecha_hoy)
        OUTPUT_FILE = os.path.join(OUTPUT_DIR, f'Reporte_Calidad_{fecha_hoy}.docx')

        # Crear directorio de salida si no existe
        os.makedirs(OUTPUT_DIR, exist_ok=True)


        return OUTPUT_DIR,OUTPUT_FILE




def process_image(image_url,doc,size = 5):

    response = requests.get(image_url)

    if response.status_code == 200:
        image_stream = io.BytesIO(response.content)
        image_obj = InlineImage(doc, image_stream, width=Cm(size))

    return image_obj





