# Stage 0, "build-stage", based on Node.js, to build and compile the frontend with multi-stage builds
FROM node:22.12 as build-stage

WORKDIR /app

COPY package*.json package-lock.json /app/

RUN npm install -g npm@latest

RUN npm install

COPY ./ /app/

ARG configuration=production

RUN npm run build --configuration=production

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.28

COPY nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stage 1
COPY --from=build-stage /app/dist/dreamboard/browser /usr/share/nginx/html

RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 8080