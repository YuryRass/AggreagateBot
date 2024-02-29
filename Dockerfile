FROM python:3.10-slim

RUN mkdir /bot

WORKDIR /bot

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
