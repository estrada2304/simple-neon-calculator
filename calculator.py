import tkinter as tk
from tkinter import font
import math

# Configuración inicial
root = tk.Tk()
root.title("Calculadora Científica Neon")
root.geometry("400x650")
root.configure(bg='black')
root.overrideredirect(True)  # Eliminar barra de título

# Paleta de colores neón
neon_red = '#FF3131'
neon_orange = '#FF9E3F'
neon_blue = '#4D4DFF'
dark_bg = '#111111'

# Fuente digital
try:
    digital_font = font.Font(family='DS-Digital', size=28, weight='bold')
except:
    digital_font = font.Font(family='Courier', size=28, weight='bold')

# ========== FUNCIÓN PARA DIBUJAR RECTÁNGULOS REDONDEADOS ==========
def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = []
    # Esquina superior derecha
    points.extend([x2-radius, y1, x2, y1, x2, y1+radius])
    # Esquina inferior derecha
    points.extend([x2, y2-radius, x2, y2, x2-radius, y2])
    # Esquina inferior izquierda
    points.extend([x1+radius, y2, x1, y2, x1, y2-radius])
    # Esquina superior izquierda
    points.extend([x1, y1+radius, x1, y1, x1+radius, y1])
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Añadir método al Canvas
tk.Canvas.create_rounded_rect = create_rounded_rect

# ========== FUNCIÓN PARA BOTONES REDONDEADOS ==========
def create_rounded_button(parent, text, x, y, color, command):
    btn = tk.Canvas(parent, width=60, height=60, bg=dark_bg, highlightthickness=0)
    # Círculo exterior
    btn.create_oval(5, 5, 55, 55, outline=color, width=2, fill=dark_bg)
    # Texto centrado
    btn.create_text(30, 30, text=text, font=('Arial', 14, 'bold'), fill=color)
    btn.place(x=x, y=y)
    btn.bind('<Button-1>', lambda e: (command(), on_press(btn)))
    return btn

# Efecto al presionar botones
def on_press(button):
    button.itemconfig(1, outline='white')
    root.after(100, lambda: button.itemconfig(1, outline=neon_red if button.itemcget(2, 'fill') == neon_red 
                                     else neon_orange if button.itemcget(2, 'fill') == neon_orange 
                                     else neon_blue))

# ========== LÓGICA DE LA CALCULADORA ==========
expression = ""
display_var = tk.StringVar()

def update_display(value):
    global expression
    expression += str(value)
    display_var.set(expression)

def calculate():
    global expression
    try:
        result = str(eval(expression))
        display_var.set(result)
        expression = result
    except:
        display_var.set("Error")
        expression = ""

def clear():
    global expression
    expression = ""
    display_var.set("")

def scientific_func(func):
    global expression
    try:
        if func == 'sqrt':
            result = math.sqrt(eval(expression))
        elif func == 'sin':
            result = math.sin(math.radians(eval(expression)))
        elif func == 'cos':
            result = math.cos(math.radians(eval(expression)))
        elif func == 'tan':
            result = math.tan(math.radians(eval(expression)))
        elif func == 'log':
            result = math.log10(eval(expression))
        elif func == 'ln':
            result = math.log(eval(expression))
        elif func == 'pi':
            result = math.pi
        elif func == 'e':
            result = math.e
        elif func == '^':
            expression += '**'
            display_var.set(expression)
            return
        display_var.set(str(result))
        expression = str(result)
    except:
        display_var.set("Error")
        expression = ""

# ========== INTERFAZ GRÁFICA ==========
canvas = tk.Canvas(root, bg='black', highlightthickness=0, width=400, height=650)
canvas.pack()

# Marco principal redondeado
canvas.create_rounded_rect(20, 20, 380, 630, radius=30, outline=neon_red, width=2, fill=dark_bg)

# Pantalla
display = tk.Entry(root, textvariable=display_var, font=digital_font, bd=0, 
                  width=12, borderwidth=0, justify='right', bg=dark_bg, fg=neon_red)
canvas.create_window(200, 70, window=display)

# Distribución de botones
button_layout = [
    ('sin', 30, 150, neon_orange, lambda: scientific_func('sin')),
    ('cos', 110, 150, neon_orange, lambda: scientific_func('cos')),
    ('tan', 190, 150, neon_orange, lambda: scientific_func('tan')),
    ('log', 270, 150, neon_orange, lambda: scientific_func('log')),
    ('π', 30, 230, neon_orange, lambda: scientific_func('pi')),
    ('e', 110, 230, neon_orange, lambda: scientific_func('e')),
    ('√', 190, 230, neon_orange, lambda: scientific_func('sqrt')),
    ('^', 270, 230, neon_orange, lambda: scientific_func('^')),
    ('7', 30, 310, neon_red, lambda: update_display('7')),
    ('8', 110, 310, neon_red, lambda: update_display('8')),
    ('9', 190, 310, neon_red, lambda: update_display('9')),
    ('/', 270, 310, neon_blue, lambda: update_display('/')),
    ('4', 30, 390, neon_red, lambda: update_display('4')),
    ('5', 110, 390, neon_red, lambda: update_display('5')),
    ('6', 190, 390, neon_red, lambda: update_display('6')),
    ('*', 270, 390, neon_blue, lambda: update_display('*')),
    ('1', 30, 470, neon_red, lambda: update_display('1')),
    ('2', 110, 470, neon_red, lambda: update_display('2')),
    ('3', 190, 470, neon_red, lambda: update_display('3')),
    ('-', 270, 470, neon_blue, lambda: update_display('-')),
    ('0', 30, 550, neon_red, lambda: update_display('0')),
    ('.', 110, 550, neon_red, lambda: update_display('.')),
    ('=', 190, 550, neon_blue, calculate),
    ('+', 270, 550, neon_blue, lambda: update_display('+')),
    ('C', 270, 470, neon_orange, clear),
    ('DEL', 190, 230, neon_orange, lambda: display_var.set(display_var.get()[:-1]))
]

# Crear todos los botones
for (text, x, y, color, cmd) in button_layout:
    create_rounded_button(root, text, x, y, color, cmd)

# Botón de cierre
close_btn = tk.Button(root, text='✕', font=('Arial', 12), bg=dark_bg, fg=neon_red,
                     borderwidth=0, command=root.destroy)
canvas.create_window(370, 30, window=close_btn)

root.mainloop()
