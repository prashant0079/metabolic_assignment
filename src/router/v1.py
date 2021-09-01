from fastapi import HTTPException, APIRouter
from fastapi_sqlalchemy import db
from starlette.status import HTTP_404_NOT_FOUND
from typing import List
from src.models.entry import Entry
from src.models.geography import Geography
from src.models.impact import Impact
from src.models.indicator import Indicator
from src.schema.models import IndicatorSchema, EntrySchema, \
    EntrySchemaExtended, ImpactSchemaExtended
from src.const.api_const import *

api_v1 = APIRouter()


@api_v1.get("/indicator",
            response_model=List[IndicatorSchema],
            summary=API_INDICATORS_SUMMARY,
            description=API_INDICATORS_DESCRIPTION,
            tags=[API_INDICATOR_TAG])
def indicators():
    result = db.session.query(Indicator).all()
    if result is None:
        raise HTTPException(HTTP_404_NOT_FOUND)

    return result


@api_v1.get("/indicator/{id}",
            response_model=IndicatorSchema,
            summary=API_INDICATOR_SUMMARY,
            description=API_INDICATOR_DESCRIPTION,
            tags=[API_INDICATOR_TAG])
def indicator_by_id(id: int):
    result = db.session.query(Indicator).filter(Indicator.id == id).first()
    if result is None:
        raise HTTPException(HTTP_404_NOT_FOUND)

    result_schema = IndicatorSchema.from_orm(result)
    return result_schema


@api_v1.get("/entry",
            response_model=List[EntrySchema],
            summary=API_ENTRIES_SUMMARY,
            description=API_ENTRIES_DESCRIPTION,
            tags=[API_ENTRY_TAG])
def entries():
    result = db.session.query(Entry).all()
    if result is None:
        raise HTTPException(HTTP_404_NOT_FOUND)

    return result


@api_v1.get("/entry/{id}",
            response_model=EntrySchemaExtended,
            summary=API_ENTRY_SUMMARY,
            description=API_ENTRY_DESCRIPTION,
            tags=[API_ENTRY_TAG])
def entry_by_id(id: int):
    result = db.session.query(Entry).filter(Entry.id == id).first()
    if result is None:
        raise HTTPException(HTTP_404_NOT_FOUND)

    result_obj = result
    result_obj.geography = db.session.query(Geography) \
        .filter(Geography.id == result.geography_id).first().__dict__
    result_obj.impact = result.impact
    return result_obj


@api_v1.get("/impact",
            response_model=ImpactSchemaExtended,
            summary=API_IMPACT_SUMMARY,
            description=API_IMPACT_DESCRIPTION,
            tags=[API_IMPACT_TAG])
def impact(entry_id: int, indicator_id: int):
    try:
        result = db.session.query(Impact).filter(Impact.indicator_id == indicator_id,
                                                 Impact.entry_id == entry_id).first()

        indicator = db.session.query(Indicator).filter(Indicator.id == indicator_id).first()

        entry = db.session.query(Entry).filter(Entry.id == entry_id).first()
        result_obj = {
            "id": result.id,
            "coefficient": result.coefficient,
            "entry": entry.__dict__,
            "indicator": indicator.__dict__
        }
        return result_obj

    except Exception as e:
        print(e)
        raise HTTPException(HTTP_404_NOT_FOUND)
