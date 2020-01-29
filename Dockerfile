FROM python:3

MAINTAINER daemonchild

COPY app/ /app/
ADD requirements.txt /app/

RUN pip install -r /app/requirements.txt

EXPOSE 8000

CMD [ "python", "/app/app.py" ]