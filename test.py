import asyncio

import srcom


async def print_run(run):
    player = await run.player()
    print(', '.join((
        run.time,
        player.name,
        player.country or 'NONE',
        (await run.category()).name,
        run.link,
    )))


async def main():
    async with srcom.Client() as client:
        game = await client.get_game(name="Kingdom Hearts II")
        game_by_id = await srcom.Game.from_id(game.id, client.http)

        assert type(game.id) == str
        assert game.id == game_by_id.id
        assert game == game_by_id

        for run in await game.leaderboard(3):
            assert run.status == "verified"
            await print_run(run)

        print()

        record = await game.record()
        await print_run(record)

        assert await record.game() == game


asyncio.get_event_loop().run_until_complete(main())
