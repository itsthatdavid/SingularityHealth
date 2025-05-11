# Location: SINGULARITYHEALTH/frontend/Dockerfile
FROM node:18-alpine AS development

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
# If you use yarn:
# COPY yarn.lock ./
# RUN yarn install --frozen-lockfile

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]