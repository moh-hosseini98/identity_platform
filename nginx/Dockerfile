FROM nginx:1.31.1-alpine-slim

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/default.conf



EXPOSE 80
