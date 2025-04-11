import asyncio
import json
import websockets
from game import Game

game = Game()
connected = {}

async def handle_client(ws):
    player_id = f"player{len(connected) + 1}"
    print(f"New connection: {player_id}")
    connected[player_id] = ws
    game.add_player(player_id)

    await ws.send(json.dumps(game.get_init()))

    try:
        while True:
            data = await ws.recv()
            msg = json.loads(data)
            print(f"Received message from {player_id}: {msg}")
            if msg["type"] == "move":
                game.move_player(player_id, msg["dir"])

            state = game.get_state(player_id)
            await asyncio.gather(*[
                conn.send(json.dumps(state))
                for conn in connected.values()
            ])
    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed for {player_id}")
        game.remove_player(player_id)
        connected.pop(player_id, None)

async def main():
    print("Server running at ws://0.0.0.0:8765")
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
