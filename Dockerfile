FROM node:22-alpine AS build
WORKDIR /source
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY docs ./docs
COPY scripts ./scripts
ARG DOCS_BASE=/
ENV DOCS_BASE=${DOCS_BASE}
ENV DOCS_ARCHIVE_BUILD=true
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /source/docs/.vitepress/dist /usr/share/nginx/html
EXPOSE 8080
