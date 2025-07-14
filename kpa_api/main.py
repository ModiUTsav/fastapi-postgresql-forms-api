from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from typing import Optional, List
from datetime import date

from . import models, schemas, crud
from .database import SessionLocal, engine, get_db

# Load environment variables from .env file
load_dotenv()

# Create database tables if they don't exist
# This will create the tables defined in models.py if they don't already exist in the DB.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPA Form Data API Assignment",
    description="Backend Assignment: Implementation of Bogie Checksheet (POST) and Wheel Specifications (GET) APIs.",
    version="1.0.0",
)

# --- Placeholder Login API ---
# This API is included as per the assignment's context but is not directly used
# for authentication of the other two APIs in this simplified setup.
# In a real application, you would integrate proper authentication (e.g., OAuth2 with JWT)
# to secure your endpoints.
@app.post("/login", response_model=dict, summary="User Login (Placeholder)")
async def login(phone_number: str, password: str):
    """
    Simulates a user login.
    For this assignment, it accepts hardcoded credentials from the .env file.
    """
    expected_phone = os.getenv("LOGIN_PHONE_NUMBER")
    expected_password = os.getenv("LOGIN_PASSWORD")

    if phone_number == expected_phone and password == expected_password:
        return {"message": "Login successful", "token": "dummy_jwt_token_for_kpa"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# --- API 1: POST /api/forms/bogie-checksheet ---
@app.post(
    "/api/forms/bogie-checksheet",
    response_model=schemas.BogieChecksheetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Bogie Checksheet Entry",
    description="Submits a new bogie checksheet form with various details including bogie, BMBC, and general checksheet information.",
)
def create_bogie_checksheet_endpoint(
    bogie_checksheet_data: schemas.BogieChecksheetCreate,
    db: Session = Depends(get_db)
):
    """
    **Creates a new Bogie Checksheet record.**

    This endpoint accepts a JSON payload containing details about a bogie checksheet,
    including `formNumber`, `inspectionBy`, `inspectionDate`, and nested objects
    for `bmbcChecksheet`, `bogieChecksheet`, and `bogieDetails`.

    **Request Body Example:**
    ```json
    {
      "bmbcChecksheet": {
        "adjustingTube": "DAMAGED",
        "cylinderBody": "WORN OUT",
        "pistonTrunnion": "GOOD",
        "plungerSpring": "GOOD"
      },
      "bogieChecksheet": {
        "axleGuide": "Worn",
        "bogieFrameCondition": "Good",
        "bolster": "Good",
        "bolsterSuspensionBracket": "Cracked",
        "lowerSpringSeat": "Good"
      },
      "bogieDetails": {
        "bogieNo": "BG1234",
        "dateOfIOH": "2025-07-01",
        "deficitComponents": "None",
        "incomingDivAndDate": "NR / 2025-06-25",
        "makerYearBuilt": "RDSO/2018"
      },
      "formNumber": "BOGIE-2025-001",
      "inspectionBy": "user_id_456",
      "inspectionDate": "2025-07-03"
    }
    ```

    **Responses:**
    - `201 Created`: Successfully created the bogie checksheet.
    - `400 Bad Request`: If the input data is invalid (e.g., duplicate formNumber).
    """
    # Check for duplicate formNumber before creating
    existing_form = db.query(models.BogieChecksheet).filter(
        models.BogieChecksheet.form_number == bogie_checksheet_data.formNumber
    ).first()
    if existing_form:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Form with formNumber '{bogie_checksheet_data.formNumber}' already exists."
        )

    db_bogie_checksheet = crud.create_bogie_checksheet(db=db, bogie_checksheet=bogie_checksheet_data)

    return schemas.BogieChecksheetResponse(
        data=schemas.BogieChecksheetResponseData(
            formNumber=db_bogie_checksheet.form_number,
            inspectionBy=db_bogie_checksheet.inspection_by,
            inspectionDate=db_bogie_checksheet.inspection_date,
            status="Saved" # As per Swagger example
        ),
        # --- FIX: Explicitly pass message and success fields ---
        message="Bogie checksheet submitted successfully.",
        success=True
    )

# --- API 2: GET /api/forms/wheel-specifications ---
@app.get(
    "/api/forms/wheel-specifications",
    response_model=schemas.WheelSpecificationListResponse,
    summary="Retrieve Wheel Specifications (with filters)",
    description="Fetches a list of wheel specification forms, with optional filtering by form number, submitter, or submission date.",
)
def get_wheel_specifications_endpoint(
    formNumber: Optional[str] = Query(None, description="Filter by unique form number"),
    submittedBy: Optional[str] = Query(None, description="Filter by the ID of the user who submitted the form"),
    submittedDate: Optional[date] = Query(None, description="Filter by the submission date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    **Retrieves a list of Wheel Specification records.**

    This endpoint allows you to fetch wheel specification forms.
    You can filter the results using the following optional query parameters:
    - `formNumber`: A specific form number to search for.
    - `submittedBy`: The ID of the user who submitted the form.
    - `submittedDate`: The date on which the form was submitted (format: YYYY-MM-DD).

    **Example Response:**
    ```json
    {
      "data": [
        {
          "fields": {
            "condemningDia": "825 (800-900)",
            "lastShopIssueSize": "837 (800-900)",
            "treadDiameterNew": "915 (900-1000)",
            "wheelGauge": "1600 (+2,-1)",
            "axleBoxHousingBoreDia": "280 (+0.030/+0.052)",
            "bearingSeatDiameter": "130.043 TO 130.068",
            "intermediateWWP": "20 TO 28",
            "rollerBearingBoreDia": "130 (+0.0/-0.025)",
            "rollerBearingOuterDia": "280 (+0.0/-0.035)",
            "rollerBearingWidth": "93 (+0/-0.250)",
            "variationSameAxle": "0.5",
            "variationSameBogie": "5",
            "variationSameCoach": "13",
            "wheelDiscWidth": "127 (+4/-0)",
            "wheelProfile": "29.4 Flange Thickness"
          },
          "formNumber": "WHEEL-2025-001",
          "submittedBy": "user_id_123",
          "submittedDate": "2025-07-03"
        }
      ],
      "message": "Filtered wheel specification forms fetched successfully.",
      "success": true
    }
    ```

    **Responses:**
    - `200 OK`: Returns a list of matching wheel specification forms.
    """
    wheel_specs = crud.get_wheel_specifications(
        db=db,
        form_number=formNumber,
        submitted_by=submittedBy,
        submitted_date=submittedDate
    )

    # Convert SQLAlchemy models to Pydantic response models
    response_data = [
        schemas.WheelSpecificationResponseDataItem(
            formNumber=spec.form_number,
            submittedBy=spec.submitted_by,
            submittedDate=spec.submitted_date,
            fields=schemas.WheelSpecificationFields(**spec.fields) if spec.fields else schemas.WheelSpecificationFields()
        ) for spec in wheel_specs
    ]

    # If no data is found, return an empty list in data and a message
    message = "Filtered wheel specification forms fetched successfully."
    if not response_data:
        message = "No wheel specification forms found matching the criteria."

    return schemas.WheelSpecificationListResponse(
        data=response_data,
        message=message,
        success=True
    )

# --- Endpoint to populate dummy data (Optional, for testing convenience) ---
@app.post("/populate-dummy-wheel-data", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def populate_dummy_wheel_data(db: Session = Depends(get_db)):
    """
    Helper endpoint to populate some dummy wheel specification data for testing.
    This endpoint is not part of the core assignment APIs and is excluded from Swagger UI.
    """
    dummy_data = [
        schemas.WheelSpecificationCreate(
            formNumber="WHEEL-2025-001",
            submittedBy="user_id_123",
            submittedDate=date(2025, 7, 3),
            fields=schemas.WheelSpecificationFields(
                condemningDia="825 (800-900)",
                lastShopIssueSize="837 (800-900)",
                treadDiameterNew="915 (900-1000)",
                wheelGauge="1600 (+2,-1)",
                axleBoxHousingBoreDia="280 (+0.030/+0.052)",
                bearingSeatDiameter="130.043 TO 130.068",
                intermediateWWP="20 TO 28",
                rollerBearingBoreDia="130 (+0.0/-0.025)",
                rollerBearingOuterDia="280 (+0.0/-0.035)",
                rollerBearingWidth="93 (+0/-0.250)",
                variationSameAxle="0.5",
                variationSameBogie="5",
                variationSameCoach="13",
                wheelDiscWidth="127 (+4/-0)",
                wheelProfile="29.4 Flange Thickness"
            )
        ),
        schemas.WheelSpecificationCreate(
            formNumber="WHEEL-2025-002",
            submittedBy="user_id_456",
            submittedDate=date(2025, 7, 4),
            fields=schemas.WheelSpecificationFields(
                condemningDia="830 (800-900)",
                lastShopIssueSize="840 (800-900)",
                treadDiameterNew="920 (900-1000)",
                wheelGauge="1601 (+2,-1)"
            )
        )
    ]

    for item in dummy_data:
        # Check if already exists to prevent duplicates on repeated calls
        existing = db.query(models.WheelSpecification).filter(
            models.WheelSpecification.form_number == item.formNumber
        ).first()
        if not existing:
            crud.create_dummy_wheel_specification(db, item)

    return {"message": "Dummy wheel specification data populated successfully."}
