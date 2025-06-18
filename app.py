import streamlit as st
import sqlite3
from datetime import datetime
import pytz
from streamlit_extras.colored_header import colored_header

# Configuración
zona_horaria = pytz.timezone('America/Lima')

# --- Diseño con color ---
st.set_page_config(page_title="🐔 Pollos COB500", layout="wide")

# Estilos CSS personalizados
st.markdown("""
<style>
    .stNumberInput, .stDateInput, .stButton>button {
        border-radius: 10px !important;
    }
    .css-1v0mbdj {
        border: 2px solid #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Base de datos SQLite ---
def init_db():
    conn = sqlite3.connect('pollos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS crianza
                 (pollos_iniciales INT, pollos_actuales INT, 
                  fecha_inicio TEXT, pollos_muertos INT)''')
    conn.commit()
    conn.close()

def guardar_datos(pollos_iniciales, pollos_actuales, fecha_inicio, pollos_muertos):
    conn = sqlite3.connect('pollos.db')
    c = conn.cursor()
    c.execute("INSERT INTO crianza VALUES (?, ?, ?, ?)",
              (pollos_iniciales, pollos_actuales, fecha_inicio, pollos_muertos))
    conn.commit()
    conn.close()

# --- Interfaz ---
colored_header(
    label="🐔 MANEJO DE POLLOS COB500",
    description="Sistema de seguimiento de crianza",
    color_name="light-blue-70"
)

# Estado inicial
if 'pollos_muertos' not in st.session_state:
    st.session_state.pollos_muertos = 0

# 1. Configuración Inicial
with st.expander("🔧 INICIAR CRIANZA", expanded=True):
    cols = st.columns(2)
    pollos_iniciales = cols[0].number_input("Cantidad inicial de pollos", min_value=1, value=100)
    fecha_inicio = cols[1].date_input("Fecha de inicio")

    if st.button("🟢 Iniciar nueva crianza", type="primary"):
        guardar_datos(pollos_iniciales, pollos_iniciales, str(fecha_inicio), 0)
        st.success("¡Crianza iniciada!")

# 2. Registro Diario
with st.expander("📝 REGISTRO DIARIO"):
    muertos_hoy = st.number_input("Pollos muertos hoy", min_value=0, value=0)
    if st.button("✍️ Registrar"):
        st.session_state.pollos_muertos += muertos_hoy
        st.rerun()

# 3. Resumen (Tarjetas coloridas)
st.divider()
cols = st.columns(3)
cols[0].metric("🔵 Pollos vivos", f"{pollos_iniciales - st.session_state.pollos_muertos}")
cols[1].metric("🔴 Pollos muertos", st.session_state.pollos_muertos, delta=f"-{muertos_hoy} hoy")
cols[2].metric("🟢 Consumo diario", f"{(pollos_iniciales - st.session_state.pollos_muertos) * 0.2:.1f} kg")

# --- Proyección de Consumo (Tabla colorida) ---
st.divider()
st.markdown("### 📊 PROYECCIÓN DE CONSUMO")
data = {
    "Fase": ["Inicio (0-21 días)", "Crecimiento (22-35 días)", "Engorde (36-42 días)"],
    "Consumo Total": ["60 kg", "90 kg", "60 kg"]
}
st.dataframe(data, width=800, hide_index=True,
             column_config={
                 "Fase": st.column_config.TextColumn(width="medium"),
                 "Consumo Total": st.column_config.ProgressColumn(
                     format="%f kg",
                     min_value=0,
                     max_value=100
                 )
             })

# Botón de reinicio
if st.button("🗑️ Eliminar toda la crianza", type="secondary"):
    st.session_state.pollos_muertos = 0
    st.rerun()
