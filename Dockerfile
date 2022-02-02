FROM python:3.8.2

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD ["python","main.py"]