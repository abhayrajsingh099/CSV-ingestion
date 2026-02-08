# Step 1: Base image
FROM python:3.11-slim

# Step 2: Environment optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set working directory
WORKDIR /app

# Step 4: Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy dependency file
COPY requirements.txt .

# Step 6: Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Step 7: Copy Django project (app folder only)
COPY app/ /app/

# Step 8: Expose Django port
EXPOSE 8000

# Step 9: Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
