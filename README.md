# connect-four

An api for playing the game connect-four.


## Running in Docker

To build a Docker image hosting the application, run this in the project root:

```
docker build -t christopherbare/connect-four:latest .
```

We can run the flask development server in a Docker container with the following command:

```
./run-dev-in-docker.sh
```

To run the tests in a Docker container:

```
./run-tests-in-docker.sh
```

## Local Development

The flask web service can be run for local development with this command:

```
PYTHONPATH=`pwd`/src FLASK_APP=api.py flask run --reload
```


### Testing

To run test suite:

```
PYTHONPATH=`pwd`/src py.test -v
```

To see output of tests, add the -s flag:

```
PYTHONPATH=`pwd`/src py.test -vs
```

## Configuration

This code has been tested on:
 * MacOS 10.14.5 & Python 3.7.0
 * Amazon Linux AMI release 2018.03 & Python 3.6.8
