# Network-based Pong Game
A Pong game running over a network through `WebSockets` protocol

# Server
- Store game state
- Edit game state with game logic
- Broadcast state changes

# Client
- Send key inputs to server
- Receive game state from server
- Render game state with `pygame`


## Start Server
```
uvicorn server.main:app --host 0.0.0.0 --port 8765
```

## Connect client
```
python .\client\main.py
```


## PYTHONPATH in powershell
```
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONPATH="C:\Users\albin\Documents\GitHub\pong\server;$env:PYTHONPATH"
```