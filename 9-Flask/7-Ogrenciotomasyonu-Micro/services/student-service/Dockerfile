FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5004
ENV DB_PATH=/data/students.db

EXPOSE 5004

CMD ["python", "app.py"]
