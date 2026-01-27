import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sys
import os

# --- Importar tu lógica ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from generator import generador
except ImportError:
    # Simulación actualizada para aceptar lista de variedades
    def generador(fechas, lista_variedades, prod, callback_progreso=None):
        import time
        total = 5
        print(f"Simulación: Variedades seleccionadas: {lista_variedades}")
        for i in range(1, total + 1):
            time.sleep(0.5)
            if callback_progreso:
                callback_progreso(f"Procesando {i}/{total}...", i, total)

class AppFrutas(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Quality control")
        self.geometry("500x750") # Altura de ventana
        
        self.LISTA_VARIEDADES = [
            "AREKO", "BING", "KORDIA", "LAPINS", "PACIFIC RED", 
            "RAINIER", "REGINA", "ROYAL DAWN", "SANTINA", "SKEENA", 
            "STELLA", "SUMMIT", "SWEET ARYANA", "SWEETHEART", 
            "SYMPHONY", "VAN"
        ]
        
        self.LISTA_ESPECIE = ["CEREZA","NECTARIN"]

        self.fechas_seleccionadas = []
        # Variables de control para activar/desactivar filtros
        self.var_filtrar_variedad = tk.BooleanVar()
        #self.var_filtrar_productor = tk.BooleanVar()

        self._crear_interfaz()

    def _crear_interfaz(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- SECCIÓN 1: FECHAS ---
        lbl_titulo = ttk.Label(main_frame, text=" Selección de Fechas", font=("Arial", 12, "bold"))
        lbl_titulo.pack(anchor="w", pady=(0, 5))

        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        self.cal_entry = DateEntry(date_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.cal_entry.pack(side=tk.LEFT, padx=5)
        
        btn_add = ttk.Button(date_frame, text="Agregar Fecha", command=self.agregar_fecha)
        btn_add.pack(side=tk.LEFT, padx=5)

        self.tree_fechas = ttk.Treeview(main_frame, columns=("fecha"), show="headings", height=6)
        self.tree_fechas.heading("fecha", text="Fechas Seleccionadas")
        self.tree_fechas.pack(fill=tk.X, pady=5)
        
        btn_del = ttk.Button(main_frame, text="Eliminar Seleccionada", command=self.eliminar_fecha)
        btn_del.pack(anchor="e")

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

        # --- SECCIÓN 2: FILTROS ---
        lbl_filtros = ttk.Label(main_frame, text=" Filtros Opcionales", font=("Arial", 12, "bold"))
        lbl_filtros.pack(anchor="w", pady=(0, 5))

        # ==========================================================================================
        # FILTRO ESPECIE

        

        frame_esp = ttk.LabelFrame(main_frame,text="Seleccione una especie (Obligatorio) : ",padding=13)
        frame_esp.pack(fill=tk.X,pady=5)

        self.combo_especie = ttk.Combobox(main_frame,values=self.LISTA_ESPECIE,state="readonly",width=30)

        self.combo_especie.pack(pady=5)


        '''
        esp_container = ttk.Frame(frame_esp)
        esp_container.pack(fill=tk.X,pady=5)

        scroll_esp = ttk.Scrollbar(esp_container)
        scroll_esp.pack(side=tk.RIGHT,fill=tk.Y)

        self.listbox_especies = tk.Listbox(esp_container, selectmode=tk.EXTENDED, 
                                           height=5, yscrollcommand=scrollbar.set, exportselection=False)
        
         # Llenar la lista
        for var in self.LISTA_ESPECIE:
            self.listbox_especies.insert(tk.END, var)

        self.listbox_especies.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scroll_esp.config(command=self.listbox_especies.yview)
        '''
        # --- FILTRO VARIEDAD (SELECCIÓN MÚLTIPLE) ---
        frame_var = ttk.LabelFrame(main_frame, text=" Variedades ", padding=10)
        frame_var.pack(fill=tk.X, pady=5)

        chk_var = ttk.Checkbutton(frame_var, text="Activar Filtro", 
                                variable=self.var_filtrar_variedad, command=self.toggle_filtros)
        chk_var.pack(anchor="w")

        # Contenedor para la lista y el scrollbar
        list_container = ttk.Frame(frame_var)
        list_container.pack(fill=tk.X, pady=5)

        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox con modo 'multiple' o 'extended' (extended permite arrastrar y usar Ctrl)
        self.listbox_variedades = tk.Listbox(list_container, selectmode=tk.EXTENDED, 
                                           height=5, yscrollcommand=scrollbar.set, exportselection=False)
        
        # Llenar la lista
        for var in self.LISTA_VARIEDADES:
            self.listbox_variedades.insert(tk.END, var)
            
        self.listbox_variedades.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar.config(command=self.listbox_variedades.yview)
        
        # Texto de ayuda
        lbl_help = ttk.Label(frame_var, text="(Usa Ctrl + Click para seleccionar varias)", font=("Arial", 8, "italic"))
        lbl_help.pack(anchor="w")


        # --- FILTRO PRODUCTOR ---
        #frame_prod = ttk.Frame(main_frame)
        #frame_prod.pack(fill=tk.X, pady=10)
        
        #chk_prod = ttk.Checkbutton(frame_prod, text="Filtrar por Productor", 
        #                         variable=self.var_filtrar_productor, command=self.toggle_filtros)
        #chk_prod.pack(side=tk.LEFT)
        
        #self.entry_productor = ttk.Entry(frame_prod, state="disabled")
        #self.entry_productor.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        #ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

        # --- BOTON EJECUTAR ---
        style = ttk.Style()
        style.configure("Bold.TButton", font=("Arial", 10, "bold"))
        self.btn_run = ttk.Button(main_frame, text="GENERAR INFORME WORD", 
                                style="Bold.TButton", command=self.ejecutar_proceso)
        self.btn_run.pack(fill=tk.X, ipady=10)
        
        # Inicializar estado visual
        self.toggle_filtros()

    # --- METODOS DE FECHAS ---
    def agregar_fecha(self):
        fecha = self.cal_entry.get_date().strftime("%Y-%m-%d")
        if fecha not in self.fechas_seleccionadas:
            self.fechas_seleccionadas.append(fecha)
            self.fechas_seleccionadas.sort()
            self._actualizar_lista_fechas()
        else:
            messagebox.showwarning("Aviso", "Fecha ya está en lista.")

    def eliminar_fecha(self):
        sel = self.tree_fechas.selection()
        if sel:
            val = self.tree_fechas.item(sel[0], "values")[0]
            self.fechas_seleccionadas.remove(val)
            self._actualizar_lista_fechas()

    def _actualizar_lista_fechas(self):
        for item in self.tree_fechas.get_children(): self.tree_fechas.delete(item)
        for f in self.fechas_seleccionadas: self.tree_fechas.insert("", "end", values=(f,))

    # --- METODOS DE FILTROS ---
    def toggle_filtros(self):
        # Logica visual para la lista de variedades
        if self.var_filtrar_variedad.get():
            self.listbox_variedades.config(state="normal", bg="white")
        else:
            self.listbox_variedades.selection_clear(0, tk.END) # Limpiar selección al desactivar
            self.listbox_variedades.config(state="disabled", bg="#f0f0f0")

        # Logica para productor
        #estado_prod = "normal" if self.var_filtrar_productor.get() else "disabled"
        #self.entry_productor.config(state=estado_prod)

    def reiniciar_formulario(self):
        self.fechas_seleccionadas.clear()
        self._actualizar_lista_fechas()
        
        self.var_filtrar_variedad.set(False)
        #self.var_filtrar_productor.set(False)
        self.toggle_filtros()
        
        #self.entry_productor.delete(0, tk.END)
        self.listbox_variedades.selection_clear(0, tk.END) # Limpiar selección múltiple
        self.combo_especie.select_clear(0,tk.END)

    def ejecutar_proceso(self):
        if not self.fechas_seleccionadas:
            messagebox.showerror("Error", "Selecciona al menos una fecha.")
            return
        especie = self.combo_especie.get()

        if not especie:
            messagebox.showwarning("Campo Obligatorio","Por favor seleccione una especie")
            self.combo_especie.focus()
            return
        # 1. Obtener Variedades (NUEVA LÓGICA)
        if self.var_filtrar_variedad.get():
            indices = self.listbox_variedades.curselection() # Retorna tupla de índices (0, 2, 5)
            if not indices:
                messagebox.showwarning("Falta dato", "Activaste filtro variedad pero no seleccionaste ninguna.")
                return
            # Convertimos índices a nombres reales
            lista_variedades_final = [self.listbox_variedades.get(i) for i in indices]
        else:
            lista_variedades_final = None # O None, según prefieras en tu lógica

        # 2. Obtener Productor
        #productor = self.entry_productor.get() if self.var_filtrar_productor.get() else "TODOS"


        # --- LÓGICA DE VENTANA DE CARGA ---
        ventana_carga = tk.Toplevel(self)
        ventana_carga.title("Procesando...")
        ventana_carga.geometry("400x150")
        ventana_carga.resizable(False, False)
        ventana_carga.transient(self)
        ventana_carga.grab_set()
        
        x = self.winfo_x() + 50
        y = self.winfo_y() + 150
        ventana_carga.geometry(f"+{x}+{y}")

        lbl_tit = ttk.Label(ventana_carga, text="Generando Informe...", font=("Arial", 11, "bold"))
        lbl_tit.pack(pady=15)
        bar = ttk.Progressbar(ventana_carga, length=320, mode="determinate")
        bar.pack(pady=5)
        lbl_st = ttk.Label(ventana_carga, text="Iniciando...", font=("Arial", 9))
        lbl_st.pack(pady=5)

        def cb_gui(msg, paso, total):
            lbl_st.config(text=msg)
            if total > 0: bar['value'] = (paso/total)*100
            ventana_carga.update()

        self.btn_run.config(state="disabled")

        try:
            # Pasamos la LISTA DE VARIEDADES a generador
            generador(self.fechas_seleccionadas, lista_variedades_final,especie,callback_progreso=cb_gui)
            
            ventana_carga.destroy()
            if messagebox.askyesno("Éxito", "Informe listo.\n¿Otro reporte?"):
                self.reiniciar_formulario()
            else:
                self.destroy()

        except Exception as e:
            ventana_carga.destroy()
            import traceback
            messagebox.showerror("Error", f"Error:\n{traceback.format_exc()}")

        finally:
            try:
                if self.btn_run.winfo_exists():
                    self.btn_run.config(state="normal")
            except: pass

if __name__ == "__main__":
    app = AppFrutas()
    app.mainloop()
