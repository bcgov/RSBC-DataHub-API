FROM node:18-alpine AS base
RUN apk add --no-cache g++ make py3-pip libc6-compat
WORKDIR /app
COPY package*.json ./
EXPOSE 3000

FROM base AS builder
WORKDIR /app
COPY . .
RUN npm run build

FROM base AS production
WORKDIR /app

# ENV NODE_ENV production
RUN npm ci --ignore-scripts

RUN addgroup -g 1003 -S nodegroup
RUN adduser -S nextuser -u 1003
USER nextuser

COPY --from=builder /app/.next ./.next
RUN chown nextuser:nodegroup ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

CMD npm start

FROM base AS dev
RUN npm install 

COPY package.json .
COPY package-lock.json .
#COPY /node_modules ./node_modules
COPY /src ./src
COPY /public ./public
COPY next.config.mjs .
#COPY next-env.d.ts .
COPY tsconfig.json .
COPY .eslintrc.json .

RUN addgroup -g 1003 -S nodegroup
RUN adduser -S nextuser -u 1003

RUN chown -R nextuser:nodegroup /app

USER nextuser

CMD npm run dev