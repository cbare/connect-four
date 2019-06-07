#!/bin/bash

# Some fun shell hackery to demo the connect-four API.
# NOTE: requires httpie and jq

host=127.0.0.1
port=5000

set -x

http GET http://${host}:${port}/drop_token

# new game
gameId=`http --body POST http://${host}:${port}/drop_token \
                         players:='["player1", "player2"]' \
                         rows:=7 columns:=7 \
                         | jq --raw-output '.gameId'`

# get state of game
http GET http://${host}:${port}/drop_token/${gameId}

# make a bunch of moves
http POST http://${host}:${port}/drop_token/${gameId}/player1 column:=3
http POST http://${host}:${port}/drop_token/${gameId}/player2 column:=4
http POST http://${host}:${port}/drop_token/${gameId}/player1 column:=2
http POST http://${host}:${port}/drop_token/${gameId}/player2 column:=1
http POST http://${host}:${port}/drop_token/${gameId}/player1 column:=3
http POST http://${host}:${port}/drop_token/${gameId}/player2 column:=2
http POST http://${host}:${port}/drop_token/${gameId}/player1 column:=3
http POST http://${host}:${port}/drop_token/${gameId}/player2 column:=2
http POST http://${host}:${port}/drop_token/${gameId}/player1 column:=3

# get state of game, player 1 wins!
http GET http://${host}:${port}/drop_token/${gameId}

# recap moves leading to glorious victory of player 1
http GET http://${host}:${port}/drop_token/${gameId}/moves
