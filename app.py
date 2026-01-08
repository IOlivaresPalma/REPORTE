import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import sys
import os
import threading


# --- Importar tu lógica ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from generator import generador
    #from load_data import 
except ImportError:
    def generador(fechas, var, prod):
        # Simulación de tiempo de proceso
        import time
        time.sleep(1)
        print(f"SIMULACIÓN: Fechas={fechas}, Var={var}, Prod={prod}")

class AppFrutas(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Reportes Frutícola")
        self.geometry("500x650")
        
        self.LISTA_VARIEDADES = [
            "AREKO", "BING", "KORDIA", "LAPINS", "PACIFIC RED", 
            "RAINIER", "REGINA", "ROYAL DAWN", "SANTINA", "SKEENA", 
            "STELLA", "SUMMIT", "SWEET ARYANA", "SWEETHEART", 
            "SYMPHONY", "VAN"
        ]
        
        self.fechas_seleccionadas = []
        self.var_filtrar_variedad = tk.BooleanVar()
        self.var_filtrar_productor = tk.BooleanVar()

        self._crear_interfaz()

    def _crear_interfaz(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # SECCIÓN 1: FECHAS
        lbl_titulo = ttk.Label(main_frame, text=" Selección de Fechas", font=("Arial", 12, "bold"))
        lbl_titulo.pack(anchor="w", pady=(0, 5))

        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        self.cal_entry = DateEntry(date_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.cal_entry.pack(side=tk.LEFT, padx=5)
        
        btn_add = ttk.Button(date_frame, text="Agregar Fecha", command=self.agregar_fecha)
        btn_add.pack(side=tk.LEFT, padx=5)

        self.tree_fechas = ttk.Treeview(main_frame, columns=("fecha"), show="headings", height=8)
        self.tree_fechas.heading("fecha", text="Fechas Seleccionadas")
        self.tree_fechas.pack(fill=tk.X, pady=10)
        
        btn_del = ttk.Button(main_frame, text="Eliminar Seleccionada", command=self.eliminar_fecha)
        btn_del.pack(anchor="e")

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)

        # SECCIÓN 2: FILTROS
        lbl_filtros = ttk.Label(main_frame, text=" Filtros Opcionales", font=("Arial", 12, "bold"))
        lbl_filtros.pack(anchor="w", pady=(0, 10))

        frame_var = ttk.Frame(main_frame)
        frame_var.pack(fill=tk.X, pady=5)
        
        chk_var = ttk.Checkbutton(frame_var, text="Filtrar por Variedad", 
                                variable=self.var_filtrar_variedad, command=self.toggle_filtros)
        chk_var.pack(side=tk.LEFT)
        
        self.combo_variedad = ttk.Combobox(frame_var, values=self.LISTA_VARIEDADES, state="disabled")
        self.combo_variedad.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        self.combo_variedad.set("LAPINS") 

        frame_prod = ttk.Frame(main_frame)
        frame_prod.pack(fill=tk.X, pady=5)
        
        chk_prod = ttk.Checkbutton(frame_prod, text="Filtrar por Productor", 
                                 variable=self.var_filtrar_productor, command=self.toggle_filtros)
        chk_prod.pack(side=tk.LEFT)
        
        self.entry_productor = ttk.Entry(frame_prod, state="disabled")
        self.entry_productor.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)

        # BOTÓN EJECUTAR
        style = ttk.Style()
        style.configure("Bold.TButton", font=("Arial", 10, "bold"))
        
        self.btn_run = ttk.Button(main_frame, text="GENERAR INFORME WORD", 
                                style="Bold.TButton", command=self.ejecutar_proceso)
        self.btn_run.pack(fill=tk.X, ipady=10)

    def agregar_fecha(self):
        fecha = self.cal_entry.get_date()
        fecha_str = fecha.strftime("%Y-%m-%d")
        if fecha_str not in self.fechas_seleccionadas:
            self.fechas_seleccionadas.append(fecha_str)
            self.fechas_seleccionadas.sort()
            self._actualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Esa fecha ya está en la lista.")

    def eliminar_fecha(self):
        seleccion = self.tree_fechas.selection()
        if seleccion:
            item = seleccion[0]
            val = self.tree_fechas.item(item, "values")[0]
            self.fechas_seleccionadas.remove(val)
            self._actualizar_lista()

    def _actualizar_lista(self):
        for item in self.tree_fechas.get_children():
            self.tree_fechas.delete(item)
        for fecha in self.fechas_seleccionadas:
            self.tree_fechas.insert("", "end", values=(fecha,))

    def toggle_filtros(self):
        if self.var_filtrar_variedad.get():
            self.combo_variedad.config(state="readonly")
        else:
            self.combo_variedad.config(state="disabled")
        
        estado_prod = "normal" if self.var_filtrar_productor.get() else "disabled"
        self.entry_productor.config(state=estado_prod)

    def reiniciar_formulario(self):
        """Limpia todo para un nuevo reporte"""
        self.fechas_seleccionadas.clear()
        self._actualizar_lista()
        
        self.var_filtrar_variedad.set(False)
        self.var_filtrar_productor.set(False)
        self.toggle_filtros()
        
        self.entry_productor.delete(0, tk.END)
        # La variedad la dejamos en default por si acaso

    def ejecutar_proceso(self):
        if not self.fechas_seleccionadas:
            messagebox.showerror("Error", "Debes seleccionar al menos una fecha.")
            return

        variedad = self.combo_variedad.get() if self.var_filtrar_variedad.get() else "TODAS"
        productor = self.entry_productor.get() if self.var_filtrar_productor.get() else "TODOS"

        if self.var_filtrar_variedad.get() and not variedad:
             messagebox.showwarning("Falta dato", "Selecciona una variedad.")
             return

        # UI Feedback
        self.btn_run.config(text="Procesando...", state="disabled")
        self.update()

        try:
            # Ejecución
            generador(self.fechas_seleccionadas, variedad, productor)
            
            # --- PREGUNTA FINAL ---
            respuesta = messagebox.askyesno(
                "Proceso Finalizado", 
                "El informe se generó exitosamente.\n\n¿Deseas generar OTRO informe?"
            )
            
            if respuesta: # Usuario dijo SI
                self.reiniciar_formulario() # Limpiamos para el siguiente
                self.btn_run.config(text="GENERAR INFORME WORD", state="normal")
            else: # Usuario dijo NO
                self.destroy() # Cerramos la app
                
        except Exception as e:
            messagebox.showerror("Error Crítico", f"Ocurrió un error:\n{str(e)}")
            self.btn_run.config(text="GENERAR INFORME WORD", state="normal")

if __name__ == "__main__":
    app = AppFrutas()
    app.mainloop()
