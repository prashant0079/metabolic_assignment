from src.database import Session
from src.models.entry import Entry
from src.models.geography import Geography
from src.models.impact import Impact
from src.models.indicator import Indicator


class PrepareTables:
    """A class containing all the methods to add valid data
     to the tables in the database. This class supports context manager
     and closes session at the exit of the context

     Attributes
     ----------
        session: It holds the session object of type Session()(SessionMaker) from SQLAlchemy library
                 Basically a connection to the db.
        data: json object holding the dataset.
    """
    def __init__(self, data):
        self.session = Session()
        self.data = data

    def __enter__(self):
        return self

    def geography(self):
        """Fills Geography data"""
        geography_nl = Geography(country_id="NL", short_name="NLD", name="The Netherlands")
        self.session.add(geography_nl)
        print("Adding Geography data")
        self.session.commit()

    def entry(self):
        """Fills Entry data"""
        entries = []
        for record in self.data:
            if record["Ecoinvent process OR other names"] != "":
                product_name = record["Ecoinvent process OR other names"].split(", [NL]")[0]
                unit = record["Unit"]
                # only one geography i.e. The Netherlands
                geography_id = 1
                # creating valid entry record
                entry_object = Entry(product_name=product_name, unit=unit, geography_id=geography_id)
                entries.append(entry_object)

        self.session.add_all(entries)
        print("Adding Entries data")
        self.session.commit()

    def indicator(self):
        """Fills indicator data"""
        indicators = []
        ignore_properties = ["Data source", "Ecoinvent process OR other names", "Unit", "Reference quantity", ""]
        for key, value in self.data[0].items():
            if key not in ignore_properties:
                method, category, indicator = key.split(":")
                # creating indicator record
                indicator_object = Indicator(method=method, category=category, indicator=indicator, unit=value)
                indicators.append(indicator_object)

        self.session.add_all(indicators)
        print("Adding Indicator data")
        self.session.commit()

    def impact(self):
        """Fills impact data"""
        impacts = []
        ignore_properties = ["Data source", "Ecoinvent process OR other names",
                             "Unit", "Reference quantity", ""]
        for record in self.data:
            if record["Ecoinvent process OR other names"] != "":
                product_name = record["Ecoinvent process OR other names"].split(", [NL]")[0]
                # querying valid entry with the product name
                entry = self.session.query(Entry).filter(Entry.product_name == product_name).first()
                entry_id = entry.id
                for key, value in record.items():
                    if key not in ignore_properties:
                        method, category, indicator = key.split(":")
                        # querying valid indicator
                        indicator = self.session.query(Indicator).filter(Indicator.method == method,
                                                                         Indicator.category == category,
                                                                         Indicator.indicator == indicator).first()
                        indicator_id = indicator.id
                        if value != "":
                            # Creating a valid impact record
                            impact_object = Impact(entry_id=entry_id, indicator_id=indicator_id,
                                                   coefficient=float(value))
                            impacts.append(impact_object)

        self.session.add_all(impacts)
        print("Adding Impact data")
        self.session.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit method"""
        # closing session
        self.session.close()
