FROM node:18

WORKDIR /app/backend

COPY backend/package*.json ./
RUN npm install

# Copy backend code
COPY backend/ .

# Copy frontend from root (you must build from project root)
COPY frontend/ /app/frontend/

EXPOSE 3000
CMD ["node", "src/app.js"]
