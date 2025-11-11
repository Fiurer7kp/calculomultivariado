# utils/symbolic_helpers.py
import sympy as sp
import re

def safe_sympify(expr_str, variables=None):
    """Convierte string a expresión SymPy de forma segura"""
    try:
        if variables:
            # Crear símbolos
            sym_vars = sp.symbols(' '.join(variables))
            # Evaluar con contexto seguro
            local_dict = {'sp': sp, **dict(zip(variables, sym_vars))}
            return eval(expr_str, {"__builtins__": None}, local_dict)
        else:
            return sp.sympify(expr_str)
    except:
        return sp.sympify(expr_str)

def latex_clean(latex_str):
    """Limpia strings LaTeX para display"""
    return latex_str.replace('\\', '\\\\')