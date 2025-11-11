from flask import Flask, render_template, request, jsonify
import math
import sympy as sp
import numpy as np
from sympy import symbols, sympify, diff, hessian, solve, Matrix, latex

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
                     .replace('√', 'sqrt')
                     .replace('Math.', ''))

        # Remover prefijos tipo f(x)=, f(x,y)=, z=
        for prefix in ['f(x)=', 'f(x) =', 'f(x,y)=', 'f(x,y) =', 'z=', 'z =']:
            if expr_clean.strip().lower().startswith(prefix.replace(' ', '')) or expr_clean.strip().startswith(prefix):
                expr_clean = expr_clean.split('=', 1)[-1].strip()
        
        # Evaluar con sympy
        x, y, z = symbols('x y z')
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

@app.route('/optimize', methods=['POST'])
def optimize():
    """Optimización multivariable básica para f(x,y).
    Devuelve gradiente, hessiano, puntos críticos y clasificación.
    """
    try:
        data = request.json or {}
        func_str = data.get('func', '')
        if not func_str:
            return jsonify({'success': False, 'error': 'Función vacía'})

        # Preparar símbolos y expresión
        x, y = symbols('x y')
        expr = sympify(func_str)

        # Gradiente y Hessiano
        grad = [diff(expr, x), diff(expr, y)]
        H = hessian(expr, (x, y))

        # Puntos críticos resolviendo gradiente = 0
        crit_solutions = solve([sp.Eq(grad[0], 0), sp.Eq(grad[1], 0)], (x, y), dict=True)

        # Clasificación por criterio de segunda derivada
        classification = []
        crit_points_latex = []
        for sol in crit_solutions:
            subs = [(x, sol[x]), (y, sol[y])]
            f_xx = H[0, 0].subs(subs)
            detH = H.det().subs(subs)
            if detH.is_real:
                if detH > 0:
                    if f_xx > 0:
                        cls = 'Mínimo local'
                    else:
                        cls = 'Máximo local'
                elif detH < 0:
                    cls = 'Punto de silla'
                else:
                    cls = 'Indeterminado'
            else:
                cls = 'Indeterminado'
            classification.append(f"({sp.N(sol[x])}, {sp.N(sol[y])}): {cls}")
            crit_points_latex.append(f"(x = {latex(sol[x])}, y = {latex(sol[y])})")

        payload = {
            'success': True,
            'gradient_latex': r"\\nabla f = (" + latex(grad[0]) + ", " + latex(grad[1]) + ")",
            'hessian_latex': latex(Matrix(H)),
            'critical_points_latex': crit_points_latex,
            'classification': classification
        }
        return jsonify(payload)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/solve_for_y', methods=['POST'])
def solve_for_y():
    """Resuelve una ecuación en x,y para y(x). Devuelve lista de expresiones de y.
    Permite graficar relaciones como x + y = 1, y - x = sin(x), etc.
    """
    try:
        data = request.json or {}
        eq_str = data.get('equation', '')
        if not eq_str:
            return jsonify({'success': False, 'error': 'Ecuación vacía'})

        # Normalizar notación básica
        eq_str = (eq_str.replace('^', '**').replace('π', 'pi').replace('√', 'sqrt'))
        x, y = symbols('x y')

        # Construir ecuación SymPy
        if '=' in eq_str:
            left, right = eq_str.split('=', 1)
            eq = sp.Eq(sympify(left), sympify(right))
        else:
            # Si no hay igualdad, interpretamos como y = expresión
            expr = sympify(eq_str)
            eq = sp.Eq(y, expr)

        sols = solve(eq, y)

        y_exprs = [str(sp.simplify(s)) for s in sols] if isinstance(sols, (list, tuple)) else [str(sols)]

        return jsonify({'success': True, 'y_expressions': y_exprs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ------------------ New Analysis Endpoints ------------------

@app.route('/domain_range', methods=['POST'])
def domain_range():
    """Aproxima dominio (puntos válidos en un rectángulo) y rango de f(x,y) por muestreo."""
    try:
        data = request.json or {}
        fstr = data.get('expression', '')
        xr = data.get('x_range', [-5, 5])
        yr = data.get('y_range', [-5, 5])
        samples = int(data.get('samples', 80))

        clean = (fstr.replace('×', '*').replace('÷', '/').replace('^', '**')
                      .replace('π', 'pi').replace('√', 'sqrt').replace('Math.', ''))
        if '=' in clean:
            # Si viene z = f(x,y), toma la derecha
            left, right = clean.split('=', 1)
            clean = right.strip()

        x, y = symbols('x y')
        f = sympify(clean)
        f_np = sp.lambdify((x, y), f, 'numpy')

        xv = np.linspace(float(xr[0]), float(xr[1]), samples)
        yv = np.linspace(float(yr[0]), float(yr[1]), samples)
        X, Y = np.meshgrid(xv, yv)
        Z = None
        try:
            Z = f_np(X, Y)
        except Exception:
            Z = np.empty_like(X, dtype=float)
            Z[:] = np.nan
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    try:
                        val = float(f.subs({x: float(X[i, j]), y: float(Y[i, j])}).evalf())
                        Z[i, j] = val
                    except Exception:
                        Z[i, j] = np.nan

        valid = np.isfinite(Z)
        if not np.any(valid):
            return jsonify({'success': True, 'domain_points': 0, 'range_min': None, 'range_max': None})

        rmin = float(np.nanmin(Z))
        rmax = float(np.nanmax(Z))
        return jsonify({'success': True,
                        'domain_points': int(valid.sum()),
                        'x_range_used': [float(xr[0]), float(xr[1])],
                        'y_range_used': [float(yr[0]), float(yr[1])],
                        'range_min': rmin,
                        'range_max': rmax})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/limit2d', methods=['POST'])
def limit2d():
    """Estimación de límite de f(x,y) en (a,b) por aproximación multi-ruta."""
    try:
        data = request.json or {}
        fstr = data.get('expression', '')
        a = float(data.get('a'))
        b = float(data.get('b'))

        clean = (fstr.replace('×', '*').replace('÷', '/').replace('^', '**')
                      .replace('π', 'pi').replace('√', 'sqrt').replace('Math.', ''))
        if '=' in clean:
            left, right = clean.split('=', 1)
            clean = right.strip()

        x, y = symbols('x y')
        f = sympify(clean)
        f_np = sp.lambdify((x, y), f, 'numpy')

        epsilons = np.array([1e-1, 5e-2, 1e-2, 5e-3, 1e-3])
        paths = [
            lambda h: (a + h, b),
            lambda h: (a, b + h),
            lambda h: (a + h, b + h),
            lambda h: (a + h, b - h)
        ]
        seqs = []
        for p in paths:
            vals = []
            for h in epsilons:
                try:
                    xx, yy = p(h)
                    val = float(f_np(xx, yy))
                except Exception:
                    val = np.nan
                vals.append(val)
            seqs.append(vals)
        last_vals = np.array([v[-1] for v in seqs])
        if np.any(np.isnan(last_vals)):
            limit_estimate = None
            converges = False
        else:
            mean = float(np.mean(last_vals))
            spread = float(np.max(np.abs(last_vals - mean)))
            limit_estimate = mean
            converges = spread < 1e-3

        return jsonify({'success': True, 'limit_estimate': limit_estimate, 'converges': converges, 'last_values': last_vals.tolist()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/derivatives', methods=['POST'])
def derivatives():
    """Parciales, gradiente y Hessiano de f(x,y). Evalúa gradiente en punto si se pasa."""
    try:
        data = request.json or {}
        fstr = data.get('expression', '')
        point = data.get('point')

        clean = (fstr.replace('×', '*').replace('÷', '/').replace('^', '**')
                      .replace('π', 'pi').replace('√', 'sqrt').replace('Math.', ''))
        if '=' in clean:
            left, right = clean.split('=', 1)
            clean = right.strip()

        x, y = symbols('x y')
        f = sympify(clean)
        fx = diff(f, x)
        fy = diff(f, y)
        H = hessian(f, (x, y))

        payload = {
            'success': True,
            'fx_latex': latex(fx),
            'fy_latex': latex(fy),
            'hessian_latex': latex(Matrix(H))
        }
        if point and 'x' in point and 'y' in point:
            xv = float(point['x'])
            yv = float(point['y'])
            try:
                gradx = float(fx.subs({x: xv, y: yv}).evalf())
                grady = float(fy.subs({x: xv, y: yv}).evalf())
                payload['grad_at_point'] = [gradx, grady]
            except Exception:
                payload['grad_at_point'] = None
        return jsonify(payload)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/lagrange', methods=['POST'])
def lagrange():
    """Multiplicadores de Lagrange para f(x,y) con restricción g(x,y)=0."""
    try:
        data = request.json or {}
        fstr = data.get('f', '')
        gstr = data.get('g', '')
        if not fstr or not gstr:
            return jsonify({'success': False, 'error': 'Se requieren f y g.'})

        def norm(s):
            s = (s.replace('×', '*').replace('÷', '/').replace('^', '**')
                    .replace('π', 'pi').replace('√', 'sqrt').replace('Math.', ''))
            if '=' in s:
                left, right = s.split('=', 1)
                s = f"({left}) - ({right})"  # g=0 forma
            return s

        x, y, lam = symbols('x y lam')
        f = sympify(norm(fstr))
        g = sympify(norm(gstr))
        eqs = [diff(f, x) - lam*diff(g, x), diff(f, y) - lam*diff(g, y), sp.Eq(g, 0)]
        sols = solve(eqs, (x, y, lam), dict=True)
        points = []
        for s in sols:
            try:
                points.append({'x': float(sp.N(s[x])), 'y': float(sp.N(s[y]))})
            except Exception:
                pass
        return jsonify({'success': True, 'points': points, 'latex': {'f': latex(f), 'g': latex(g)}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/integral2d', methods=['POST'])
def integral2d():
    """Integración doble de f(x,y) sobre límites rectangulares."""
    try:
        data = request.json or {}
        fstr = data.get('expression', '')
        bounds = data.get('bounds', {})  # {x:[a,b], y:[c,d]}
        clean = (fstr.replace('×', '*').replace('÷', '/').replace('^', '**')
                      .replace('π', 'pi').replace('√', 'sqrt').replace('Math.', ''))
        # Si viene "f(x,y)=..." o "z=...", tomar la parte derecha
        if '=' in clean:
            left, right = clean.split('=', 1)
            clean = right.strip()
        x, y = symbols('x y')
        f = sympify(clean)
        a, b = bounds.get('x', [-1, 1])
        c, d = bounds.get('y', [-1, 1])
        res = sp.integrate(f, (x, a, b), (y, c, d))
        return jsonify({'success': True, 'result': str(sp.N(res)), 'latex': latex(res)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/integral3d', methods=['POST'])
def integral3d():
    """Integración triple de f(x,y,z) sobre límites rectangulares."""
    try:
        data = request.json or {}
        fstr = data.get('expression', '')
        bounds = data.get('bounds', {})  # {x:[a,b], y:[c,d], z:[e,f]}
        clean = (fstr.replace('×', '*').replace('÷', '/').replace('^', '**')
                      .replace('π', 'pi').replace('√', 'sqrt').replace('Math.', ''))
        # Si viene "f(x,y,z)=..." o "z=...", tomar la parte derecha
        if '=' in clean:
            left, right = clean.split('=', 1)
            clean = right.strip()
        x, y, z = symbols('x y z')
        f = sympify(clean)
        a, b = bounds.get('x', [-1, 1])
        c, d = bounds.get('y', [-1, 1])
        e, fz = bounds.get('z', [-1, 1])
        res = sp.integrate(f, (x, a, b), (y, c, d), (z, e, fz))
        return jsonify({'success': True, 'result': str(sp.N(res)), 'latex': latex(res)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Desactivar reloader para ejecución estable en este entorno
    app.run(debug=True, port=5000, use_reloader=False)