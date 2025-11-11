import sympy as sp
from sympy import symbols, solve, Eq, exp, sin, cos, tan, log, sqrt
import re

class AdvancedEquationSolver:
    def __init__(self):
        self.supported_functions = {
            'exp': exp, 'sin': sin, 'cos': cos, 'tan': tan,
            'log': log, 'sqrt': sqrt, 'ln': log
        }
    
    def parse_equation(self, equation_str, variables):
        """Convierte string de ecuación a objeto SymPy"""
        try:
            # Crear símbolos
            sym_vars = symbols(' '.join(variables))
            
            # Reemplazar funciones personalizadas
            eq_processed = equation_str
            for func_name, func_obj in self.supported_functions.items():
                eq_processed = eq_processed.replace(func_name, f'sp.{func_name.__name__}')
            
            # Crear ecuación
            if '=' in eq_processed:
                lhs, rhs = eq_processed.split('=', 1)
                equation = Eq(eval(lhs, {'sp': sp, **dict(zip(variables, sym_vars))}), 
                             eval(rhs, {'sp': sp, **dict(zip(variables, sym_vars))}))
            else:
                expression = eval(eq_processed, {'sp': sp, **dict(zip(variables, sym_vars))})
                equation = Eq(expression, 0)
            
            return equation, sym_vars
        except Exception as e:
            raise ValueError(f"Error parsing equation: {str(e)}")
    
    def solve_equation(self, equation_str, variables, solve_type="Solución General"):
        """Resuelve ecuaciones de forma avanzada"""
        equation, sym_vars = self.parse_equation(equation_str, variables)
        
        solutions = []
        latex_solution = ""
        
        try:
            if solve_type == "Solución General":
                solutions = solve(equation, sym_vars, dict=True)
                if solutions:
                    latex_solution = r"\text{Soluciones: } " + ", ".join([
                        "(" + ", ".join([f"{var} = {sol[var]}" for var in variables]) + ")" 
                        for sol in solutions
                    ])
                else:
                    latex_solution = r"\text{No se encontraron soluciones algebraicas}"
            
            elif solve_type == "Solución Numérica":
                # Para ecuaciones no algebraicas
                numeric_sols = sp.nsolve(equation, sym_vars, [1]*len(sym_vars))
                solutions = [dict(zip(variables, numeric_sols))]
                latex_solution = r"\text{Solución numérica: } " + str(numeric_sols)
        
        except Exception as e:
            latex_solution = f"\\text{{Error en solución: {str(e)}}}"
        
        return {
            'latex_equation': sp.latex(equation),
            'latex_solution': latex_solution,
            'solutions': solutions,
            'equation_obj': equation
        }
    
    def solve_system(self, equations_list, variables):
        """Resuelve sistemas de ecuaciones"""
        try:
            parsed_eqs = []
            for eq_str in equations_list:
                eq, _ = self.parse_equation(eq_str, variables)
                parsed_eqs.append(eq)
            
            solutions = solve(parsed_eqs, symbols(' '.join(variables)), dict=True)
            return solutions
        except Exception as e:
            raise ValueError(f"Error solving system: {str(e)}")