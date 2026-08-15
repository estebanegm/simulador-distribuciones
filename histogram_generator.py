import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t, f

# CONFIGURACION DE LA PAGINA
st.set_page_config(
    page_title="Simulador de Distribuciones",
    page_icon=":bar_chart:",
    layout="centered"
)

# TITULO
st.title("Simulador de Distribuciones de Probabilidad")
st.markdown("*Genera datos aleatorios, visualiza histogramas y compara con la densidad teorica*")
st.markdown("---")

# MENU EN BARRA LATERAL
st.sidebar.header("Selecciona una distribucion")

opcion = st.sidebar.selectbox(
    "Distribucion:",
    ["Normal", "t de Student", "F de Fisher"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("Parametros")

# ENTRADA DEL TAMAÑO DE MUESTRA
n = st.sidebar.number_input(
    "Numero de datos a generar (n):", 
    value=10000, 
    min_value=100, 
    max_value=100000, 
    step=1000,
    format="%d"
)

if opcion == "Normal":
    mu = st.sidebar.number_input("Media (u):", value=0.0, step=0.5, format="%.1f")
    sigma = st.sidebar.number_input("Desviacion estandar (s):", value=1.0, min_value=0.1, step=0.5, format="%.1f")
    
    datos = np.random.normal(loc=mu, scale=sigma, size=n)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = norm.pdf(x, loc=mu, scale=sigma)
    
    titulo = f"Distribucion Normal (u = {mu}, s = {sigma})"
    xlabel = "X"

elif opcion == "t de Student":
    gl = st.sidebar.number_input("Grados de libertad:", value=10, min_value=1, step=1)
    
    datos = np.random.standard_t(df=gl, size=n)
    x = np.linspace(-4, 4, 1000)
    y = t.pdf(x, df=gl)
    
    titulo = f"Distribucion t de Student (gl = {gl})"
    xlabel = "X"

else:
    gl1 = st.sidebar.number_input("Grados de libertad (numerador):", value=5, min_value=1, step=1)
    gl2 = st.sidebar.number_input("Grados de libertad (denominador):", value=10, min_value=1, step=1)
    
    datos = np.random.f(dfnum=gl1, dfden=gl2, size=n)
    x = np.linspace(0, 6, 1000)
    y = f.pdf(x, dfn=gl1, dfd=gl2)
    
    titulo = f"Distribucion F de Fisher (gl1 = {gl1}, gl2 = {gl2})"
    xlabel = "F"

# CALCULO DE ESTADISTICAS
media = np.mean(datos)
desviacion = np.std(datos)

# MOSTRAR HISTOGRAMA
st.markdown("<h3 style='text-align: center;'>Histograma vs Densidad Teorica</h3>", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(datos, bins=50, density=True, alpha=0.6, color="skyblue", edgecolor='black', label="Datos simulados")
ax.plot(x, y, color="red", linewidth=2.5, label="Densidad teorica")

ax.set_title(titulo, fontsize=14, fontweight='bold')
ax.set_xlabel(xlabel, fontsize=12)
ax.set_ylabel("Densidad", fontsize=12)
ax.legend(loc="upper right")
ax.grid(alpha=0.3)

if opcion == "F de Fisher":
    ax.set_xlim(0, 6)

st.pyplot(fig)

# MOSTRAR ESTADISTICAS
col1, col2, col3 = st.columns(3)
col1.metric("Media muestral", f"{media:.4f}")
col2.metric("Desviacion estandar", f"{desviacion:.4f}")
col3.metric("Tamano de muestra", f"{n:,}")

# FIRMA
st.markdown("---")
st.caption("Elaborado por Esteban E. G. M.")
