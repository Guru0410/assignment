FROM node:14

WORKDIR /usr/src/app/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
COPY package*.json ./

RUN npm install

COPY . .

RUN ls /usr/src/app/target

EXPOSE 9997

#CMD [ "node", "app.js", "splitter"]
