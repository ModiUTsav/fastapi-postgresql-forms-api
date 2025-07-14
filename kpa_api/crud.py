from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import Optional, List
from datetime import date

# --- CRUD Operations for Bogie Checksheet ---

def create_bogie_checksheet(db: Session, bogie_checksheet: schemas.BogieChecksheetCreate):
    """
    Creates a new bogie checksheet record in the database.
    Ensures nested Pydantic models are serialized to JSON-compatible dictionaries
    before storing in JSONB columns.
    """
    # Use model_dump(mode='json') to serialize nested Pydantic models,
    # which correctly handles date objects by converting them to ISO 8601 strings.
    db_bogie_checksheet = models.BogieChecksheet(
        form_number=bogie_checksheet.formNumber,
        inspection_by=bogie_checksheet.inspectionBy,
        inspection_date=bogie_checksheet.inspectionDate,
        bmbc_checksheet=bogie_checksheet.bmbcChecksheet.model_dump(mode='json') if bogie_checksheet.bmbcChecksheet else None,
        bogie_checksheet_details=bogie_checksheet.bogieChecksheet.model_dump(mode='json') if bogie_checksheet.bogieChecksheet else None,
        bogie_details=bogie_checksheet.bogieDetails.model_dump(mode='json') if bogie_checksheet.bogieDetails else None,
    )
    db.add(db_bogie_checksheet)
    db.commit()
    db.refresh(db_bogie_checksheet)
    return db_bogie_checksheet

# --- CRUD Operations for Wheel Specifications ---

def get_wheel_specifications(
    db: Session,
    form_number: Optional[str] = None,
    submitted_by: Optional[str] = None,
    submitted_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.WheelSpecification]:
    """
    Retrieves wheel specification records from the database with optional filters.
    """
    query = db.query(models.WheelSpecification)

    if form_number:
        query = query.filter(models.WheelSpecification.form_number == form_number)
    if submitted_by:
        query = query.filter(models.WheelSpecification.submitted_by == submitted_by)
    if submitted_date:
        query = query.filter(models.WheelSpecification.submitted_date == submitted_date)

    return query.offset(skip).limit(limit).all()

# For demonstration, let's add a function to populate some dummy data for wheel specifications
def create_dummy_wheel_specification(db: Session, item: schemas.WheelSpecificationCreate):
    """
    Creates a dummy wheel specification record. Used for populating initial data.
    """
    db_item = models.WheelSpecification(
        form_number=item.formNumber,
        submitted_by=item.submittedBy,
        submitted_date=item.submittedDate,
        # Use model_dump(mode='json') here as well for consistency and correct date serialization
        fields=item.fields.model_dump(mode='json') if item.fields else None,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
