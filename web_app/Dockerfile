FROM nginx:latest
COPY nginx.conf /app/nginx.conf
WORKDIR /app
COPY dist /app/dist

CMD ["nginx", "-c", "/app/nginx.conf",  "-g", "daemon off;"]

