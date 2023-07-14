# Base docker image for node
FROM node:18

# Set directory
WORKDIR /app

# Copy settings files
COPY package.json package-lock.json tsconfig.json vite.config.ts svelte.config.js playwright.config.ts ./

# Install dependencies
RUN npm install

# Run the server
ENTRYPOINT [ "npm", "run", "dev", "--", "--host", "0.0.0.0"]
