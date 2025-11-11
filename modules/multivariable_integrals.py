import sympy as sp
from sympy import symbols, integrate, Matrix, sin, cos, sqrt

class MultivariableIntegrator:
    def __init__(self):
        pass
    
    def double_integral(self, func_str, x_limits, y_limits):
        """Calcula integral doble ∫∫ f(x,y) dx dy"""
        x, y = symbols('x y')
        func = eval(func_str, {'sp': sp, 'x': x, 'y': y})
        
        # Integral iterada
        inner_integral = integrate(func, (x, x_limits[0], x_limits[1]))
        result = integrate(inner_integral, (y, y_limits[0], y_limits[1]))
        
        return {
            'integral_latex': r"\int_{" + str(y_limits[0]) + "}^{" + str(y_limits[1]) + "} \int_{" + str(x_limits[0]) + "}^{" + str(x_limits[1]) + "} " + sp.latex(func) + r" \, dx \, dy",
            'result_latex': sp.latex(result),
            'numeric_result': float(result.evalf()) if result.is_number else result
        }
    
    def triple_integral(self, func_str, x_limits, y_limits, z_limits):
        """Calcula integral triple ∫∫∫ f(x,y,z) dx dy dz"""
        x, y, z = symbols('x y z')
        func = eval(func_str, {'sp': sp, 'x': x, 'y': y, 'z': z})
        
        result = integrate(func, 
                          (x, x_limits[0], x_limits[1]),
                          (y, y_limits[0], y_limits[1]), 
                          (z, z_limits[0], z_limits[1]))
        
        return {
            'integral_latex': r"\iiint " + sp.latex(func) + r" \, dV",
            'result_latex': sp.latex(result),
            'numeric_result': float(result.evalf()) if result.is_number else result
        }
    
    def jacobian_transformation(self, transformation, old_vars, new_vars):
        """Calcula el Jacobiano para cambio de coordenadas"""
        jacobian_matrix = Matrix([[diff(transformation[i], old_var) for old_var in old_vars] for i in range(len(transformation))])
        return jacobian_matrix.det()