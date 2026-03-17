#!/bin/bash
exec python3 -m gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT main:app
