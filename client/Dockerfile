FROM node:24-slim

WORKDIR /app/client
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +rx /usr/local/bin/docker-entrypoint.sh && chown -R node /app && \
    apt update && apt install gosu git gnupg2 -y && apt clean
USER node

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

EXPOSE 3000
USER root
CMD ["yarn", "dev"]
