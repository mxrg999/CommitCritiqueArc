FROM python:latest

WORKDIR /usr/app/src

COPY ./ /usr/app/src/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]