import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t, f

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Simulador de Distribuciones",
    page_icon="📊",
    layout="centered"
)


# TÍTULO

st.title("🎲 Simulador de Distribuciones de Probabilidad")
st.markdown("*Genera datos aleatorios, visualiza histogramas y compara con la densidad teórica*")
st.markdown("---")

# MENÚ EN BARRA LATERAL
st.sidebar.header("📌 Selecciona una distribución")

opcion = st.sidebar.selectbox(
    "Distribución:",
    ["Normal", "t de Student", "F de Fisher"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Parámetros")

# ENTRADA DE PARÁMETROS

n = 10000  # Tamaño de muestra fijo

if opcion == "Normal":
    mu = st.sidebar.number_input("Media (μ):", value=0.0, step=0.5, format="%.1f")
    sigma = st.sidebar.number_input("Desviación estándar (σ):", value=1.0, min_value=0.1, step=0.5, format="%.1f")
    
    datos = np.random.normal(loc=mu, scale=sigma, size=n)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = norm.pdf(x, loc=mu, scale=sigma)
    
    titulo = f"Distribución Normal (μ = {mu}, σ = {sigma})"
    xlabel = "X"

elif opcion == "t de Student":
    gl = st.sidebar.number_input("Grados de libertad:", value=10, min_value=1, step=1)
    
    datos = np.random.standard_t(df=gl, size=n)
    x = np.linspace(-4, 4, 1000)
    y = t.pdf(x, df=gl)
    
    titulo = f"Distribución t de Student (gl = {gl})"
    xlabel = "X"

else:  # F de Fisher
    gl1 = st.sidebar.number_input("Grados de libertad (numerador):", value=5, min_value=1, step=1)
    gl2 = st.sidebar.number_input("Grados de libertad (denominador):", value=10, min_value=1, step=1)
    
    datos = np.random.f(dfnum=gl1, dfden=gl2, size=n)
    x = np.linspace(0, 6, 1000)
    y = f.pdf(x, dfn=gl1, dfd=gl2)
    
    titulo = f"Distribución F de Fisher (gl1 = {gl1}, gl2 = {gl2})"
    xlabel = "F"

# CÁLCULO DE ESTADÍSTICAS

media = np.mean(datos)
desviacion = np.std(datos)

# MOSTRAR HISTOGRAMA
st.subheader("📊 Histograma vs Densidad Teórica")

fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(datos, bins=50, density=True, alpha=0.6, color="skyblue", edgecolor='black', label="Datos simulados")
ax.plot(x, y, color="red", linewidth=2.5, label="Densidad teórica")

ax.set_title(titulo, fontsize=14, fontweight='bold')
ax.set_xlabel(xlabel, fontsize=12)
ax.set_ylabel("Densidad", fontsize=12)
ax.legend(loc="upper right")
ax.grid(alpha=0.3)

if opcion == "F de Fisher":
    ax.set_xlim(0, 6)

st.pyplot(fig)

# MOSTRAR ESTADÍSTICAS

col1, col2, col3 = st.columns(3)
col1.metric("📌 Media muestral", f"{media:.4f}")
col2.metric("📌 Desviación estándar", f"{desviacion:.4f}")
col3.metric("📌 Tamaño de muestra", f"{n:,}")

# MOSTRAR PARÁMETROS USADOS

st.markdown("---")
st.caption("Datos generados aleatoriamente con tamaño de muestra n = 10,000")