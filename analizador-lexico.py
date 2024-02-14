import tkinter as tk
from tkinter import ttk, scrolledtext
import ply.lex as lex

class lexema(object):
    palabras_reservadas = {
        'AREA': 'AREA', 'BASE': 'BASE', 'ALTURA': 'ALTURA',
    }

    tokens = [
        'IDENTIFICADOR', 'NUMERO',
        'OPERADOR', 'SIMBOLO', 'FIN',
    ] + list(palabras_reservadas.values())

    t_OPERADOR = r'[\+\*-/=]'
    t_SIMBOLO = r'[\(\)\[\]\{\};,]'
    t_ignore = ' \t'

    def t_NUMERO(self, t):
        r'\d*\.\d+|\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print(f"Float value too large {t.value}")
            t.value = 0
        t.type = 'NUMERO'
        return t

    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.palabras_reservadas.get(t.value.upper(), 'IDENTIFICADOR')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        
def analizar_codigo():
    codigo = input.get("1.0", "end-1c")
    lexema = lexema()
    lexema.build()
    lexema.lexer.input(codigo)
    
    for i in result_tree.get_children():
        result_tree.delete(i)

    for tok in lexema.lexer:
        is_reserved = "✓" if tok.type in lexema.palabras_reservadas.values() else ""
        is_identificador = "✓" if tok.type == 'IDENTIFICADOR' else ""
        is_numero = "✓" if tok.type == 'NUMERO' else ""
        is_operador = "✓" if tok.type == 'OPERADOR' else ""
        is_simbolo = "✓" if tok.type == 'SIMBOLO' else ""

        result_tree.insert("", 'end', values=(tok.value, is_reserved, is_identificador, is_numero, is_operador, is_simbolo))

def eliminar_seleccionados():
    seleccionados = result_tree.selection()
    for item in seleccionados:
        result_tree.delete(item)
    # Ocultar ambos frames
    frame_izquierda.grid_remove()
    frame_derecha.grid_remove()

window = tk.Tk()
window.title("Analizador Léxico con Tkinter")

frame_izquierda = ttk.Frame(window)
frame_izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

input = scrolledtext.ScrolledText(frame_izquierda, width=40, height=10, wrap=tk.WORD)
input.pack(fill="both", expand=True)

boton_analizar = tk.Button(frame_izquierda, text="Analizar Código", command=analizar_codigo, bg="blue", fg="white")
boton_analizar.pack(pady=5)

frame_derecha = ttk.Frame(window)
frame_derecha.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

result_tree = ttk.Treeview(frame_derecha, columns=("Valor", "Palabra Reservada", "IDENTIFICADOR", "NUMERO", "OPERADOR", "SÍMBOLO"), show="headings")
result_tree.heading("Valor", text="Valor")
result_tree.heading("Palabra Reservada", text="Palabra Reservada")
result_tree.heading("IDENTIFICADOR", text="Identificador")
result_tree.heading("NUMERO", text="Número")
result_tree.heading("OPERADOR", text="Operador")
result_tree.heading("SÍMBOLO", text="Símbolo")

result_tree.column("Valor", anchor="center")
result_tree.column("Palabra Reservada", anchor="center")
result_tree.column("IDENTIFICADOR", anchor="center")
result_tree.column("NUMERO", anchor="center")
result_tree.column("OPERADOR", anchor="center")
result_tree.column("SÍMBOLO", anchor="center")

result_tree.pack(fill="both", expand=True)

boton_eliminar = tk.Button(frame_derecha, text="Eliminar seleccionados", command=eliminar_seleccionados, bg="red", fg="white")
boton_eliminar.pack(pady=5)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

window.mainloop()
