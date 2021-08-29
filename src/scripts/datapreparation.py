import json
import os
import asyncio

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.geography import Geography
from src.models.entry import Entry
from src.models.indicator import Indicator
from src.models.impact import Impact

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rivm2016.json")
f = open(json_file, )
data = json.load(f)


async def geography_data():
    geography_nl = Geography(country_id="NL", short_name="NLD", name="The Netherlands")
    session.add(geography_nl)
    session.commit()
    await asyncio.sleep(3)


async def entries_data():
    entries = []
    for record in data:
        if record["Ecoinvent process OR other names"] != "":
            product_name = record["Ecoinvent process OR other names"].split(", [NL]")[0]
            unit = record["Unit"]
            geography_id = 1  # only one geography i.e. The Netherlands
            entry_object = Entry(product_name=product_name, unit=unit, geography_id=geography_id)
            entries.append(entry_object)

    session.add_all(entries)
    session.commit()
    await asyncio.sleep(3)


async def indicator_data():
    indicators = []
    ignore_properties = ["Data source", "Ecoinvent process OR other names", "Unit", "Reference quantity", ""]
    for key, value in data[0].items():
        if key not in ignore_properties:
            method, category, indicator = key.split(":")
            indicator_object = Indicator(method=method, category=category, indicator=indicator, unit=value)
            indicators.append(indicator_object)

    session.add_all(indicators)
    session.commit()
    await asyncio.sleep(3)


async def impact_data():
    impacts = []
    ignore_properties = ["Data source", "Ecoinvent process OR other names",
                         "Unit", "Reference quantity", ""]
    for record in data:
        if record["Ecoinvent process OR other names"] != "":
            product_name = record["Ecoinvent process OR other names"].split(", [NL]")[0]
            entry = session.query(Entry).filter(Entry.product_name == product_name).first()
            entry_id = entry.id
            for key, value in record.items():
                if key not in ignore_properties:
                    method, category, indicator = key.split(":")
                    indicator = session.query(Indicator).filter(Indicator.method == method,
                                                                Indicator.category == category,
                                                                Indicator.indicator == indicator).first()
                    indicator_id = indicator.id
                    if value != "":
                        impact_object = Impact(entry_id=entry_id, indicator_id=indicator_id,
                                               coefficient=float(value))
                        impacts.append(impact_object)

    session.add_all(impacts)
    session.commit()
    await asyncio.sleep(3)


def datapreparation():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(geography_data())
    loop.run_until_complete(entries_data())
    loop.run_until_complete(indicator_data())
    loop.run_until_complete(impact_data())
    loop.close()


if __name__ == "__main__":
    datapreparation()
