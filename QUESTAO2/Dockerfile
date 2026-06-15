FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ServerUDP.py .

EXPOSE 6000/udp

CMD ["python", "ServerUDP.py"]
