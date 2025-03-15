# Sử dụng Python 3.10 làm base image
FROM python:3.10

# Đặt thư mục làm việc trong container
WORKDIR /backend

# Sao chép file requirements.txt vào container và cài đặt
COPY requirements.txt .  
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ project vào container
COPY . .

# Expose port 8000 (cổng chạy Django)
EXPOSE 8000

# Lệnh khởi động mặc định (không cần entrypoint.sh)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
