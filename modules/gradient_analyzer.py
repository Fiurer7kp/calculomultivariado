import sympy as sp
from sympy import symbols, diff, solve, Matrix, hessian

class GradientAnalyzer:
    def __init__(self):
        pass
    
    def parse_function(self, func_str, variables):
        """Convierte string de función a expresión SymPy"""
        sym_vars = symbols(' '.join(variables))
        expression = eval(func_str, {'sp': sp, **dict(zip(variables, sym_vars))})
        return expression, sym_vars
    
    def compute_gradient(self, func, variables):
        """Calcula el gradiente de la función"""
        gradient = [diff(func, var) for var in variables]
        return gradient
    
    def find_critical_points(self, func, variables):
        """Encuentra puntos críticos resolviendo ∇f = 0"""
        gradient = self.compute_gradient(func, variables)
        critical_points = solve(gradient, variables, dict=True)
        return critical_points
    
    def compute_hessian(self, func, variables):
        """Calcula la matriz Hessiana"""
        return hessian(func, variables)
    
    def classify_critical_point(self, func, variables, point):
        """Clasifica punto crítico usando criterio de segunda derivada"""
        hessian_matrix = self.compute_hessian(func, variables)
        
        if len(variables) == 2:
            # Para 2 variables
            H = hessian_matrix
            f_xx = H[0,0]
            determinant = H.det()
            
            # Evaluar en el punto crítico
            substitutions = [(var, point[var]) for var in variables]
            f_xx_val = f_xx.subs(substitutions)
            det_val = determinant.subs(substitutions)
            
            if det_val > 0:
                if f_xx_val > 0:
                    return "Mínimo local"
                else:
                    return "Máximo local"
            elif det_val < 0:
                return "Punto de silla"
            else:
                return "Indeterminado"
        
        return "Clasificación para n>2 requiere análisis adicional"
    
    def complete_analysis(self, func_str, variables):
        """Análisis completo de la función"""
        func, sym_vars = self.parse_function(func_str, variables)
        
        # Gradiente
        gradient = self.compute_gradient(func, sym_vars)
        gradient_latex = r"\nabla f = \begin{pmatrix} " + " \\\\ ".join([sp.latex(g) for g in gradient]) + r" \end{pmatrix}"
        
        # Puntos críticos
        critical_points = self.find_critical_points(func, sym_vars)
        critical_points_latex = []
        
        # Clasificación
        classification = []
        
        for point in critical_points:
            point_latex = "(" + ", ".join([f"{sp.latex(var)} = {sp.latex(point[var])}" for var in sym_vars]) + ")"
            critical_points_latex.append(point_latex)
            
            # Clasificar punto
            point_class = self.classify_critical_point(func, sym_vars, point)
            classification.append(f"Punto {point_latex}: {point_class}")
        
        return {
            'function': func,
            'gradient': gradient,
            'gradient_latex': gradient_latex,
            'critical_points': critical_points_latex,
            'classification': classification,
            'hessian': self.compute_hessian(func, sym_vars)
        }