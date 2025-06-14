FROM node:18

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Set working directory for Node app
WORKDIR /app/backend

# Install Node dependencies
COPY backend/package*.json ./
RUN npm install

# Copy backend source files including Python script
COPY backend/ .

# Copy frontend files (if needed)
COPY frontend/ /app/frontend/

# Copy Python dependencies file
COPY backend/src/requirements.txt /app/backend/src/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r src/requirements.txt

EXPOSE 3000

CMD ["node", "src/app.js"]
