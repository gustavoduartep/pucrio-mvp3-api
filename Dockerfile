FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Comando para iniciar o servidor Flask.
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
