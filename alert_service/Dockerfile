# === Base Image ===
# Use a lightweight Python 3.11 image
FROM python:3.11-slim

# === Set Working Directory ===
WORKDIR /app

# === Copy Application Files ===
COPY . .

# === Install System Dependencies ===
# 'curl' is often useful for debugging or health checks
RUN apt update && apt install -y curl && apt clean

# === Install Python Dependencies ===
RUN pip install --no-cache-dir requests yagmail schedule python-dotenv

# === Default Command ===
# Run the alert service when the container starts
CMD ["python", "alert_service.py"]
