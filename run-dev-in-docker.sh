#!/bin/bash

#
# Run the Flask development server in a Docker container.
#
docker run --rm -d \
    -e PYTHONPATH=/app/src \
    -e FLASK_APP=api.py \
    -p 5000:5000 \
    --name connect-four \
    christopherbare/connect-four:latest \
    flask

docker ps
