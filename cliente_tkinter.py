# cliente_tkinter.py
 
import tkinter as tk
from tkinter import ttk, messagebox
import requests
 
URL = "http://127.0.0.1:8000"
 
def insertar_usuario():
    nombre = entry_nombre.get()
    if not nombre.strip():
        messagebox.showwarning("Campo vacío", "Por favor ingrese un nombre.")
        return
    resp = requests.post(f"{URL}/insertar", json={"nombre": nombre})
    if resp.status_code == 201:
        messagebox.showinfo("Éxito", "Usuario insertado.")
        mostrar_usuarios()
        limpiar_campos()
    else:
        messagebox.showerror("Error", resp.json().get("error"))
 
def eliminar_usuario():
    codigo = entry_codigo.get()
    if not codigo.isdigit():
        messagebox.showwarning("Código inválido", "Ingrese un código válido.")
        return
    resp = requests.delete(f"{URL}/eliminar/{codigo}")
    if resp.status_code == 200:
        messagebox.showinfo("Éxito", "Usuario eliminado.")
        mostrar_usuarios()
        limpiar_campos()
    else:
        messagebox.showerror("Error", resp.json().get("error"))
 
def buscar_usuario():
    codigo = entry_codigo.get()
    if not codigo.isdigit():
        messagebox.showwarning("Código inválido", "Ingrese un código válido.")
        return
    resp = requests.get(f"{URL}/buscar/{codigo}")
    if resp.status_code == 200:
        usuario = resp.json()
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, usuario["nombre"])
    else:
        messagebox.showinfo("No encontrado", "Usuario no existe.")
 
def modificar_usuario():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    if not codigo.isdigit() or not nombre.strip():
        messagebox.showwarning("Datos inválidos", "Código y nombre requeridos.")
        return
    resp = requests.put(f"{URL}/modificar", json={"codigo": int(codigo), "nombre": nombre})
    if resp.status_code == 200:
        messagebox.showinfo("Éxito", "Usuario modificado.")
        mostrar_usuarios()
        limpiar_campos()
    else:
        messagebox.showerror("Error", resp.json().get("error"))
 
def limpiar_campos():
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
 
def mostrar_usuarios():
    for item in tree.get_children():
        tree.delete(item)
    resp = requests.get(f"{URL}/usuarios")
    if resp.status_code == 200:
        for row in resp.json():
            tree.insert("", tk.END, values=(row["codigo"], row["nombre"]))
 
# --- INTERFAZ TKINTER ---
ventana = tk.Tk()
ventana.title("Cliente CRUD - Tkinter con Flask")
ventana.geometry("500x450")
ventana.resizable(False, False)
 
tk.Label(ventana, text="Gestión de Usuarios", font=("Arial", 14, "bold")).pack(pady=10)
 
frame_datos = tk.LabelFrame(ventana, text="Datos del Usuario")
frame_datos.pack(fill="x", padx=10, pady=5)
 
tk.Label(frame_datos, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_codigo = tk.Entry(frame_datos)
entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
 
tk.Label(frame_datos, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_nombre = tk.Entry(frame_datos, width=40)
entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")
 
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)
 
tk.Button(frame_botones, text="Insertar", width=10, command=insertar_usuario).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Eliminar", width=10, command=eliminar_usuario).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Buscar", width=10, command=buscar_usuario).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="Modificar", width=10, command=modificar_usuario).grid(row=0, column=3, padx=5)
tk.Button(frame_botones, text="Limpiar", width=10, command=limpiar_campos).grid(row=0, column=4, padx=5)
 
frame_lista = tk.LabelFrame(ventana, text="Lista de Usuarios")
frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
 
tree = ttk.Treeview(frame_lista, columns=("codigo", "nombre"), show="headings")
tree.heading("codigo", text="Código")
tree.heading("nombre", text="Nombre")
tree.column("codigo", width=80)
tree.column("nombre", width=350)
tree.pack(fill="both", expand=True)
 
mostrar_usuarios()
ventana.mainloop()
