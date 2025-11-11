import sympy as sp
from sympy import symbols, diff, Matrix, curl, divergence

class VectorCalculus:
    def __init__(self):
        pass
    
    def parse_vector_field(self, vector_str):
        """Convierte string de campo vectorial a SymPy"""
        x, y, z = symbols('x y z')
        vector_list = eval(vector_str, {'sp': sp, 'x': x, 'y': y, 'z': z})
        return Matrix(vector_list), [x, y, z]
    
    def divergence(self, vector_str):
        """Calcula la divergencia de un campo vectorial"""
        vector_field, vars = self.parse_vector_field(vector_str)
        div = divergence(vector_field, vars)
        
        return {
            'latex': r"\nabla \cdot \mathbf{F} = " + sp.latex(div),
            'expression': div
        }
    
    def curl(self, vector_str):
        """Calcula el rotacional de un campo vectorial"""
        vector_field, vars = self.parse_vector_field(vector_str)
        curl_matrix = curl(vector_field, vars)
        
        return {
            'latex': r"\nabla \times \mathbf{F} = \begin{pmatrix} " + " \\\\ ".join([sp.latex(c) for c in curl_matrix]) + r" \end{pmatrix}",
            'expression': curl_matrix
        }
    
    def stokes_theorem(self, vector_str):
        """Aplica el teorema de Stokes"""
        curl_result = self.curl(vector_str)
        
        return {
            'latex': r"\oint_C \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S} = " + sp.latex(curl_result['expression']),
            'expression': curl_result['expression']
        }