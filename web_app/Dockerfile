# FROM registry.access.redhat.com/ubi8/nodejs-16-minimal:latest AS build
FROM node:16 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build





FROM registry.access.redhat.com/ubi8/nginx-118:latest
ARG VERSION
ENV VERSION=$VERSION
COPY nginx.conf /app/nginx.conf
WORKDIR /app
COPY --from=build /app/dist /app/dist
# COPY dist /app/dist

CMD ["nginx", "-c", "/app/nginx.conf",  "-g", "daemon off;"]