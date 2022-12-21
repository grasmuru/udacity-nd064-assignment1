FROM python:3.11

WORKDIR /techtrends

ADD . .

RUN pip install -r techtrends/requirements.txt

EXPOSE 3111

RUN python techtrends/init_db.py

CMD ["python", "techtrends/app.py"]

