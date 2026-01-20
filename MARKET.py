import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="🛒Supermercado El Más Barato🛒- El Más Barato", layout="centered", page_icon="🔵")

# Estilo CSS para aplicar los colores
st.markdown("""
    <style>
    /* Color de fondo de la app */
    .stApp {
        background-color: #000000;
    }
    
    /* Personalización de botones */
    .stButton>button {
        width: 100%;
        border-radius: 20px; /* Bordes redondeados estilo  */
        background-color: #ffc220; /* Amarillo  */
        color: #0071ce; /* Azul  */
        font-weight: bold;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #e5ac1d;
        color: #0071ce;
    }

    /* Estilo de la factura */
    .factura-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #0071ce; /* Borde azul */
        color: #333333;
        font-family: 'Arial', sans-serif;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    
    .header {
        background-color: #0071ce;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px 10px 0 0;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicializar el carrito
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame(
        columns=["producto", "precio", "cantidad", "subtotal"]
    )

def agregar_producto(nombre, precio, cantidad):
    if nombre and precio > 0 and cantidad > 0:
        subtotal = float(precio) * float(cantidad)
        nueva_fila = {"producto": nombre, "precio": precio, "cantidad": cantidad, "subtotal": subtotal}
        st.session_state.table_data = pd.concat([st.session_state.table_data, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.toast(f"✅ {nombre} añadido al carrito", icon='🛒')
    else:
        st.error("⚠️ Datos inválidos")

# 3. Interfaz de Usuario
st.markdown("<h1 style='text-align: center; color: #0071ce;'>🛒Supermercado El Más Barato🛒</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Ahorra dinero. Vive mejor.</p>", unsafe_allow_html=True)

with st.expander("➕ Agregar Producto", expanded=True):
    with st.form("producto_form", clear_on_submit=True):
        producto_nombre = st.text_input("Nombre del producto")
        col1, col2 = st.columns(2)
        with col1:
            producto_precio = st.number_input("Precio (L.)", min_value=0.0, step=0.01)
        with col2:
            producto_cantidad = st.number_input("Cantidad", min_value=1, step=1)
        
        subtotal_button = st.form_submit_button("Añadir al carrito 🛒")

if subtotal_button:
    agregar_producto(producto_nombre, producto_precio, producto_cantidad)

# 4. Tabla Visual
st.subheader("📋 Resumen de Compra")
st.dataframe(st.session_state.table_data, use_container_width=True)

# 5. Factura y Totales
if not st.session_state.table_data.empty:
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("🧾 Generar Factura", type="secondary"):
            st.session_state.ver_factura = True
    
    with col_b:
        if st.button("🗑️ Vaciar Carrito"):
            st.session_state.table_data = pd.DataFrame(columns=["producto", "precio", "cantidad", "subtotal"])
            if "ver_factura" in st.session_state: del st.session_state.ver_factura
            st.rerun()

    if "ver_factura" in st.session_state:
         subtotal = st.session_state.table_data["subtotal"].sum()
    
    # 2. Ahora sí podemos usar la variable 'subtotal'
         impuesto = subtotal * 0.15
         total_final = subtotal + impuesto
    
    

        # Diseño de Factura 
         st.markdown(f"""
        <div class="factura-box">
            <div class="header">
                <h2 style='margin:0;'>   🛒Supermercado El Más Barato🛒</h2>
                <p style='margin:0; font-size: 0.8em;'>Recibo de Venta</p>
            </div>
            <p style='text-align: center; font-size: 0.9em;'>
                <b>Sucursal Honduras</b><br>
                {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </p>
            <hr style='border: 1px dashed #0071ce;'>
            <table style='width:100%; border-collapse: collapse;'>
                <tr style='border-bottom: 2px solid #0071ce; color: #0071ce;'>
                    <th style='text-align:left'>Cant.</th>
                    <th style='text-align:left'>Articulo</th>
                    <th style='text-align:right'>Total</th>
                </tr>
                {"".join([f"<tr style='border-bottom: 1px solid #eee;'><td style='padding:5px 0;'>{int(r.cantidad)}</td><td>{r.producto}</td><td style='text-align:right'>L. {r.subtotal:,.2f}</td></tr>" for i, r in st.session_state.table_data.iterrows()])}
            </table>
            <div style='margin-top: 15px; padding: 10px; background-color: #f9f9f9; border-radius: 5px;'>
            <p style='margin:0; text-align: right;'>Subtotal: <b>L. {subtotal:,.2f}</b></p>
            <p style='margin:0; text-align: right;'>ISV (15%): <b>L. {impuesto:,.2f}</b></p>
            <hr style='border: 0.5px solid #0071ce;'>
            <h3 style='text-align: right; color: #0071ce; margin:0;'>TOTAL A PAGAR: L. {total_final:,.2f}</h3>
             </div>
            <br>
            <p style='text-align: center; font-size: 0.8em; color: #777;'>
                ¡Gracias por su compra!<br>
                *** Ahorra dinero. Vive mejor. ***
            </p>
        </div>
        """, unsafe_allow_html=True)