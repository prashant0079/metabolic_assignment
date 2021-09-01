import asyncio
import json
import os

from src.scripts.prepare_tables import PrepareTables

# opening json file
data = json.load(open(os.path.join(os.path.dirname
                                   (os.path.abspath(__file__))
                                   , "rivm2016.json")))


def datapreparation():
    """Utility to insert data to the tables"""
    try:
        # creating object of class PrepareTables(data) in the context manager
        with PrepareTables(data) as prepare_data:
            # creating event loop for executing async transactions
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # running async tasks one by one in the event loop
            # so to avoid concurrent insertions
            loop.run_until_complete(prepare_data.geography())
            loop.run_until_complete(prepare_data.entry())
            loop.run_until_complete(prepare_data.indicator())
            loop.run_until_complete(prepare_data.impact())
            # closing event loop
            loop.close()

    except Exception as e:
        print("Some issue executing the script")
        print(f"The issue:{e}")


if __name__ == "__main__":
    datapreparation()
