import asyncio
import json
import os

from src.scripts.prepare_tables import PrepareTables

data = json.load(open(os.path.join(os.path.dirname
                                   (os.path.abspath(__file__))
                                   , "rivm2016.json")))


def datapreparation():
    with PrepareTables(data) as prepare_data:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(prepare_data.geography())
        loop.run_until_complete(prepare_data.entry())
        loop.run_until_complete(prepare_data.indicator())
        loop.run_until_complete(prepare_data.impact())
        loop.close()


if __name__ == "__main__":
    datapreparation()
