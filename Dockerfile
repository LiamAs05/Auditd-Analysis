FROM python:3.11

WORKDIR /app

COPY src src 

RUN apt install tk 
RUN pip install -r src/requirements.txt

CMD ["python3", "/app/src/main.py"]
