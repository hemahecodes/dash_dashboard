FROM python:3.6

USER root
ENV DASH_DEBUG_MODE True

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install -r requirements.txt

EXPOSE 8050

ENV NAME Dash

CMD ["python", "index.py"]