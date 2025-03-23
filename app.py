from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    pasos = []
    error = None  # Variable para manejar errores

    if request.method == "POST":
        try:
            expresion = request.form["funcion"]
            t = sp.Symbol('t')
            s = sp.Symbol('s')

            # Procedimiento para Transformada de Laplace directa
            funcion = sp.sympify(expresion, locals={"sin": sp.sin, "cos": sp.cos, "exp": sp.exp})

            pasos.append(f"Ingresaste la función: \\( f(t) = {sp.latex(funcion)} \\)")
            terminos = funcion.as_ordered_terms()
            transformados = []
            for termino in terminos:
                laplace_term = sp.laplace_transform(termino, t, s, noconds=True)
                pasos.append(f"Transformamos el término \\( {sp.latex(termino)} \\): \\( {sp.latex(laplace_term)} \\)")
                transformados.append(laplace_term)
            resultado = sum(transformados)
            pasos.append(f"El resultado final es: \\( F(s) = {sp.latex(resultado)} \\)")

        except ValueError as e:
            error = str(e)  # Capturamos el error en la variable `error`
        except Exception as e:
            error = f"Error inesperado: {str(e)}"

    return render_template("index.html", resultado=resultado, pasos=pasos, error=error)

if __name__ == "__main__":
    app.run(debug=True)


