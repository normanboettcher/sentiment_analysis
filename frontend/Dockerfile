#stage 1: build
FROM node:20.9.0-alpine AS builder

WORKDIR /app
RUN corepack enable
COPY package.json yarn.lock ./
RUN yarn set version 4.9.1
#install dependencies
ENV NODE_ENV=production
RUN yarn install --immutable

#copy the rest of the project
COPY . .
#build project
RUN yarn build

#Stage 2: serve
FROM nginx:stable-alpine

#copy built files
COPY --from=builder /app/dist /usr/share/nginx/html
COPY start_frontend.sh /start_frontend.sh
RUN chmod +x /start_frontend.sh

EXPOSE 80
CMD ["/start_frontend.sh"]
