FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project
COPY . .

# Expose Vite port
EXPOSE 5173

# Start Vite correctly
CMD ["npm", "start", "--", "--host"]