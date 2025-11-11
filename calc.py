import math
import numpy as np
from sympy import symbols, sympify, diff, integrate, solve, plot
import json

def evaluate_expression(expr):
    """Evalúa expresiones matemáticas usando sympy para mayor seguridad"""
    try:
        # Reemplazar notación
        expr = expr.replace('^', '**').replace('π', 'pi')
        
        # Evaluar con sympy
        result = sympify(expr).evalf()
        return float(result) if result.is_number else str(result)
        
    except Exception as e:
        raise ValueError(f"Error evaluando expresión: {str(e)}")

def solve_equation(equation):
    """Resuelve ecuaciones usando sympy"""
    x = symbols('x')
    try:
        solutions = solve(equation, x)
        return [float(sol.evalf()) if sol.is_number else str(sol) for sol in solutions]
    except Exception as e:
        raise ValueError(f"Error resolviendo ecuación: {str(e)}")

def compute_derivative(expr, variable='x', order=1):
    """Calcula derivadas"""
    x = symbols(variable)
    try:
        derivative = diff(expr, x, order)
        return str(derivative)
    except Exception as e:
        raise ValueError(f"Error calculando derivada: {str(e)}")

def compute_integral(expr, variable='x'):
    """Calcula integrales"""
    x = symbols(variable)
    try:
        integral = integrate(expr, x)
        return str(integral)
    except Exception as e:
        raise ValueError(f"Error calculando integral: {str(e)}")