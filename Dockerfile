FROM python:3.9

RUN useradd meditreats 

WORKDIR /home/meditreats

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY treats.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP treats.py

RUN chown -R meditreats:meditreats ./
USER meditreats 

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]