# Build Stage
FROM node:lts-alpine as build-stage
WORKDIR /app

ARG VUE_APP_NLU_SERVICE_URL
ENV VUE_APP_NLU_SERVICE_URL=$VUE_APP_NLU_SERVICE_URL

ARG VUE_APP_NLU_PATH
ENV VUE_APP_NLU_PATH=$VUE_APP_NLU_PATH

ARG VUE_APP_NLU_ENTRIES_PAGE_SIZE
ENV VUE_APP_NLU_ENTRIES_PAGE_SIZE=$VUE_APP_NLU_ENTRIES_PAGE_SIZE

ARG PUBLIC_PATH
ENV PUBLIC_PATH=$PUBLIC_PATH

COPY package*.json ./
RUN yarn install

COPY ./ .
RUN yarn build

# Production Stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]