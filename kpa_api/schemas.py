from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class BmbcChecksheet(BaseModel):
    adjustingTube: Optional[str] = Field(None,description="DAMAGED")
    cylinderBody: Optional[str] = Field(None, example="WORN OUT")
    pistonTrunnion: Optional[str] = Field(None, example="GOOD")
    plungerSpring: Optional[str] = Field(None, example="GOOD")

class BogieChecksheetDetails(BaseModel):
    
    axleGuide: Optional[str] = Field(None, example="Worn")
    bogieFrameCondition: Optional[str] = Field(None, example="Good")
    bolster: Optional[str] = Field(None, example="Good")
    bolsterSuspensionBracket: Optional[str] = Field(None, example="Cracked")
    lowerSpringSeat: Optional[str] = Field(None, example="Good")


class BogieDetails(BaseModel):
    """Schema for bogieDetails."""
    bogieNo: Optional[str] = Field(None, example="BG1234")
    dateOfIOH: Optional[date] = Field(None, example="2025-07-01") # Changed to date type
    deficitComponents: Optional[str] = Field(None, example="None")
    incomingDivAndDate: Optional[str] = Field(None, example="NR / 2025-06-25")
    makerYearBuilt: Optional[str] = Field(None, example="RDSO/2018")

# --- Request Body Schema for POST /api/forms/bogie-checksheet ---
class BogieChecksheetCreate(BaseModel):
    """Request schema for creating a new Bogie Checksheet."""
    bmbcChecksheet: Optional[BmbcChecksheet] = None
    bogieChecksheet: Optional[BogieChecksheetDetails] = None
    bogieDetails: Optional[BogieDetails] = None
    formNumber: str = Field(..., example="BOGIE-2025-001") # Required field
    inspectionBy: str = Field(..., example="user_id_456") # Required field
    inspectionDate: date = Field(..., example="2025-07-03") # Required field, changed to date type

# --- Response Schemas for POST /api/forms/bogie-checksheet ---
class BogieChecksheetResponseData(BaseModel):
    """Data part of the Bogie Checksheet creation response."""
    formNumber: str = Field(..., example="BOGIE-2025-001")
    inspectionBy: str = Field(..., example="user_id_456")
    inspectionDate: date = Field(..., example="2025-07-03")
    status: str = Field(..., example="Saved")

class BogieChecksheetResponse(BaseModel):
    """Full response schema for Bogie Checksheet creation."""
    data: BogieChecksheetResponseData
    message: str = Field(..., example="Bogie checksheet submitted successfully.")
    success: bool = Field(..., example=True)


    # Get Method api

class WheelSpecificationFields(BaseModel):
    """Schema for fields within Wheel Specifications."""
    condemningDia: Optional[str] = Field(None, example="825 (800-900)")
    lastShopIssueSize: Optional[str] = Field(None, example="837 (800-900)")
    treadDiameterNew: Optional[str] = Field(None, example="915 (900-1000)")
    wheelGauge: Optional[str] = Field(None, example="1600 (+2,-1)")
    axleBoxHousingBoreDia: Optional[str] = Field(None, example="280 (+0.030/+0.052)")
    bearingSeatDiameter: Optional[str] = Field(None, example="130.043 TO 130.068")
    intermediateWWP: Optional[str] = Field(None, example="20 TO 28")
    rollerBearingBoreDia: Optional[str] = Field(None, example="130 (+0.0/-0.025)")
    rollerBearingOuterDia: Optional[str] = Field(None, example="280 (+0.0/-0.035)")
    rollerBearingWidth: Optional[str] = Field(None, example="93 (+0/-0.250)")
    variationSameAxle: Optional[str] = Field(None, example="0.5")
    variationSameBogie: Optional[str] = Field(None, example="5")
    variationSameCoach: Optional[str] = Field(None, example="13")
    wheelDiscWidth: Optional[str] = Field(None, example="127 (+4/-0)")
    wheelProfile: Optional[str] = Field(None, example="29.4 Flange Thickness")


# --- Response Data Item Schema for GET /api/forms/wheel-specifications ---
class WheelSpecificationResponseDataItem(BaseModel):
    """Individual item schema for Wheel Specification response data."""
    fields: WheelSpecificationFields
    formNumber: str = Field(..., example="WHEEL-2025-001")
    submittedBy: str = Field(..., example="user_id_123")
    submittedDate: date = Field(..., example="2025-07-03") # Changed to date type

    class Config:
        # This is crucial for SQLAlchemy models to be compatible with Pydantic
        # It allows Pydantic to read data from ORM objects.
        from_attributes = True


# --- Full Response Schema for GET /api/forms/wheel-specifications ---
class WheelSpecificationListResponse(BaseModel):
    """Full response schema for fetching Wheel Specifications."""
    data: List[WheelSpecificationResponseDataItem]
    message: str = Field(..., example="Filtered wheel specification forms fetched successfully.")
    success: bool = Field(..., example=True)

# --- Request Body Schema for POST /api/forms/wheel-specifications (if you were to implement it) ---
# This is included for completeness based on the swagger, but we are only implementing GET for this path.
class WheelSpecificationCreate(BaseModel):
    """Request schema for creating a new Wheel Specification."""
    fields: WheelSpecificationFields
    formNumber: str = Field(..., example="WHEEL-2025-001")
    submittedBy: str = Field(..., example="user_id_123")
    submittedDate: date = Field(..., example="2025-07-03")

# --- Response Schemas for POST /api/forms/wheel-specifications (if you were to implement it) ---
class WheelSpecificationCreateResponseData(BaseModel):
    """Data part of the Wheel Specification creation response."""
    formNumber: str = Field(..., example="WHEEL-2025-001")
    status: str = Field(..., example="Saved")
    submittedBy: str = Field(..., example="user_id_123")
    submittedDate: date = Field(..., example="2025-07-03")

class WheelSpecificationCreateResponse(BaseModel):
    """Full response schema for Wheel Specification creation."""
    data: WheelSpecificationCreateResponseData
    message: str = Field(..., example="Wheel specification submitted successfully.")
    success: bool = Field(..., example=True)
