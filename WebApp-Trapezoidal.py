import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, lambdify, symbols, integrate

# Streamlit App Title
st.title("Numerical Integration with Trapezoidal Rule")

# Input fields
st.write("This app demonstrates the Trapezoidal Rule for numerical integration. You can input a function, specify integration limits, and observe the results.")

function_input = st.text_input("Enter the function to integrate (in terms of x):", value="sin(x)")

try:
    func_expr = sympify(function_input)
    x = symbols('x')
    func = lambdify(x, func_expr, 'numpy')
except Exception as e:
    st.error(f"Invalid function: {e}")
    st.stop()

# Integration limits and sub-intervals
a = st.number_input("Lower limit of integration (a):", value=2.0)
b = st.number_input("Upper limit of integration (b):", value=14.0)
n = st.slider("Number of sub-intervals (n):", min_value=1, max_value=100, value=24)

# Trapezoidal Rule Implementation
if a >= b:
    st.error("Lower limit (a) must be less than upper limit (b).")
    st.stop()

def trapezoidal_rule(func, a, b, n):
    x_vals = np.linspace(a, b, n + 1)
    y_vals = func(x_vals)
    h = (b - a) / n
    integral = h * (0.5 * y_vals[0] + 0.5 * y_vals[-1] + np.sum(y_vals[1:-1]))
    return integral, x_vals, y_vals

numerical_integral, x_vals, y_vals = trapezoidal_rule(func, a, b, n)

# Exact integral using sympy
try:
    exact_integral = float(integrate(func_expr, (x, a, b)))
except Exception:
    exact_integral = None

# Results
st.subheader("Results")
st.write(f"Numerical Integral (Trapezoidal Rule): {numerical_integral:.6f}")
if exact_integral is not None:
    st.write(f"Exact Integral: {exact_integral:.6f}")
    st.write(f"Error: {abs(numerical_integral - exact_integral):.6f}")
else:
    st.write("Exact integral could not be computed.")

# Plot
fig, ax = plt.subplots()
ax.plot(x_vals, y_vals, 'o-', label="Function")
for i in range(n):
    ax.fill_between([x_vals[i], x_vals[i+1]], [y_vals[i], y_vals[i+1]], color='orange', alpha=0.5)
ax.set_title("Trapezoidal Approximation")
ax.legend()
ax.grid(True)
st.pyplot(fig)
