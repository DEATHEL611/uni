import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Checkbutton, BooleanVar
from PIL import Image, ImageTk  # Importación corregida

# Configuración de la API de Gemini
genai.configure(api_key="AIzaSyBKtLl0KuRsVi-coW_BGB92xsC808wg1lU")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Variables para el modo claro y oscuro
modo_oscuro = False

# Crear ventana principal
root = tk.Tk()
root.title("COOKING CODICE")
root.geometry("700x700")

# Colores para modo claro y oscuro
colores_claros = {
    "bg": "#f5f5f5",
    "usuario": "#DCF8C6",
    "gemini": "#EAEAEA",
    "texto": "#000000",
    "boton": "#4CAF50",
    "entrada": "#FFFFFF",
    "boton_texto": "white",
}

colores_oscuros = {
    "bg": "#2E2E2E",
    "usuario": "#1E3F2E",
    "gemini": "#3A3A3A",
    "texto": "#FFFFFF",
    "boton": "#555555",
    "entrada": "#404040",
    "boton_texto": "white",
}

# Función para cambiar entre modo claro y oscuro
def cambiar_modo():
    global modo_oscuro
    modo_oscuro = not modo_oscuro

    if modo_oscuro:
        colores = colores_oscuros
    else:
        colores = colores_claros

    # Aplicar colores
    root.config(bg=colores["bg"])
    chat_box.config(bg=colores["bg"], fg=colores["texto"])
    entrada_usuario.config(bg=colores["entrada"], fg=colores["texto"])
    boton_enviar.config(bg=colores["boton"], fg=colores["boton_texto"])
    boton_modo.config(bg=colores["boton"], fg=colores["boton_texto"])
    check_solo_ingredientes.config(bg=colores["bg"], fg=colores["texto"])

    # Actualizar burbujas
    chat_box.tag_config("usuario", background=colores["usuario"], foreground=colores["texto"])
    chat_box.tag_config("gemini", background=colores["gemini"], foreground=colores["texto"])
    chat_box.tag_config("negrita", foreground=colores["texto"])
    chat_box.tag_config("titulo", foreground=colores["texto"])
    chat_box.tag_config("lista", foreground=colores["texto"])

# Zona de chat con scrollbar
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), bg=colores_claros["bg"], fg=colores_claros["texto"], bd=0, padx=10, pady=10)
chat_box.config(state=tk.DISABLED)
chat_box.place(x=20, y=120, width=660, height=450)

# Campo de entrada de texto
entrada_usuario = Entry(root, font=("Arial", 14), width=50, bd=2, relief="flat", bg=colores_claros["entrada"], fg=colores_claros["texto"])
entrada_usuario.place(x=20, y=580, height=40)

# Variable para el checkbutton de "Solo con estos ingredientes"
solo_ingredientes_var = BooleanVar()

# Función para agregar burbujas de mensajes
def agregar_mensaje(mensaje, tipo="usuario"):
    chat_box.config(state=tk.NORMAL)

    if tipo == "usuario":
        chat_box.insert(tk.END, "Tú: ", ("bold",))
        chat_box.insert(tk.END, mensaje + "\n", ("usuario",))
    else:
        formatear_salida(mensaje)

    chat_box.see(tk.END)  # Scroll automático
    chat_box.config(state=tk.DISABLED)

# Configuración de las burbujas
chat_box.tag_config("usuario", background=colores_claros["usuario"], foreground=colores_claros["texto"], font=("Arial", 12), lmargin1=20, lmargin2=20)
chat_box.tag_config("gemini", background=colores_claros["gemini"], foreground=colores_claros["texto"], font=("Arial", 12), lmargin1=20, lmargin2=20)
chat_box.tag_config("bold", font=("Arial", 12, "bold"))
chat_box.tag_config("negrita", font=("Arial", 12, "bold"))
chat_box.tag_config("titulo", font=("Arial", 20, "bold"))
chat_box.tag_config("lista", font=("Arial", 12, "normal"))

# Función para formatear la salida según reglas
def formatear_salida(texto):
    partes = texto.split("\n")

    for parte in partes:
        if parte.startswith("#"):
            chat_box.insert(tk.END, parte[1:].strip() + "\n", "titulo")  # Formato de título
        elif "**" in parte:
            inicio = 0
            while "**" in parte[inicio:]:
                pre_negrita = parte[inicio:parte.find("**", inicio)]
                chat_box.insert(tk.END, pre_negrita)
                inicio_negrita = parte.find("**", inicio) + 2
                fin_negrita = parte.find("**", inicio_negrita)
                if fin_negrita == -1:
                    fin_negrita = len(parte)
                negrita = parte[inicio_negrita:fin_negrita]
                chat_box.insert(tk.END, negrita, "negrita")
                inicio = fin_negrita + 2
            chat_box.insert(tk.END, "\n")
        elif parte.lstrip().startswith(tuple(str(i) for i in range(1, 10)) + (".",)):
            chat_box.insert(tk.END, "• " + parte.lstrip()[2:] + "\n", "lista")  # Formato de lista
        elif parte.startswith("*"):
            chat_box.insert(tk.END, "• " + parte.lstrip()[1:].strip() + "\n", "lista")  # Formato de lista simple
        else:
            chat_box.insert(tk.END, parte + "\n", "gemini")  # Texto normal

# Función para obtener la receta
def obtener_receta():
    mensaje_usuario = entrada_usuario.get().strip()
    if not mensaje_usuario:
        return

    entrada_usuario.delete(0, tk.END)

    agregar_mensaje(mensaje_usuario, tipo="usuario")

    # Crear el prompt según la opción de solo ingredientes
    if solo_ingredientes_var.get():
        prompt = f"Quiero una receta con solo estos ingredientes: {mensaje_usuario}"
    else:
        prompt = f"Quiero una receta con estos ingredientes y puedes agregar otros si es necesario: {mensaje_usuario}"

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    respuesta_gemini = response.text

    agregar_mensaje(respuesta_gemini, tipo="gemini")

# Cargar ícono de avión de papel para el botón de enviar
try:
    img_avion = Image.open(r"C:\Users\alejo\OneDrive\Pictures\imagenes_codigo\avion.png")  # Ruta de tu imagen del avión
    img_avion = img_avion.resize((30, 30), Image.LANCZOS)  # Reemplazo de ANTIALIAS con Image.LANCZOS
    img_avion = ImageTk.PhotoImage(img_avion)
except Exception as e:
    print(f"Error al cargar la imagen del avión: {e}")
    img_avion = None

# Botón para enviar el mensaje con ícono de avión
boton_enviar = Button(root, image=img_avion, command=obtener_receta, bg=colores_claros["boton"], fg=colores_claros["boton_texto"], relief="flat")
boton_enviar.place(x=620, y=580, height=40, width=40)

# Checkbutton para "solo ingredientes introducidos"
check_solo_ingredientes = Checkbutton(root, text="Usar solo estos ingredientes", font=("Arial", 12), variable=solo_ingredientes_var, bg=colores_claros["bg"], fg=colores_claros["texto"])
check_solo_ingredientes.place(x=20, y=630)

# Botón para cambiar entre modo claro y oscuro
boton_modo = Button(root, text="Modo Oscuro/Claro", font=("Arial", 12), command=cambiar_modo, bg=colores_claros["boton"], fg=colores_claros["boton_texto"], relief="flat")
boton_modo.place(x=500, y=630, height=30, width=180)

# Cargar imagen del logo de Gemini
try:
    img_gemini = Image.open(r"C:\Users\alejo\OneDrive\Pictures\imagenes_codigo\coocking_codice.png")  # Verifica la ruta de la imagen
    img_gemini = img_gemini.resize((120,80), Image.LANCZOS)  # Reemplazo de ImageResampling con Image.LANCZOS
    img_gemini = ImageTk.PhotoImage(img_gemini)
    label_logo = tk.Label(root, image=img_gemini, bg=colores_claros["bg"])
    label_logo.place(x=290, y=20)  # Posición centrada
except Exception as e:
    print(f"Error al cargar la imagen de Gemini: {e}")

root.mainloop()
