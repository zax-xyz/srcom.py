# srcom.py

**This project is a work in progress.**

An asynchronous Python wrapper for the speedrun.com REST API. Currently it focuses on the most important parts of the API, i.e., games, runs, users. It follows an object-oriented design, with methods integrating different parts of the API together and allowing simple retrieval of information.

## Simple Example

```py
import asyncio

import srcom


async def main():
    client = srcom.Client()

    # Exact match by abbreviation
    game = await client.get_game(abbreviation="khfm")

    # Make sure to close the HTTP session!
    await client.close()

    # You can also use a context manager to automatically close the client
    async with srcom.Client() as client:
        # Fuzzy search game by name
        game = await client.get_game(name="Kingdom Hearts II")
        # You can get any resource directly from its ID as well
        game = await srcom.Game.from_id(game.id, client)

        # Gets the 3 fastest runs for the default category
        for run in await game.leaderboard(3):
            await print_run(run)

        print()

        # Returns at most 20 runs (default limit in API)
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
