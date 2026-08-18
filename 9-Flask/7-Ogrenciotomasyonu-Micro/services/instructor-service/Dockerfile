FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5005
ENV DB_PATH=/data/instructors.db

EXPOSE 5005

CMD ["python", "app.py"]
