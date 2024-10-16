Simulación de Data Scientist en Steam<br><br>
Descripción:<br>
Este proyecto simula el trabajo de un Data Scientist en la empresa Steam, con el objetivo de analizar datos de la 
plataforma, realizar una limpieza de datos, crear una API, explorar los datos a través de un Análisis Exploratorio (EDA) y 
desarrollar un sistema de recomendación de videojuegos en base a un juego dado.

Contenido del Proyecto:<br>
Limpieza de Datos: Preprocesamiento de los datos para asegurar su calidad, eliminando valores nulos, duplicados y 
transformando variables para mejorar su análisis.<br>
API con FastAPI: Implementación de una API para interactuar con los datos procesados, permitiendo realizar consultas sobre
los usuarios y obtener la cantidad de juegos comprados y su porcentaje de juegos que fueron comprados por recomendación.<br>
Análisis Exploratorio de Datos (EDA): Visualización y análisis de las características de los juegos disponibles,
explorando variables como precios y desarrolladores.<br>
Sistema de Recomendación: Desarrollo de un sistema de recomendación de juegos basado en la similitud entre juegos
(utilizando la similitud del coseno), utilizando métricas de distancia y técnicas de Machine Learning.<br><br>

Instalación<br><br>

1. Clona este repositorio:  <br>
git clone https://github.com/tuusuario/tu-repositorio.git <br>
cd tu-repositorio <br><br>

2. Crea un entorno virtual (opcional pero lo recomiendo): <br>
python -m venv venv  <br>
venv\Scripts\activate  <br><br>


3. Instala las dependencias necesarias:  <br>
pip install -r requirements.txt  <br><br>

4. Inicia la API: <br>
uvicorn main:app --reload <br><br>

Uso:  <br>
API: Consulta la documentación interactiva de la API en http://localhost:8000/docs una vez que esté en funcionamiento. <br><br>

Sistema de Recomendación: Envía una solicitud a la API con el id de un juego para obtener una lista de
recomendaciones basadas en la similitud.  <br><br>

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, sigue estos pasos:<br>

1. Haz un fork del repositorio.<br>
2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).<br>
3. Realiza tus cambios y haz commits (git commit -m 'Añadir nueva funcionalidad').<br>
4. Envía un pull request.<br><br><br>

Este proyecto fue desarrollado por Cristo Benjamín como parte de un ejercicio de simulación de 
trabajo en ciencia de datos. <br><br>

Licencia: Código abierto. <br><br>

Si tienes alguna pregunta o sugerencia, no dudes en contactarme a través de mi perfil de GitHub. <br><br>


Link del video: https://www.youtube.com/watch?v=SXYbDvxgFkA

