# NetworkProject01-PokemonGame
Simple Pokemon game using socket programming in python
---
## client
send user and command to server

- user <String> : used for identifying user

- command <Array of String> used for telling server what user want to do
    - index [0] = action
    - index [1...n] = argument
---
## server
read and follow user's command and send back response

### user's command