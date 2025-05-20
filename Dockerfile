# Sử dụng Python base image
FROM python:3.10-slim

# Tạo thư mục làm việc trong container
WORKDIR /app

# Copy các file cần thiết
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Chạy ứng dụng
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]