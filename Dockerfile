FROM python:3.8-slim
ARG port

USER root
COPY . /test-app
WORKDIR /test-app

# COPY data/MetaTrader5/MetaTrader5 /usr/local/lib/python3.8/site-packages/MetaTrader5
# COPY data/MetaTrader5/MetaTrader5-5.0.37.dist-info /usr/local/lib/python3.8/site-packages/MetaTrader5-5.0.37.dist-info
ENV PORT=$port
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# EXPOSE $PORT

RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y --no-install-recommends curl \
    && apt-get install --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && chgrp -R 0 /test-app \
    && chmod -R g=u /test-app \
    && pip install pip --upgrade \
    && pip install -U -r requirements.txt \
    && python3 -c "import nltk; nltk.download('punkt_tab')" \
    && cp -r /root/nltk_data /usr/local/share/
RUN python3 -m unittest discover -s tests/ -p "test_*.py" \
    && ls -lh
CMD gunicorn app:server --bind 0.0.0.0:$PORT --workers 2 --worker-class gevent --preload
