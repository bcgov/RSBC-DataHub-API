FROM registry.access.redhat.com/ubi8/nginx-118:latest
COPY nginx.conf /app/nginx.conf
WORKDIR /app
COPY dist /app/dist

CMD ["nginx", "-c", "/app/nginx.conf",  "-g", "daemon off;"]

