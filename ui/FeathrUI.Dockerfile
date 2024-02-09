FROM node:16-alpine as ui-build

RUN mkdir -p /usr/src/ui
WORKDIR /usr/src/ui
COPY ./ /usr/src/ui
RUN npm install && npm run build

FROM nginx:alpine

COPY --from=ui-build /usr/src/ui/build /usr/share/nginx/html
COPY --from=ui-build /usr/src/ui/build /etc/nginx/html

COPY ./deploy/nginx.conf /etc/nginx/nginx.conf
COPY ./deploy/start.sh .

EXPOSE 3000

RUN ["chmod", "+x", "./start.sh"]
