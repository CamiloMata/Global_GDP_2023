import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry  # Necesario para obtener los códigos ISO de los países

# --- Configuración de la Página ---
# Usamos un layout ancho para que el dashboard ocupe más espacio
st.set_page_config(layout="wide")

# --- Funciones de Carga y Limpieza de Datos ---

@st.cache_data  # Cache para no recargar/reprocesar los datos en cada interacción
def load_and_clean_data(filepath):
    """
    Carga el CSV, limpia las columnas numéricas y obtiene los códigos ISO.
    """
    try:
        df = pd.read_csv(filepath, index_col=0)
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo '{filepath}'.")
        st.error("Asegúrate de que el archivo CSV esté en la misma carpeta que `app.py`.")
        return pd.DataFrame() # Devuelve un DataFrame vacío si hay error

    # 1. Limpieza de columnas numéricas (quitar $, % y comas)
    
    # Limpiar 'Share of World GDP' y renombrar para claridad
    if 'Share of World GDP' in df.columns and df['Share of World GDP'].dtype == 'object':
        df['Share %'] = df['Share of World GDP'].str.replace('%', '', regex=False).astype(float)
    
    # Limpiar 'GDP Growth'
    if 'GDP Growth' in df.columns and df['GDP Growth'].dtype == 'object':
        df['GDP Growth'] = df['GDP Growth'].str.replace('%', '', regex=False)
        # Convertir a numérico, los errores (ej. 'N/A') se volverán NaN
        df['GDP Growth'] = pd.to_numeric(df['GDP Growth'], errors='coerce')

    # Limpiar columnas con '$' y ','
    cols_to_clean = ['GDP (nominal, 2023)', 'GDP per capita', 'Population 2023']
    for col in cols_to_clean:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].str.replace(r'[$,]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Obtener códigos ISO para el mapa
    def get_iso_code(country_name):
        """
        Busca el código ISO alpha-3 para un nombre de país.
        """
        try:
            # search_fuzzy es bueno para encontrar coincidencias ligeras
            return pycountry.countries.search_fuzzy(country_name)[0].alpha_3
        except LookupError:
            # Si no se encuentra, devolvemos None para que Plotly lo ignore
            return None

    df['ISO_Code'] = df['Country'].apply(get_iso_code)
    
    return df

# --- Carga de Datos ---
# Asegúrate de que el nombre del archivo coincida exactamente
file_path = "Global GDP Explorer 2025 (World Bank  UN Data).csv"
df = load_and_clean_data(file_path)

# --- Layout del Dashboard ---

st.title("🌎 Dashboard de PIB Global (Datos 2023)")

st.markdown("""
Este dashboard interactivo muestra la participación de cada país en el PIB mundial,
basado en datos de 2023. Usa el mapa para explorar visualmente la participación
y consulta la tabla inferior para obtener detalles económicos específicos.
""")

st.markdown("---") # Separador horizontal

# --- 1. Mapa Coroplético ---
st.header("Mapa de Participación en el PIB Mundial")

if not df.empty and 'ISO_Code' in df.columns and 'Share %' in df.columns:
    # Filtramos las filas donde no pudimos encontrar un ISO_Code
    map_df = df.dropna(subset=['ISO_Code', 'Share %'])

    fig = px.choropleth(
        map_df,
        locations="ISO_Code",                 # Columna con códigos ISO
        color="Share %",                      # Columna para la escala de color
        hover_name="Country",                 # Qué mostrar al pasar el ratón
        hover_data={                          # Datos extra en el hover
            "Share %": ":.2f%",               # Formatear como porcentaje
            "GDP (abbrev.)": True,
            "ISO_Code": False                 # Ocultar el ISO_Code
        },
        color_continuous_scale=px.colors.sequential.Plasma, # Paleta de colores
        title="Participación en el PIB Mundial (%)"
    )
    
    # Ajustes de diseño para un look más limpio
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0), # Márgenes ajustados
        geo=dict(
            showframe=False,              # Sin marco alrededor del mapa
            showcoastlines=False,         # Sin líneas de costa
            projection_type='natural earth' # Tipo de proyección
        )
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No se pudieron generar los datos del mapa. Verifica el archivo CSV.")


# --- 2. Tabla de Datos ---
st.header("Tabla de Datos Económicos")

if not df.empty:
    # Columnas solicitadas para la tabla
    columns_to_show = [
        "Country",
        "GDP (nominal, 2023)",
        "GDP per capita",
        "Population 2023",
        "GDP Growth"
    ]
    
    # Asegurarnos de que todas las columnas existan
    available_columns = [col for col in columns_to_show if col in df.columns]
    df_table = df[available_columns]
    
    # Usamos st.dataframe para mostrar la tabla
    st.dataframe(
        df_table,
        use_container_width=True, 
        hide_index=True,          
        
        # --- AQUÍ OCURRE LA MAGIA ---
        column_config={
            
            # Columna: Country (Texto)
            # No la listamos aquí, así que usa el formato por defecto.
            # Si quisieras renombrarla a "País", añadirías:
            # "Country": st.column_config.TextColumn("País"),

            # Columna: GDP (nominal, 2023)
            "GDP (nominal, 2023)": st.column_config.NumberColumn(
                "PIB Nominal (2023)",  # Nuevo nombre para la cabecera
                format="$%0f"         # Formato: Símbolo '$', sin decimales
            ),
            
            # Columna: GDP per capita
            "GDP per capita": st.column_config.NumberColumn(
                "PIB per Cápita",       # Nuevo nombre
                format="$%.0f"         # Formato: Símbolo '$', sin decimales
            ),
            
            # Columna: Population 2023
            "Population 2023": st.column_config.NumberColumn(
                "Población (2023)",    # Nuevo nombre
                format="%d"            # Formato: Número entero (Streamlit añadirá comas)
            ),
            
            # Columna: GDP Growth
            "GDP Growth": st.column_config.NumberColumn(
                "Crecimiento PIB (%)", # Nuevo nombre
                format="%.2f%%"        # Formato: 2 decimales y el símbolo '%'
            )
        }
    )
else:
    st.warning("No se pudieron cargar los datos para la tabla.")