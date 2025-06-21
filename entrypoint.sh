#!/bin/sh
exec gunicorn app:server --bind 0.0.0.0:${PORT:-8000} --workers 2 --worker-class gevent --preload
