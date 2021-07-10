# srcom.py

**This project is a work in progress.**

An asynchronous Python wrapper for the speedrun.com REST API. Currently it focuses on the most important parts of the API. I.e., games, runs, users. It follow an object-oriented design, with methods integrating different parts of the API together and allowing the simple retrieval of information.

## Simple Example

```py
import asyncio

import srcom


async def main():
    client = srcom.Client()
    game = await client.get_game(abbreviation="khfm")
    await client.close()

    # You can also use a context manager for automatically closing the client
    async with srcom.Client() as client:
        # Searches for game by name
        game = await client.get_game(name="Kingdom Hearts II")

        # Gets the 3 fastest runs for the default category
        for run in await game.leaderboard(3):
            await print_run(run)

        print()

        for run in await game.runs():
            await print_run(run)

        print()

        # Gets the WR for the default category for the game
        record = await game.record()
        await print_run(record)


async def print_run(run):
    # Retrieve the runner
    player = await run.player()
    print("{}    {}    {}    {}".format(
        run.time,
        player.name,
        player.country or 'NONE',  # player.country can be None
        (await run.category()).name,
        run.link,  # direct link to run on speedrun.com
    ))


asyncio.get_event_loop().run_until_complete(main())
```
