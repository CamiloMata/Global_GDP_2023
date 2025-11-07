🌎 Dashboard de PIB Global (Datos 2023)
Un dashboard web interactivo construido con Streamlit que visualiza el Producto Interno Bruto (PIB) global y otros indicadores económicos clave basados en datos de 2023.

(Nota: Reemplaza el enlace de la insignia de arriba con la URL de tu aplicación una vez que la hayas desplegado).

📸 Vista Previa
¡Inserta aquí una captura de pantalla de tu dashboard! Es la mejor manera de mostrar tu trabajo.

![Captura del Dashboard](screenshot.png)

(Para que esto funcione, añade una imagen llamada screenshot.png a tu repositorio).

📋 Descripción
Este proyecto utiliza Streamlit, Pandas y Plotly para crear un dashboard dinámico que muestra:

Un mapa coroplético mundial que colorea los países según su participación porcentual en el PIB mundial.

Una tabla de datos interactiva que detalla el PIB nominal, el PIB per cápita, la población y la tasa de crecimiento del PIB de cada país.

El script está diseñado para cargar, limpiar y visualizar los datos de forma eficiente, utilizando el caché de Streamlit (@st.cache_data) para un rendimiento óptimo.

✨ Características Principales
Mapa Interactivo: Visualiza la participación global del PIB usando plotly.express. Pasa el cursor sobre un país para ver su nombre y porcentaje.

Tabla de Datos Detallada: Muestra los datos económicos clave en un formato claro y legible.

Formato de Datos Limpio: Usa la función st.column_config de Streamlit para formatear automáticamente los números como moneda ($), porcentajes (%) y enteros con separadores de miles.

Limpieza de Datos Automatizada: El script limpia automáticamente las columnas numéricas (eliminando símbolos como $, % y ,) y convierte los nombres de los países a códigos ISO-3 (requeridos por Plotly) usando la biblioteca pycountry.

📊 Fuente de Datos
Este dashboard utiliza el archivo Global GDP Explorer 2025 (World Bank UN Data).csv.

Importante: Este archivo CSV debe estar en la misma carpeta que el script dashboard.py (o app.py) para que la aplicación funcione correctamente.

🔧 Tecnologías Utilizadas
Streamlit - Para la creación de la aplicación web.

Pandas - Para la carga y manipulación de datos.

Plotly - Para la generación del mapa coroplético interactivo.

PyCountry - Para obtener los códigos de país ISO alpha-3.

🚀 Instalación y Ejecución Local
Sigue estos pasos para ejecutar el dashboard en tu máquina local.

1. Prerrequisitos
Python 3.8 o superior

Git (opcional, para clonar)

2. Clona el Repositorio
Bash

git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
3. Crea un Entorno Virtual (Recomendado)
Bash

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
4. Instala las Dependencias
Crea un archivo requirements.txt en la raíz de tu proyecto con el siguiente contenido:

Plaintext

streamlit
pandas
plotly
pycountry
Luego, instálalo usando pip:

Bash

pip install -r requirements.txt
5. Ejecuta la Aplicación
Asegúrate de que tu archivo de datos (Global GDP Explorer 2025 (World Bank UN Data).csv) esté en la misma carpeta.

Bash

streamlit run dashboard.py
¡Abre tu navegador en la dirección http://localhost:8501 para ver tu dashboard en acción!

☁️ Despliegue
Esta aplicación está lista para ser desplegada en Streamlit Community Cloud de forma gratuita. Simplemente sube tu repositorio a GitHub (asegúrate de incluir el archivo requirements.txt) y conéctalo a Streamlit Cloud.