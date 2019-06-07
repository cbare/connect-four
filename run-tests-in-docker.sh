#!/bin/bash

#
# Run the Flask development server in a Docker container.
#
docker run --rm \
    -e PYTHONPATH=/app/src \
    --name connect-four-test \
    christopherbare/connect-four:latest \
    test
