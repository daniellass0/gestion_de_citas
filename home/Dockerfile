FROM nginx:alpine

# Copiamos los archivos de la vista al directorio que Nginx sirve por defecto
COPY index.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/styles.css

# Nginx escucha por defecto en el puerto 80
EXPOSE 80

# La imagen base de Nginx ya inicia el servidor automáticamente al arrancar
