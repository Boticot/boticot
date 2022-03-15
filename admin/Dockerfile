# Build Stage
FROM node:lts-alpine as build-stage
WORKDIR /app

COPY package*.json ./
RUN yarn install

COPY ./ .
RUN yarn build

# Production Stage
FROM nginx:stable-alpine as production-stage
WORKDIR /usr/share/nginx/html
COPY --from=build-stage /app/dist .
COPY ./entrypoint.sh /entrypoint.sh
EXPOSE 80
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
