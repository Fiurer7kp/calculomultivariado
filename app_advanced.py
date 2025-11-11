from flask import Flask, request, jsonify
import sympy as sp
import numpy as np
from sympy import symbols, sympify, diff, integrate, solve, series, limit
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoGebra Advanced Calculus</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { background: #1e2a3a; min-height: 100vh; padding: 15px; color: white; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: center; }
        .main-content { display: grid; grid-template-columns: 1fr 400px; gap: 15px; }
        .graph-panel { background: #34495e; padding: 15px; border-radius: 10px; }
        .graph-container { width: 100%; height: 300px; background: white; border-radius: 5px; display: flex; align-items: center; justify-content: center; }
        #graphImage { max-width: 100%; max-height: 100%; }
        .calc-panel { background: #2c3e50; padding: 15px; border-radius: 10px; }
        .display { background: #1a1a1a; color: #00ff00; font-size: 18px; padding: 12px; 
                  border-radius: 5px; margin-bottom: 10px; min-height: 50px; font-family: monospace; }
        .mode-selector { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin-bottom: 10px; }
        .mode-btn { padding: 8px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .mode-btn.active { background: #e67e22; }
        .buttons { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin-bottom: 10px; }
        button { padding: 12px 5px; font-size: 14px; border: none; border-radius: 5px; cursor: pointer; }
        .number { background: #95a5a6; }
        .operation { background: #3498db; color: white; }
        .function { background: #e67e22; color: white; }
        .advanced { background: #9b59b6; color: white; }
        .equals { background: #2ecc71; color: white; }
        .clear { background: #e74c3c; color: white; }
        .results { background: #34495e; padding: 10px; border-radius: 5px; margin-top: 10px; max-height: 150px; overflow-y: auto; }
        .loading { color: #f39c12; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧮 GeoGebra Advanced Calculus</h1>
            <p>Calculadora Multivariable y Análisis Vectorial</p>
        </div>
        
        <div class="main-content">
            <div class="graph-panel">
                <h3>Visualización Gráfica</h3>
                <div class="graph-container">
                    <img id="graphImage" src="" alt="Gráfico de la función">
                </div>
                <div class="results" id="results">
                    <strong>Resultados:</strong><br>
                    <div id="resultText">Selecciona una función y presiona "Calcular"</div>
                </div>
            </div>
            
            <div class="calc-panel">
                <div class="display" id="display">x^2 + y^2</div>
                
                <div class="mode-selector">
                    <button class="mode-btn active" onclick="setMode('function')">Función 2D</button>
                    <button class="mode-btn" onclick="setMode('3d')">Superficie 3D</button>
                    <button class="mode-btn" onclick="setMode('derivative')">Derivada</button>
                    <button class="mode-btn" onclick="setMode('integral')">Integral</button>
                    <button class="mode-btn" onclick="setMode('vector')">Vectorial</button>
                    <button class="mode-btn" onclick="setMode('limit')">Límite</button>
                </div>
                
                <div class="buttons">
                    <!-- Variables -->
                    <button class="function" onclick="addToDisplay('x')">x</button>
                    <button class="function" onclick="addToDisplay('y')">y</button>
                    <button class="function" onclick="addToDisplay('z')">z</button>
                    <button class="function" onclick="addToDisplay('t')">t</button>
                    
                    <!-- Constantes -->
                    <button class="function" onclick="addToDisplay('pi')">π</button>
                    <button class="function" onclick="addToDisplay('e')">e</button>
                    
                    <!-- Operadores básicos -->
                    <button class="number" onclick="addToDisplay('7')">7</button>
                    <button class="number" onclick="addToDisplay('8')">8</button>
                    <button class="number" onclick="addToDisplay('9')">9</button>
                    <button class="operation" onclick="addToDisplay('+')">+</button>
                    <button class="operation" onclick="addToDisplay('-')">-</button>
                    
                    <button class="number" onclick="addToDisplay('4')">4</button>
                    <button class="number" onclick="addToDisplay('5')">5</button>
                    <button class="number" onclick="addToDisplay('6')">6</button>
                    <button class="operation" onclick="addToDisplay('*')">×</button>
                    <button class="operation" onclick="addToDisplay('/')">÷</button>
                    
                    <button class="number" onclick="addToDisplay('1')">1</button>
                    <button class="number" onclick="addToDisplay('2')">2</button>
                    <button class="number" onclick="addToDisplay('3')">3</button>
                    <button class="function" onclick="addToDisplay('**')">^</button>
                    <button class="function" onclick="addToDisplay('sqrt(')">√</button>
                    
                    <button class="number" onclick="addToDisplay('0')">0</button>
                    <button class="function" onclick="addToDisplay('.')">.</button>
                    <button class="function" onclick="addToDisplay('(')">(</button>
                    <button class="function" onclick="addToDisplay(')')">)</button>
                    <button class="clear" onclick="clearDisplay()">C</button>
                    
                    <!-- Funciones avanzadas -->
                    <button class="advanced" onclick="addToDisplay('sin(')">sin</button>
                    <button class="advanced" onclick="addToDisplay('cos(')">cos</button>
                    <button class="advanced" onclick="addToDisplay('tan(')">tan</button>
                    <button class="advanced" onclick="addToDisplay('log(')">ln</button>
                    <button class="advanced" onclick="addToDisplay('exp(')">exp</button>
                    
                    <!-- Operaciones cálculo -->
                    <button class="advanced" onclick="calculateOperation('gradient')">∇f</button>
                    <button class="advanced" onclick="calculateOperation('laplacian')">∇²</button>
                    <button class="advanced" onclick="calculateOperation('integrate')">∫∫</button>
                    <button class="advanced" onclick="addToDisplay(',')">,</button>
                    
                    <!-- Ejemplos predefinidos -->
                    <button class="function" onclick="loadExample('paraboloid')">Paraboloide</button>
                    <button class="function" onclick="loadExample('sphere')">Esfera</button>
                    <button class="function" onclick="loadExample('saddle')">Silla</button>
                    <button class="function" onclick="loadExample('wave')">Onda</button>
                    <button class="equals" onclick="calculate()">Calcular</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentExpression = 'x**2 + y**2';
        let currentMode = 'function';
        const display = document.getElementById('display');
        const resultText = document.getElementById('resultText');
        const graphImage = document.getElementById('graphImage');
        
        function setMode(mode) {
            currentMode = mode;
            document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            updateDisplay();
        }
        
        function addToDisplay(value) {
            currentExpression += value;
            updateDisplay();
        }
        
        function clearDisplay() {
            currentExpression = '';
            updateDisplay();
        }
        
        function updateDisplay() {
            display.textContent = getDisplayText();
        }
        
        function getDisplayText() {
            const prefixes = {
                'function': 'f(x,y) = ',
                '3d': 'z = ',
                'derivative': '∂/∂x de: ',
                'integral': '∫ de: ',
                'vector': 'F(x,y,z) = ',
                'limit': 'lim x→a: '
            };
            return (prefixes[currentMode] || '') + currentExpression;
        }
        
        function loadExample(type) {
            const examples = {
                'paraboloid': 'x**2 + y**2',
                'sphere': 'sqrt(25 - x**2 - y**2)',
                'saddle': 'x**2 - y**2',
                'wave': 'sin(x) * cos(y)'
            };
            currentExpression = examples[type];
            updateDisplay();
        }
        
        async function calculate() {
            resultText.innerHTML = '<div class="loading">🔄 Calculando y graficando...</div>';
            
            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        expression: currentExpression,
                        mode: currentMode,
                        operation: 'evaluate'
                    })
                });
                const data = await response.json();
                if (data.success) {
                    resultText.innerHTML = `<div style="color: #2ecc71;">✅ ${data.result}</div>`;
                    if (data.plot_image) {
                        graphImage.src = 'data:image/png;base64,' + data.plot_image;
                    }
                } else {
                    resultText.innerHTML = `<div style="color: #e74c3c;">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultText.innerHTML = `<div style="color: #e74c3c;">❌ Error de conexión: ${error}</div>`;
            }
        }
        
        async function calculateOperation(operation) {
            resultText.innerHTML = '<div class="loading">🔄 Calculando...</div>';
            
            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        expression: currentExpression,
                        mode: currentMode,
                        operation: operation
                    })
                });
                const data = await response.json();
                if (data.success) {
                    resultText.innerHTML = `<div style="color: #2ecc71;">✅ ${operation}: ${data.result}</div>`;
                } else {
                    resultText.innerHTML = `<div style="color: #e74c3c;">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultText.innerHTML = `<div style="color: #e74c3c;">❌ Error de conexión</div>`;
            }
        }
        
        // Inicializar
        updateDisplay();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

def create_plot(expression, mode):
    """Crear gráfico usando matplotlib"""
    try:
        # Configurar matplotlib para no mostrar ventanas
        plt.switch_backend('Agg')
        plt.figure(figsize=(8, 6))
        
        x, y = symbols('x y')
        expr_sympy = sympify(expression)
        
        if mode in ['function', '3d']:
            # Crear malla de puntos
            x_vals = np.linspace(-5, 5, 100)
            y_vals = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(x_vals, y_vals)
            
            # Evaluar función
            Z = np.zeros_like(X)
            for i in range(len(x_vals)):
                for j in range(len(y_vals)):
                    try:
                        val = float(expr_sympy.subs({x: x_vals[i], y: y_vals[j]}))
                        Z[j, i] = val
                    except:
                        Z[j, i] = np.nan
            
            if mode == '3d':
                # Gráfico 3D
                from mpl_toolkits.mplot3d import Axes3D
                ax = plt.axes(projection='3d')
                ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_title(f'z = {expression}')
            else:
                # Gráfico de contorno 2D
                contour = plt.contour(X, Y, Z, levels=20)
                plt.clabel(contour, inline=True, fontsize=8)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title(f'f(x,y) = {expression}')
                plt.grid(True, alpha=0.3)
                plt.colorbar(contour)
        
        elif mode == 'derivative':
            # Gráfico de derivada
            x_vals = np.linspace(-5, 5, 100)
            derivative = diff(expr_sympy, x)
            y_vals = [float(derivative.subs(x, val)) for val in x_vals]
            plt.plot(x_vals, y_vals, 'r-', linewidth=2)
            plt.xlabel('x')
            plt.ylabel("f'(x)")
            plt.title(f"Derivada: {derivative}")
            plt.grid(True, alpha=0.3)
        
        # Convertir gráfico a imagen base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plot_image = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return plot_image
        
    except Exception as e:
        print(f"Error creando gráfico: {e}")
        return None

@app.route('/calculate', methods=['POST'])
def calculate_advanced():
    try:
        data = request.json
        expression = data['expression']
        mode = data.get('mode', 'function')
        operation = data.get('operation', 'evaluate')
        
        print(f"Modo: {mode}, Operación: {operation}, Expresión: {expression}")
        
        # Definir símbolos
        x, y, z, t = symbols('x y z t')
        
        # Limpiar expresión
        expr_clean = expression.replace('^', '**').replace('π', 'pi')
        
        result = ""
        plot_image = None
        
        if operation == 'evaluate':
            if mode in ['function', '3d']:
                # Evaluar función
                expr_sympy = sympify(expr_clean)
                result = f"f(x,y) = {expr_sympy}"
                # Crear gráfico
                plot_image = create_plot(expr_clean, mode)
                
            elif mode == 'derivative':
                # Calcular derivada parcial
                expr_sympy = sympify(expr_clean)
                derivative = diff(expr_sympy, x)
                result = f"∂f/∂x = {derivative}"
                plot_image = create_plot(str(derivative), 'derivative')
                
            elif mode == 'integral':
                # Calcular integral
                expr_sympy = sympify(expr_clean)
                integral = integrate(expr_sympy, x)
                result = f"∫f dx = {integral} + C"
                
            elif mode == 'vector':
                # Operaciones vectoriales
                expr_sympy = sympify(expr_clean)
                result = f"Campo vectorial: {expr_sympy}"
                
            elif mode == 'limit':
                # Calcular límite
                expr_sympy = sympify(expr_clean)
                lim = limit(expr_sympy, x, 0)
                result = f"lim x→0 = {lim}"
                
        elif operation == 'gradient':
            # Gradiente
            expr_sympy = sympify(expr_clean)
            grad_x = diff(expr_sympy, x)
            grad_y = diff(expr_sympy, y)
            result = f"∇f = ({grad_x}, {grad_y})"
            
        elif operation == 'laplacian':
            # Laplaciano
            expr_sympy = sympify(expr_clean)
            laplacian = diff(expr_sympy, x, 2) + diff(expr_sympy, y, 2)
            result = f"∇²f = {laplacian}"
            
        elif operation == 'integrate':
            # Integral múltiple
            expr_sympy = sympify(expr_clean)
            try:
                double_int = integrate(expr_sympy, (x, -5, 5), (y, -5, 5))
                result = f"∫∫ f dx dy ≈ {double_int.evalf()}"
            except:
                result = "No se pudo calcular la integral doble numéricamente"
        
        return jsonify({
            'success': True, 
            'result': str(result),
            'plot_image': plot_image
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error completo: {error_details}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Calculadora Multivariable Avanzada iniciada!")
    print("📊 Ahora con gráficos REALES de funciones 2D y 3D")
    print("📈 Usando matplotlib para visualización científica")
    print("🌐 Abre: http://127.0.0.1:5000")
    
    # Verificar dependencias
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        print("✅ Todas las dependencias cargadas correctamente")
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Ejecuta: python -m pip install matplotlib numpy sympy")
    
    app.run(debug=True, port=5000)