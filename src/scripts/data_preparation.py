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
        # creating object of class PrepareTables(data)
        with PrepareTables(data) as prepare_data:
            prepare_data.geography()
            prepare_data.entry()
            prepare_data.indicator()
            prepare_data.impact()

    except Exception as e:
        print("Some issue executing the script")
        print(f"The issue:{e}")


if __name__ == "__main__":
    datapreparation()
