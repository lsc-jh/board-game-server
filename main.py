import asyncio
import json
import websockets
from game import Game

game = Game()
connected = {}

async def handle_client(ws, path):
    player_id = f"player{len(connected) + 1}"
    connected[player_id] = ws
    game.add_player(player_id)

    await ws.send(json.dumps(game.get_init()))

    try:
        while True:
            data = await ws.recv()
            msg = json.loads(data)

            if msg["type"] == "move":
                game.move_player(player_id, msg["dir"])

            state = game.get_state(player_id)
            await asyncio.gather(*[
                conn.send(json.dumps(state))
                for conn in connected.values()
            ])
    except websockets.exceptions.ConnectionClosed:
        game.remove_player(player_id)
        connected.pop(player_id, None)

start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

print("Server running at ws://0.0.0.0:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()