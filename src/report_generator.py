from docxtpl import DocxTemplate,InlineImage
from docx.shared import Cm, Mm, Inches  # Para definir el tamaño
import os
from datetime import datetime
import requests
import io


def generate_word(BASE_DIR,RAW_DATA,RAW_DATA_DETALLES):

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

    # Descomentar para depurar
    #print(RAW_DATA)   
    
    for idx, item in enumerate(RAW_DATA):

        
        
        # Creamos una copia del diccionario para no modificar la data original

        item_procesado = item.copy()
        
        # Obtenemos la URL de la columna 'image_url' (ajusta este nombre según tu Excel)
        url_foto_etiqueta = item.get('foto_etiqueta', '')
        url_foto_open     = item.get('foto_open', '')
        url_foto_open2    = item.get('foto_open2', '')
        url_foto_bandeja  = item.get('foto_bandeja','')
        url_foto_partida  = item.get('foto_frutapartida','')
        url_foto_defecto1 = item.get('foto_defecto1','')
        url_foto_defecto2 = item.get('foto_defecto2','')
        # Llamamos a la función de process_image
        # Ajustar tamaño de imagen en Cm
        size = 3.5

        image_etiqueta = process_image(url_foto_etiqueta,doc,size)
        image_open     = process_image(url_foto_open,doc,size)
        image_open2    = process_image(url_foto_open2,doc,size)
        image_bandeja  = process_image(url_foto_bandeja,doc,size)
        image_partida  = process_image(url_foto_partida,doc,size)
        if url_foto_defecto1 != "":
            image_defecto1 = process_image(url_foto_defecto1,doc,size)
            item_procesado['foto_defecto1'] = image_defecto1
        if url_foto_defecto2 != "":
            image_defecto2 = process_image(url_foto_defecto2,doc,size)
            item_procesado['foto_defecto2'] = image_defecto2
        
        # Guardamos el objeto imagen en una nueva clave que usarás en Word: {{ item.imagen_renderizada }}
        item_procesado['foto_open']     = image_open
        item_procesado['foto_open2']    = image_open2
        item_procesado['foto_etiqueta'] = image_etiqueta
        item_procesado['foto_bandeja']  = image_bandeja
        item_procesado['foto_partida']  = image_partida
        
        

    

        items_para_reporte.append(item_procesado)
        print(f"   - Procesado item {idx+1}/{len(RAW_DATA)}: {item.get('box_id', 'Sin ID')}")
    
    detalles = {}
    i = 0
    for diccionario in RAW_DATA_DETALLES:
        dic = f"dict_{i}"
        lista = []
        for _,value in diccionario.items():
            lista.append(value)
        detalles[dic] = lista
        i+=1

    print(detalles)
    # 5. RENDERIZADO
    context = {
        'titulo': 'QUALITY CONTROL',
        'fecha_generacion': datetime.now().strftime("%d-%m-%Y"),
        'usuario': 'Analista BI',
        'columnas':["Box Id","Soft","Wound","Bruise","Stain","Cracking","No Stem",
                    "Pitting","Decay","Avg Brix","Firmness","Open"],
        'columnas2':["Box Id","Producer","csg","Lot","Variety","Packing Date","Evaluation Date","Package","Label","Size"],
        'items': items_para_reporte,  # Esta es la clave que usas en el loop {%tr for item in items %}
        'details':detalles
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

    if image_url is not None:
        response = requests.get(image_url) 

        if response.status_code == 200:
            image_stream = io.BytesIO(response.content)
            image_obj = InlineImage(doc, image_stream, width=Cm(size))
    else:
        image_obj = image_url
    return image_obj





