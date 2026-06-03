FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

FROM nginx:1.27-alpine

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/certs/localhost.crt /etc/nginx/certs/localhost.crt
COPY nginx/certs/localhost.key /etc/nginx/certs/localhost.key
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

EXPOSE 80 443
