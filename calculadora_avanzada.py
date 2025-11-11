#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALCULADORA MULTIVARIABLE AVANZADA
"""
import sympy as sp
from sympy import symbols, diff, integrate, solve, Eq, Matrix, sin, cos, tan, exp, log, sqrt, pi, E
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n" + "="*60)
    print("           CALCULADORA MULTIVARIABLE AVANZADA")
    print("="*60)
    print("1.  Resolver ecuaciones")
    print("2.  Calcular derivadas")
    print("3.  Calcular integrales")
    print("4.  Operaciones con matrices")
    print("5.  Limites de funciones")
    print("6.  Series de Taylor")
    print("7.  Ecuaciones diferenciales")
    print("8.  Calculo vectorial")
    print("9.  Salir")
    print("="*60)

def resolver_ecuacion():
    print("\n=== RESOLVER ECUACION ===")
    print("Ejemplos: x**2 - 4, sin(x)=0.5, exp(x)=10, x+y=5")
    ecuacion = input("Ecuacion: ")
    variables = input("Variables (ej: x,y): ").split(',')
    
    try:
        vars_list = [v.strip() for v in variables]
        syms = sp.symbols(' '.join(vars_list))
        
        if '=' in ecuacion:
            lhs, rhs = ecuacion.split('=', 1)
            eq = Eq(sp.sympify(lhs), sp.sympify(rhs))
        else:
            eq = Eq(sp.sympify(ecuacion), 0)
        
        soluciones = solve(eq, syms)
        print(f"\nEcuacion: {eq}")
        
        if soluciones:
            print("Soluciones encontradas:")
            for i, sol in enumerate(soluciones):
                if isinstance(sol, dict):
                    sol_str = ", ".join([f"{k} = {v}" for k, v in sol.items()])
                    print(f"  Solucion {i+1}: {sol_str}")
                else:
                    print(f"  Solucion {i+1}: {sol}")
        else:
            print("No se encontraron soluciones algebraicas")
            
    except Exception as e:
        print(f"Error: {e}")

def calcular_derivada():
    print("\n=== CALCULAR DERIVADA ===")
    print("Ejemplos: x**3, sin(x)*cos(x), exp(x**2), log(x)")
    funcion = input("Funcion: ")
    variable = input("Variable: ")
    orden = int(input("Orden (1-4): ") or "1")
    
    try:
        x = symbols(variable)
        f = sp.sympify(funcion)
        derivada = diff(f, x, orden)
        
        print(f"\nFuncion: f({variable}) = {f}")
        print(f"Derivada de orden {orden}: {derivada}")
        
    except Exception as e:
        print(f"Error: {e}")

def calcular_integral():
    print("\n=== CALCULAR INTEGRAL ===")
    print("Ejemplos: x**2, cos(x), exp(-x), 1/(x**2+1)")
    funcion = input("Funcion: ")
    variable = input("Variable: ")
    
    tipo = input("Tipo [i]ndefinida o [d]efinida? ").lower()
    
    try:
        x = symbols(variable)
        f = sp.sympify(funcion)
        
        if tipo == 'd':
            lim_inf = input("Limite inferior: ")
            lim_sup = input("Limite superior: ")
            a = sp.sympify(lim_inf)
            b = sp.sympify(lim_sup)
            resultado = integrate(f, (x, a, b))
            print(f"\nIntegral definida:")
            print(f"∫ desde {a} hasta {b} de {f} d{variable} = {resultado}")
        else:
            resultado = integrate(f, x)
            print(f"\nIntegral indefinida:")
            print(f"∫ {f} d{variable} = {resultado} + C")
            
    except Exception as e:
        print(f"Error: {e}")

def operaciones_matrices():
    print("\n=== OPERACIONES CON MATRICES ===")
    print("Ejemplo: [[1,2],[3,4]] o [[1,2,3],[4,5,6],[7,8,9]]")
    matriz_str = input("Matriz: ")
    
    try:
        M = Matrix(eval(matriz_str))
        print(f"\nMatriz {M.shape[0]}x{M.shape[1]}:\n{M}")
        
        if M.shape[0] == M.shape[1]:
            print(f"Determinante: {M.det()}")
            print(f"Traza: {M.trace()}")
            
            if M.shape[0] <= 3:
                print("Valores propios:")
                eigenvals = M.eigenvals()
                for val, mult in eigenvals.items():
                    print(f"  λ = {val} (multiplicidad: {mult})")
                    
    except Exception as e:
        print(f"Error: {e}")

def limites_funciones():
    print("\n=== LIMITES DE FUNCIONES ===")
    print("Ejemplos: sin(x)/x, (1-cos(x))/x**2, (1+1/x)**x")
    funcion = input("Funcion: ")
    variable = input("Variable: ")
    punto = input("Punto (ej: 0, oo para infinito): ")
    
    try:
        x = symbols(variable)
        f = sp.sympify(funcion)
        
        if punto == 'oo':
            punto = sp.oo
        else:
            punto = sp.sympify(punto)
        
        limite = sp.limit(f, x, punto)
        print(f"\nLimite de {f} cuando {variable} -> {punto} = {limite}")
        
    except Exception as e:
        print(f"Error: {e}")

def series_taylor():
    print("\n=== SERIES DE TAYLOR ===")
    print("Ejemplos: sin(x), cos(x), exp(x), log(1+x)")
    funcion = input("Funcion: ")
    variable = input("Variable: ")
    punto = input("Punto de expansion (ej: 0): ") or "0"
    orden = input("Orden de la serie (ej: 5): ") or "5"
    
    try:
        x = symbols(variable)
        f = sp.sympify(funcion)
        punto_num = sp.sympify(punto)
        orden_num = int(orden)
        
        serie = sp.series(f, x, punto_num, orden_num).removeO()
        print(f"\nSerie de Taylor de {f} alrededor de {variable} = {punto_num}:")
        print(f"Orden {orden_num}: {serie}")
        
    except Exception as e:
        print(f"Error: {e}")

def ecuaciones_diferenciales():
    print("\n=== ECUACIONES DIFERENCIALES ===")
    print("Ejemplos: f(x).diff(x) - f(x), f(x).diff(x,x) + f(x)")
    print("Usa f(x) para la funcion desconocida")
    ecuacion = input("Ecuacion diferencial: ")
    
    try:
        x = symbols('x')
        f = sp.Function('f')(x)
        
        eq = sp.sympify(ecuacion)
        solucion = sp.dsolve(eq, f)
        
        print(f"\nEcuacion: {eq} = 0")
        print(f"Solucion: {solucion}")
        
    except Exception as e:
        print(f"Error: {e}")

def calculo_vectorial():
    print("\n=== CALCULO VECTORIAL ===")
    print("Ejemplo: [x**2, y**2, z**2]")
    campo = input("Campo vectorial (ej: [x,y,z]): ")
    variables = input("Variables (ej: x,y,z): ").split(',')
    
    try:
        vars_list = [v.strip() for v in variables]
        syms = sp.symbols(' '.join(vars_list))
        
        vector = [sp.sympify(comp) for comp in eval(campo)]
        
        # Divergencia
        divergencia = sum(sp.diff(vector[i], syms[i]) for i in range(len(vector)))
        print(f"\nDivergencia: {divergencia}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    limpiar_pantalla()
    print("CALCULADORA MULTIVARIABLE AVANZADA")
    print("SymPy cargado correctamente!")
    
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona opcion (1-9): ")
        
        if opcion == '1':
            resolver_ecuacion()
        elif opcion == '2':
            calcular_derivada()
        elif opcion == '3':
            calcular_integral()
        elif opcion == '4':
            operaciones_matrices()
        elif opcion == '5':
            limites_funciones()
        elif opcion == '6':
            series_taylor()
        elif opcion == '7':
            ecuaciones_diferenciales()
        elif opcion == '8':
            calculo_vectorial()
        elif opcion == '9':
            print("¡Hasta luego!")
            break
        else:
            print("Opcion invalida")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
