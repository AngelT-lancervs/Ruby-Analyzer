import tkinter as tk
from PIL import Image, ImageTk
import analyzers.lexical_analyzer as lexical
import analyzers.syntax_analyzer as syntax
import sys
import ply.yacc as yacc

class TextComponent:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.config(state=tk.NORMAL)  # Habilitar escritura
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)  # Deshabilitar escritura

def run_ruby(text_input):
    text_console.config(state=tk.NORMAL)  # Habilitar escritura en la consola
    text_console.delete(1.0, tk.END) 
    sys.stdout = TextComponent(text_console)
    lexical.lexer.input(text_input)
    try:
        for token in lexical.lexer:
            print(token)
        lexical.lexer.lineno = 1
        syntax.parser.parse(text_input)
        lexical.lexer.lineno = 1
    except Exception as e:
        print(f"Error: {e}")

    sys.stdout = sys.__stdout__  # Restaurar sys.stdout original
    text_console.config(state=tk.DISABLED)  # Deshabilitar escritura en la consola

# Función para el botón "Run"
def on_run():
    input_text_content = text_code.get(1.0, tk.END)
    run_ruby(input_text_content)

# Crear la ventana principal
root = tk.Tk()
root.title("Ruby Analyzer")

# Configurar el marco principal con dos secciones
frame_code = tk.Frame(root, bg="darkgrey", width=600, height=400)
frame_console = tk.Frame(root, bg="darkgrey", width=500, height=400)

frame_code.grid(row=0, column=0, sticky="nsew")
frame_console.grid(row=0, column=1, sticky="nsew")

# Configurar las proporciones de las columnas y filas
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=1)

# Añadir el botón rojo en la parte superior central de la sección de código
button_run = tk.Button(frame_code, text="Run", bg="red", fg="white", command=on_run, width=8, height=2)
button_run.place(relx=0.5, rely=0, anchor="n")

# Añadir un widget de texto para la sección de código
text_code = tk.Text(frame_code, wrap=tk.WORD, bg="lightgrey", fg="black")
text_code.place(relx=0.5, rely=0.1, anchor="n", relwidth=0.9, relheight=0.9)

# Añadir una etiqueta para la consola
label_console = tk.Label(frame_console, text="Console", bg="darkgrey", fg="black")
label_console.place(relx=0.5, rely=0.05, anchor="n")

# Añadir un widget de texto de solo lectura para la consola
text_console = tk.Text(frame_console, wrap=tk.WORD, bg="lightgrey", fg="black", state=tk.DISABLED)
text_console.place(relx=0.5, rely=0.15, anchor="n", relwidth=0.9, relheight=0.8)

# Cargar la imagen y colocarla en la esquina inferior derecha
img = Image.open("ruby.png")
img = img.resize((60, 60))  # Cambiar el tamaño de la imagen si es necesario
photo = ImageTk.PhotoImage(img)

# Crear un label para la imagen y colocarla en la esquina inferior derecha
label_image = tk.Label(root, image=photo, bg="darkgrey")
label_image.image = photo  # Guardar una referencia de la imagen para evitar que sea recolectada por el garbage collector
label_image.place(relx=1.0, rely=1.0, anchor="se")

# Ejecutar la aplicación
root.mainloop()
