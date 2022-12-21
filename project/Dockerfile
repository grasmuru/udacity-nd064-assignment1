FROM python:3.11

WORKDIR /techtrends

ADD . .

RUN pip install -r requirements.txt

EXPOSE 3111

RUN python init_db.py

CMD ["python", "app.py"]

