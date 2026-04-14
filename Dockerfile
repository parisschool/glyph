FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install .

CMD ["python", "prueba.py"]
