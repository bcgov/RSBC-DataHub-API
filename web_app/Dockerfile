# Dockerfile for NextJS applications 

# Use the official Node.js image as base 
FROM node:18-alpine

ENV EMAIL_BASE_URL=$EMAIL_BASE_URL
ENV EMAIL_BASIC_AUTH=$EMAIL_BASIC_AUTH
ENV EMAIL_BASIC_AUTH_USER=$EMAIL_BASIC_AUTH_USER
ENV CLAMAV_VIRUS_SCAN_URL=$CLAMAV_VIRUS_SCAN_URL
ENV CLAMAV_CLIENT_BASIC_AUTH_USER=$CLAMAV_CLIENT_BASIC_AUTH_USER
ENV CLAMAV_CLIENT_BASIC_AUTH=$CLAMAV_CLIENT_BASIC_AUTH
ENV FLASK_API_ENDPOINT=$FLASK_API_ENDPOINT
ENV FLASK_BASIC_AUTH_USER=$FLASK_BASIC_AUTH_USER
ENV FLASK_BASIC_AUTH=$FLASK_BASIC_AUTH

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container 
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Expose the port that your Next.js app runs on
EXPOSE 3000

# Build the Next.js application
RUN npm run build


RUN ls -la /app
RUN ls -la /app/.next/cache
# Command to run the application
RUN mkdir /app/.next/cache/images  && chmod -R 777 /app/.next/cache
RUN ls -la /app/.next/cache
RUN mkdir /.npm

RUN chgrp -R 0 /.npm && \
    chmod -R g=u /.npm

#ENTRYPOINT [ "npm", "run" ]
CMD ["npm", "start"]