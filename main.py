import asyncio
import json
from typing import Dict
import websockets
from game import Game

game = Game()
connected: Dict[str, websockets.ClientConnection] = {}

async def broadcast_all():
    to_remove = []
    for pid, ws in connected.items():
        try:
            state = game.get_state(pid)
            await ws.send(json.dumps(state))
        except:
            to_remove.append(pid)
    for pid in to_remove:
        game.remove_player(pid)
        connected.pop(pid, None)


async def handle_client(ws):
    player_id = game.add_player()
    connected[player_id] = ws
    print(f"{player_id} connected")

    await ws.send(json.dumps(game.get_init()))

    try:
        async for message in ws:
            msg = json.loads(message)
            if msg["type"] == "move":
                game.move_player(player_id, msg["dir"])
    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        game.remove_player(player_id)
        connected.pop(player_id, None)
        print(f"{player_id} disconnected")


async def game_loop():
    while True:
        game.move_enemies()
        await broadcast_all()
        await asyncio.sleep(0.10)


async def main():
    print("Server running at ws://0.0.0.0:8765")
    asyncio.create_task(game_loop())
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
