FROM python:3.10
ENV PYTHONBUFFERED=1
WORKDIR /backend
COPY requirements.txt .  
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /backend/
EXPOSE 8000
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]