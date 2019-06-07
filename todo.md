# To Do

## Model objects
  - [x] Board
  - [x] Game
  - [x] Player

## Infra
  - [x] In-memory store w/ suggested alternate implementations
  - [x] Docker container
  - [ ] Serve via GUnicorn
  - [ ] Type annotations
  - [ ] Generate API docs
  - [ ] Login / auth via JWT

## API
  - [x] GET /drop_token - Return all in-progress games.
  - [x] POST /drop_token - Create a new game.
  - [x] GET /drop_token/{gameId} - Get the state of the game.
  - [x] GET /drop_token/{gameId}/moves- Get (sub) list of the moves
  - [x] POST /drop_token/{gameId}/{playerId} - Post a move.
  - [x] GET /drop_token/{gameId}/moves/{move_number} - Return the
  - [x] DELETE /drop_token/{gameId}/{playerId} - Player quits

## Problems
  - [x] add QUIT move to list of moves
  - [x] test list moves api in quit and normal cases
  - [x] why do I have to caste input to int?
  - [x] exceptions to proper http error codes
  - [x] proper comment headers
  - [x] ensure that players in a game have unique tokens
  - [x] rename test_board
  - [x] home - reasonable response to root URL
