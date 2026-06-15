FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ServerQ1.py .

EXPOSE 5000

CMD ["python", "ServerQ1.py"]
