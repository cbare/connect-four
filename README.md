# connect-four

An api for playing the game connect-four.




## Local Development

The flask web service can be run for local development with this command:

```
PYTHONPATH=`pwd`/src FLASK_APP=api.py flask run --reload
```


## Testing

To run test suite:

```
PYTHONPATH=`pwd`/src py.test -v tests/
```

To see output of tests, add the -s flag:

```
PYTHONPATH=`pwd`/src py.test -vs tests/
```
