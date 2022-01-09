FROM python:3.8-slim
ARG port

USER root
COPY . /test-app
WORKDIR /test-app

ENV PORT=$port
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apk update \
#    && apk add --virtual build-essential gcc python3-dev musl-dev libffi-dev make libevent-dev build-base \
#    && apk add postgresql-dev

#RUN adduser -D myuser
#USER myuser

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install curl \
    && apt-get install libgomp1

RUN chgrp -R 0 /test-app \
    && chmod -R g=u /test-app \
    && pip install pip --upgrade \
    && pip install -r requirements.txt
EXPOSE $PORT

RUN python3 -c "import nltk; nltk.data.path.append('/test-app/nltk_data/'); nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
COPY /root/nltk_data /test-app/nltk_data
CMD gunicorn app:server --bind 0.0.0.0:$PORT --workers 2 --worker-class gevent --preload
