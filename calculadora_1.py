 Aquí está el código mejorado con mejor estructura, seguridad y funcionalidad:

```python
import tkinter as tk
from tkinter import messagebox
import re

class Calculadora:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Calculadora - Distrisuspensiones S.A.S.")
        self.ventana.geometry("320x450")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#2C3E50")
        
        # Variables
        self.expresion_actual = ""
        self.historial = []
        
        # Crear interfaz
        self.crear_widgets()
        
        # Atajos de teclado
        self.ventana.bind('<Return>', lambda e: self.calcular())
        self.ventana.bind('<Escape>', lambda e: self.borrar())
        self.ventana.bind('<BackSpace>', lambda e: self.borrar_ultimo())
        
        # Vincular números y operadores del teclado
        for i in range(10):
            self.ventana.bind(str(i), lambda e, num=str(i): self.click_boton(num))
        for op in ['+', '-', '*', '/']:
            self.ventana.bind(op, lambda e, operador=op: self.click_boton(operador))
        self.ventana.bind('.', lambda e: self.click_boton('.'))

    def crear_widgets(self):
        # Frame para la pantalla
        frame_pantalla = tk.Frame(self.ventana, bg="#2C3E50")
        frame_pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        # Etiqueta para operación anterior (historial)
        self.label_historial = tk.Label(
            frame_pantalla, 
            text="", 
            font=("Arial", 10), 
            bg="#2C3E50", 
            fg="#95A5A6",
            anchor="e",
            height=1
        )
        self.label_historial.pack(fill="x")
        
        # Caja de texto mejorada
        self.entrada = tk.Entry(
            frame_pantalla,
            font=("Arial", 24, "bold"),
            borderwidth=0,
            relief="flat",
            justify="right",
            bg="#34495E",
            fg="#ECF0F1",
            insertbackground="#ECF0F1"
        )
        self.entrada.pack(fill="x", ipady=15)
        self.entrada.insert(0, "0")

    def click_boton(self, valor):
        actual = self.entrada.get()
        
        # Si muestra "0" o un resultado previo, reemplazar
        if actual == "0" or actual in [str(h) for h in self.historial[-1:]] and valor not in ['+', '-', '*', '/']:
            self.entrada.delete(0, tk.END)
            actual = ""
        
        # Evitar operadores duplicados
        if valor in ['+', '-', '*', '/'] and actual and actual[-1] in ['+', '-', '*', '/']:
            self.entrada.delete(len(actual)-1, tk.END)
            actual = actual[:-1]
        
        # Evitar múltiples puntos decimales en un número
        if valor == '.':
            # Obtener el último número
            numeros = re.split(r'[+\-*/]', actual)
            if numeros and '.' in numeros[-1]:
                return
        
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, actual + valor)

    def borrar(self):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "0")
        self.label_historial.config(text="")

    def borrar_ultimo(self):
        actual = self.entrada.get()
        if len(actual) > 1:
            self.entrada.delete(len(actual)-1, tk.END)
        else:
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, "0")

    def calcular(self):
        try:
            expresion = self.entrada.get()
            
            # Validar expresión antes de evaluar
            if not expresion or expresion == "0":
                return
            
            # Validación de seguridad: solo permitir números y operadores básicos
            if not re.match(r'^[0-9+\-*/.() ]+$', expresion):
                raise ValueError("Caracteres no permitidos")
            
            # Evaluar de forma segura
            resultado = eval(expresion, {"__builtins__": {}}, {})
            
            # Formatear resultado
            if isinstance(resultado, float):
                # Evitar muchos decimales
                if resultado.is_integer():
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 8)
            
            # Guardar en historial
            self.historial.append(resultado)
            self.label_historial.config(text=f"{expresion} =")
            
            # Mostrar resultado
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, str(resultado))
            
        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir entre cero")
            self.borrar()
        except Exception as e:
            messagebox.showerror("Error", "Expresión inválida")
            self.borrar()

    def crear_boton(self, texto, fila, columna, color_bg="#34495E", color_fg="#ECF0F1", 
                    columnspan=1, comando=None):
        boton = tk.Button(
            self.ventana,
            text=texto,
            width=5 if columnspan == 1 else 22,
            height=2,
            font=("Arial", 16, "bold"),
            bg=color_bg,
            fg=color_fg,
            activebackground=color_bg,
            activeforeground=color_fg,
            borderwidth=0,
            relief="flat",
            cursor="hand2",
            command=comando
        )
        boton.grid(row=fila, column=columna, columnspan=columnspan, padx=3, pady=3, sticky="nsew")
        
        # Efectos hover
        boton.bind("<Enter>", lambda e: boton.config(bg=self.ajustar_color(color_bg, 1.2)))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_bg))
        
        return boton

    def ajustar_color(self, color_hex, factor):
        """Ajusta el brillo de un color hexadecimal"""
        color_hex = color_hex.lstrip('#')
        rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * factor)) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

# Crear ventana principal
if __name__ == "__main__":
    ventana = tk.Tk()
    app = Calculadora(ventana)
    
    # Definición de botones
    botones = [
        ('7', 1, 0, '#34495E'), ('8', 1, 1, '#34495E'), ('9', 1, 2, '#34495E'), ('/', 1, 3, '#E67E22'),
        ('4', 2, 0, '#34495E'), ('5', 2, 1, '#34495E'), ('6', 2, 2, '#34495E'), ('*', 2, 3, '#E67E22'),
        ('1', 3, 0, '#34495E'), ('2', 3, 1, '#34495E'), ('3', 3, 2, '#34495E'), ('-', 3, 3, '#E67E22'),
        ('0', 4, 0, '#34495E'), ('.', 4, 1, '#34495E'), ('=', 4, 2, '#27AE60'), ('+', 4, 3, '#E67E22'),
        ('←', 5, 0, '#E74C3C'), ('C', 5, 1, '#E74C3C')
    ]
    
    for item in botones:
        if len(item) == 4:
            texto, fila, columna, color = item
            if texto == '=':
                app.crear_boton(texto, fila, columna, color, "#FFFFFF", 1, app.calcular)
            elif texto == 'C':
                app.crear_boton(texto, fila, columna, color, "#FFFFFF", 2, app.borrar)
            elif texto == '←':
                app.crear_boton(texto, fila, columna, color, "#FFFFFF", 1, app.borrar_ultimo)
            elif texto in ['+', '-', '*', '/']:
                app.crear_boton(texto, fila, columna, color, "#FFFFFF", 1, 
                              lambda t=texto: app.click_boton(t))
            else:
                app.crear_boton(texto, fila, columna, color, "#ECF0F1", 1, 
                              lambda t=texto: app.click_boton(t))
    
    ventana.mainloop()
```

## **Mejoras implementadas:**

### 🏗️ **Estructura**
- Programación orientada a objetos (clase Calculadora)
- Código más organizado y mantenible
- Separación de responsabilidades

### 🎨 **Interfaz**
- Diseño moderno con esquema de colores profesional
- Efectos hover en los botones
- Historial de operaciones visible
- Mejor contraste y legibilidad

### ⌨️ **Funcionalidad**
- **Atajos de teclado**: Enter (calcular), Esc (borrar), Backspace (borrar último)
- **Botón "←"**: Borrar último carácter
- **Validaciones**: Evita operadores duplicados y múltiples puntos decimales
- Formateo inteligente de resultados

### 🔒 **Seguridad**
- Validación con regex antes de evaluar
- `eval()` restringido sin acceso a funciones peligrosas
- Manejo robusto de errores

### ✨ **Extra**
- Historial de cálculos
- Colores diferenciados por tipo de botón
- Interfaz responsiva y profesional