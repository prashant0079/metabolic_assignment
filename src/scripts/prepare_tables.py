import asyncio

from src.database import Session
from src.models.entry import Entry
from src.models.geography import Geography
from src.models.impact import Impact
from src.models.indicator import Indicator


class PrepareTables:
    def __init__(self, data):
        self.session = Session()
        self.data = data

    def __enter__(self):
        return self

    async def geography(self):
        geography_nl = Geography(country_id="NL", short_name="NLD", name="The Netherlands")
        self.session.add(geography_nl)
        print("Adding Geography data")
        self.session.commit()
        await asyncio.sleep(3)

    async def entry(self):
        entries = []
        for record in self.data:
            if record["Ecoinvent process OR other names"] != "":
                product_name = record["Ecoinvent process OR other names"].split(", [NL]")[0]
                unit = record["Unit"]
                geography_id = 1  # only one geography i.e. The Netherlands
                entry_object = Entry(product_name=product_name, unit=unit, geography_id=geography_id)
                entries.append(entry_object)

        self.session.add_all(entries)
        print("Adding Entries data")
        self.session.commit()
        await asyncio.sleep(3)

    async def indicator(self):
        indicators = []
        ignore_properties = ["Data source", "Ecoinvent process OR other names", "Unit", "Reference quantity", ""]
        for key, value in self.data[0].items():
            if key not in ignore_properties:
                method, category, indicator = key.split(":")
                indicator_object = Indicator(method=method, category=category, indicator=indicator, unit=value)
                indicators.append(indicator_object)

        self.session.add_all(indicators)
        print("Adding Indicator data")
        self.session.commit()
        await asyncio.sleep(3)

    async def impact(self):
        impacts = []
        ignore_properties = ["Data source", "Ecoinvent process OR other names",
                             "Unit", "Reference quantity", ""]
        for record in self.data:
            if record["Ecoinvent process OR other names"] != "":
                product_name = record["Ecoinvent process OR other names"].split(", [NL]")[0]
                entry = self.session.query(Entry).filter(Entry.product_name == product_name).first()
                entry_id = entry.id
                for key, value in record.items():
                    if key not in ignore_properties:
                        method, category, indicator = key.split(":")
                        indicator = self.session.query(Indicator).filter(Indicator.method == method,
                                                                         Indicator.category == category,
                                                                         Indicator.indicator == indicator).first()
                        indicator_id = indicator.id
                        if value != "":
                            impact_object = Impact(entry_id=entry_id, indicator_id=indicator_id,
                                                   coefficient=float(value))
                            impacts.append(impact_object)

        self.session.add_all(impacts)
        print("Adding Impact data")
        self.session.commit()
        await asyncio.sleep(3)

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
