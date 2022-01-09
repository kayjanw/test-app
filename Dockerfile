FROM python:3.8-slim
ARG port

USER root
COPY . /test-app
WORKDIR /test-app

ENV PORT=$port
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install curl \
    && apt-get install libgomp1

RUN chgrp -R 0 /test-app \
    && chmod -R g=u /test-app \
    && pip install pip --upgrade \
    && pip install -r requirements.txt
EXPOSE $PORT

RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
RUN cp -r /root/nltk_data /usr/local/share/

RUN ls -lh
RUN python3 -m unittest discover -s tests/ -p "test_*.py"
CMD gunicorn app:server --bind 0.0.0.0:$PORT --workers 2 --worker-class gevent --preload
