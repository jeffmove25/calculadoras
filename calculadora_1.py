import tkinter as tk
from tkinter import messagebox

def click_boton(valor):
    actual = str(entrada.get())
    entrada.delete(0, tk.END)
    entrada.insert(0, actual + valor)

def borrar():
    entrada.delete(0, tk.END)

def calcular():
    try:
        resultado = eval(entrada.get())
        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))
    except Exception as e:
        messagebox.showerror("Error", "Expresión inválida")

# Ventana principal
ventana = tk.Tk()
ventana.title("Calculadora - Distrisuspensiones S.A.S.")
ventana.geometry("300x400")
ventana.resizable(False, False)

# Caja de texto
entrada = tk.Entry(ventana, font=("Arial", 20), borderwidth=5, relief="ridge", justify="right")
entrada.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)

# Botones
botones = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

for (texto, fila, columna) in botones:
    if texto == '=':
        tk.Button(ventana, text=texto, width=5, height=2, font=("Arial", 16),
                  bg="#4CAF50", fg="white", command=calcular).grid(row=fila, column=columna, padx=5, pady=5)
    else:
        tk.Button(ventana, text=texto, width=5, height=2, font=("Arial", 16),
                  command=lambda t=texto: click_boton(t)).grid(row=fila, column=columna, padx=5, pady=5)

# Botón borrar
tk.Button(ventana, text="C", width=22, height=2, font=("Arial", 16),
          bg="#f44336", fg="white", command=borrar).grid(row=5, column=0, columnspan=4, padx=5, pady=5)

ventana.mainloop()

