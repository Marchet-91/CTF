FROM node:14

WORKDIR /usr/src/app

COPY package*.json ./
COPY app .

COPY flag.txt /flag.txt
RUN chmod 400 /flag.txt

RUN npm install

EXPOSE 3000

CMD [ "node", "app.js" ]
