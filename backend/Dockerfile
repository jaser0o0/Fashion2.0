FROM python:3.11-slim

# System deps (optional, uncomment if you need them)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential curl && \
#     rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first (better build cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY . /app

# Make sure 'from core.* import ...' works
ENV PYTHONPATH=/app

EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
