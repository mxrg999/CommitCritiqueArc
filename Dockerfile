FROM python:latest

WORKDIR /usr/app/src

COPY ./ /usr/app/src/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]