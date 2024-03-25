# Dockerfile for NextJS applications 

# Use the official Node.js image as base 
FROM node:18-alpine

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


# Command to run the application
RUN mkdir /.npm
RUN chgrp -R 0 /.npm && \
    chmod -R g=u /.npm

ENTRYPOINT [ "npm", "run" ]
CMD [ "start"]
