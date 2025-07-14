from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .database import Base

class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheets"

    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String, unique=True, index=True, nullable=False)
    inspection_by = Column(String, nullable=False)
    inspection_date = Column(Date, nullable=False)

    bmbc_checksheet = Column(JSONB)
    bogie_checksheet_details = Column(JSONB)
    bogie_details = Column(JSONB)
    # Add a timestamp for when the record was created in the DB
    created_at = Column(Date, server_default=func.now())

    def __repr__(self):
        return f"<BogieChecksheet(form_number='{self.form_number}', inspection_by='{self.inspection_by}')>"

# --- SQLAlchemy Model for Wheel Specifications ---
class WheelSpecification(Base):
    """SQLAlchemy model for the 'wheel_specifications' table."""
    __tablename__ = "wheel_specifications"

    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String, unique=True, index=True, nullable=False)
    submitted_by = Column(String, nullable=False)
    submitted_date = Column(Date, nullable=False)
    # Store nested JSON objects as JSONB columns
    fields = Column(JSONB)
    # Add a timestamp for when the record was created in the DB
    created_at = Column(Date, server_default=func.now())

    def __repr__(self):
        return f"<WheelSpecification(form_number='{self.form_number}', submitted_by='{self.submitted_by}')>"



