FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5003
ENV DB_PATH=/data/titles.db

EXPOSE 5003

CMD ["python", "app.py"]
