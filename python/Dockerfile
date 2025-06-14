# python/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Python requirements first for better layer-caching
COPY python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the crawler Flask app
COPY python/ .

# If your script is called scripts.py and already contains:
#     if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)
# you can run it directly.
EXPOSE 5000

CMD ["python", "scripts.py"]
