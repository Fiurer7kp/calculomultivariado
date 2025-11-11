import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sympy as sp
from sympy import symbols, lambdify

class VisualizationEngine:
    def __init__(self):
        pass
    
    def create_3d_surface(self, func_str, x_range=(-5, 5), y_range=(-5, 5)):
        """Crea superficie 3D interactiva"""
        x, y = symbols('x y')
        func_expr = eval(func_str, {'sp': sp, 'x': x, 'y': y})
        
        # Convertir a función numérica
        func_numeric = lambdify((x, y), func_expr, 'numpy')
        
        # Crear grid
        x_vals = np.linspace(x_range[0], x_range[1], 50)
        y_vals = np.linspace(y_range[0], y_range[1], 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = func_numeric(X, Y)
        
        # Crear figura
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        
        fig.update_layout(
            title=f'Superficie: {func_str}',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y', 
                zaxis_title='f(x,y)'
            )
        )
        
        return fig
    
    def plot_gradient_analysis(self, func_str, variables, analysis):
        """Visualiza análisis de gradiente"""
        if len(variables) != 2:
            return
        
        x, y = symbols('x y')
        func_expr = eval(func_str, {'sp': sp, 'x': x, 'y': y})
        func_numeric = lambdify((x, y), func_expr, 'numpy')
        
        # Crear superficie
        x_vals = np.linspace(-3, 3, 30)
        y_vals = np.linspace(-3, 3, 30)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = func_numeric(X, Y)
        
        fig = go.Figure()
        
        # Superficie
        fig.add_trace(go.Surface(z=Z, x=X, y=y, opacity=0.7, name='Superficie'))
        
        # Puntos críticos (simplificado)
        # Aquí podrías añadir marcadores para puntos críticos
        
        fig.update_layout(title='Análisis de Gradiente y Puntos Críticos')
        return fig