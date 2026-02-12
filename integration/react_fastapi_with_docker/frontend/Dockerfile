# Frontend Dockerfile - React + Vite (Development)

# Use official Node.js image (alpine = minimal size)
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files first (for better layer caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Start development server (--host 0.0.0.0 required for Docker)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
