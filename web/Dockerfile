# Imagen oficial de Nginx (ligera)
FROM nginx:1.27-alpine

# Reemplazamos la configuración por defecto por la nuestra
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
