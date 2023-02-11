FROM python:3.10

WORKDIR /app

COPY . /src
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
