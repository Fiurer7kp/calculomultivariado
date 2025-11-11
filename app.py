from flask import Flask, render_template, request, jsonify
import math
import sympy as sp
from sympy import symbols, sympify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        expression = data['expression']
        print(f"Calculando: {expression}")
        
        # Limpiar expresión
        expr_clean = (expression
                     .replace('×', '*')
                     .replace('÷', '/')
                     .replace('^', '**')
                     .replace('π', 'pi')
                     .replace('√', 'sqrt'))
        
        # Evaluar con sympy
        x = symbols('x')
        expr_sympy = sympify(expr_clean)
        result = expr_sympy.evalf()
        
        if result.is_number:
            result_value = float(result)
            if result_value.is_integer():
                result_str = str(int(result_value))
            else:
                result_str = str(round(result_value, 10))
        else:
            result_str = str(result)
            
        return jsonify({'success': True, 'result': result_str})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)