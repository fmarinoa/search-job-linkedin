# Search Job LinkedIn

## Descripción

Este proyecto automatiza la búsqueda de ofertas laborales en LinkedIn a partir de dos parámetros principales:
- **Descripción del trabajo**
- **Locación**

Utilizando la librería `requests`, el script obtiene la siguiente información de cada oferta encontrada:
- Título del puesto
- Empresa empleadora y su perfil
- Ubicación de la oferta
- Tiempo transcurrido desde su publicación
- Enlace directo a la oferta
- Nombre y perfil del reclutador (si existe)
- Descripción de la oferta

Los datos obtenidos se almacenan en:
- Archivos CSV dentro de `results/<año,mes.dia>/results_<hora,minuto.segundo>.csv`
- Un archivo JSON centralizado en `results/offers.json`

Además, se genera automáticamente un archivo HTML con la información recopilada.

## Automatización con GitHub Actions

El proyecto incorpora un flujo de trabajo de GitHub Actions que:
1. Ejecuta el script principal.
2. Realiza un commit automático de los datos actualizados.
3. Genera un archivo HTML con las ofertas.
4. Envía un correo con los resultados al usuario, utilizando las credenciales almacenadas en los secretos de GitHub.

## Tecnologías utilizadas
- **Python 3.11**
- **Requests** para la obtención de datos
- **Pathlib** para el manejo de rutas
- **GitHub Actions** para la automatización de ejecución y envío de correos
- **CSV y JSON** para el almacenamiento de datos
- **HTML y CSS** para la presentación de ofertas

---
