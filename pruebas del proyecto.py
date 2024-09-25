import google.generativeai as genai
import tkinter as tk
from tkinter import Text, Checkbutton, BooleanVar
from PIL import Image, ImageTk

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

root = tk.Tk()
root.title("COOKING CODICE")
root.geometry("850x650")  # Adjusting the window size for better appearance

# Cargar la imagen de fondo
try:
    imagen_fondo = Image.open(r"/mnt/data/imagen.png")  # Usar la imagen cargada
    imagen_fondo = imagen_fondo.resize((850, 650), Image.ANTIALIAS)  # Updated dimensions
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
except Exception as e:
    print(f"Error al cargar la imagen: {e}")
    imagen_fondo = None

# Crear un Label para la imagen de fondo
if imagen_fondo:
    fondo_label = tk.Label(root, image=imagen_fondo)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa toda la ventana

fuente = ("Helvetica", 16)

# Variable para almacenar la opción de "solo estos ingredientes"
solo_ingredientes_var = BooleanVar()

# Función para manejar el formato de la salida
def formatear_salida(texto):
    texto_salida.delete("1.0", tk.END)  # Limpiar la salida
    partes = texto.split("\n")  # Dividir el texto por líneas
    
    for parte in partes:
        if parte.startswith("#"):
            texto_salida.insert(tk.END, parte[1:] + "\n", "titulo")
        elif "**" in parte:
            inicio = 0
            while "**" in parte[inicio:]:
                pre_negrita = parte[inicio:parte.find("**", inicio)]
                texto_salida.insert(tk.END, pre_negrita)
                inicio_negrita = parte.find("**", inicio) + 2
                fin_negrita = parte.find("**", inicio_negrita)
                if fin_negrita == -1:
                    fin_negrita = len(parte)
                negrita = parte[inicio_negrita:fin_negrita]
                texto_salida.insert(tk.END, negrita, "negrita")
                inicio = fin_negrita + 2
            texto_salida.insert(tk.END, "\n")
        elif parte.lstrip().startswith(tuple(str(i) for i in range(1, 10)) + (".",)):
            texto_salida.insert(tk.END, "• " + parte.lstrip()[2:] + "\n", "lista")
        elif "*" in parte:
            decorado = parte.replace("*", "✦")
            texto_salida.insert(tk.END, decorado + "\n", "decorado")
        else:
            texto_salida.insert(tk.END, parte + "\n")


# Función para obtener la receta
def obtener_receta():
    ingredientes = entrada_ingredientes.get("1.0", tk.END).strip()
    if ingredientes:
        if solo_ingredientes_var.get():
            prompt = f'Quiero una receta con solo estos ingredientes: {ingredientes}'
        else:
            prompt = f'Quiero una receta con estos ingredientes y puedes agregar otros si es necesario: {ingredientes}'
        
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        formatear_salida(response.text)
    else:
        texto_salida.delete("1.0", tk.END)
        texto_salida.insert(tk.END, "Por favor ingrese algunos ingredientes.")


# Etiqueta para ingresar ingredientes
etiqueta_ingredientes = tk.Label(root, text="Ingrese los ingredientes:", font=fuente, bg="white")
etiqueta_ingredientes.place(x=200, y=50)

# Cuadro de texto para los ingredientes
entrada_ingredientes = Text(root, wrap=tk.WORD, width=60, height=6, font=fuente)
entrada_ingredientes.place(x=100, y=100)

# Opción para seleccionar si se usan solo los ingredientes ingresados
check_solo_ingredientes = Checkbutton(root, text="Usar solo estos ingredientes", font=fuente, variable=solo_ingredientes_var, bg="white")
check_solo_ingredientes.place(x=100, y=220)

# Botón para obtener la receta
boton_receta = tk.Button(root, text="Obtener Receta", command=obtener_receta, font=fuente, width=20, height=2, bg="#4CAF50", fg="white")
boton_receta.place(x=250, y=250)

# Cuadro de texto para mostrar la salida
texto_salida = Text(root, wrap=tk.WORD, width=60, height=12, font=fuente)
texto_salida.place(x=100, y=350)

# Configuración de las etiquetas de formato
texto_salida.tag_config("titulo", font=("Helvetica", 20, "bold"))
texto_salida.tag_config("negrita", font=("Helvetica", 16, "bold"))
texto_salida.tag_config("lista", font=("Helvetica", 16))
texto_salida.tag_config("decorado", font=("Helvetica", 16, "italic"), foreground="blue")

root.imagen_fondo = imagen_fondo

root.mainloop()
