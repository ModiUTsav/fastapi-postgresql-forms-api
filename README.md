Sarva Form Data API Assignment
This project implements two API endpoints from the provided Sarva Form Data Swagger/OpenAPI specification using FastAPI and PostgreSQL.

Objective
The objective of this assignment was to develop two fully functional backend APIs that adhere to specified request/response structures, demonstrating backend development skills with Python FastAPI and PostgreSQL.

#ScreenShot
<img width="1919" height="1136" alt="Image" src="https://github.com/user-attachments/assets/f3e661f5-c811-4442-9272-b2224c45f6af" />

<img width="1917" height="1032" alt="Image" src="https://github.com/user-attachments/assets/ff73a0bc-66d2-494c-998a-2830ddc127a7" />

<img width="1916" height="1142" alt="Image" src="https://github.com/user-attachments/assets/fca7c695-3281-4050-ad78-4227fa0aab1f" />

Implemented APIs
Based on the provided Swagger UI, the following two APIs have been implemented:

POST /api/forms/bogie-checksheet

Description: This endpoint allows for the submission of a new bogie checksheet form. It expects a JSON payload containing detailed information about the bogie, including formNumber, inspectionBy, inspectionDate, and nested objects for bmbcChecksheet, bogieChecksheet, and bogieDetails. The data is validated and stored in a PostgreSQL database.

Functionality: Creates a new record in the bogie_checksheets table. Includes basic validation to prevent duplicate formNumber entries.

Request Body Example:
```

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
Successful Response (201 Created) Example:
```
{
  "data": {
    "formNumber": "BOGIE-2025-001",
    "inspectionBy": "user_id_456",
    "inspectionDate": "2025-07-03",
    "status": "Saved"
  },
  "message": "Bogie checksheet submitted successfully.",
  "success": true
}
```

GET /api/forms/wheel-specifications

Description: This endpoint retrieves a list of wheel specification forms. It supports optional filtering by formNumber, submittedBy, and submittedDate through query parameters.

Functionality: Queries the wheel_specifications table, applying filters if provided, and returns a list of matching records.

Query Parameters:

formNumber (string, optional): Filter by a specific form number.

submittedBy (string, optional): Filter by the ID of the user who submitted the form.

submittedDate (string, optional): Filter by the submission date (format: YYYY-MM-DD).

Successful Response (200 OK) Example:
```
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
Response (200 OK) Example when no data is found:
```
{
  "data": [],
  "message": "No wheel specification forms found matching the criteria.",
  "success": true
}
```

Tech Stack Used
Backend Framework: FastAPI

Programming Language: Python 3.9+

Web Server: Uvicorn

Database: PostgreSQL (running in Docker)

ORM (Object-Relational Mapper): SQLAlchemy 2.0

Environment Variables: python-dotenv

Data Validation: Pydantic (integrated with FastAPI)

Setup Instructions
Follow these steps to set up and run the project locally:

Prerequisites
Python 3.9+ installed on your system.

Docker Desktop installed and running (for PostgreSQL).

pip (Python package installer).

Postman (for testing the APIs).

1. Project Structure
Ensure your project has the following structure:
```
your_project_root/ (e.g., E:\Sarva sividhan pv.ltd\)
├── .env
├── requirements.txt
├── venv/
└── sarva_api/  
    ├── __init__.py  <-- IMPORTANT: This empty file makes 'sarva_api' a Python package
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    └── crud.py
```
If you don't have the sarva_api folder and __init__.py file, create them.

Place main.py, database.py, models.py, schemas.py, crud.py inside the sarva_api folder.

Place .env and requirements.txt in the your_project_root directory.

2. Create a Python Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.
```
python -m venv venv
```
3. Activate the Virtual Environment
On macOS/Linux:
```
source venv/bin/activate
```
On Windows:
```
.\venv\Scripts\activate
```
(You should see (venv) at the start of your terminal prompt).

4. Install Dependencies
Once the virtual environment is active, install the required Python packages:
```
pip install -r requirements.txt
```
5. Set Up PostgreSQL Database with Docker
Pull the PostgreSQL Docker Image:
```
docker pull postgres
```
Run a PostgreSQL Container:
```
docker run --name sarva-postgres-db -e POSTGRES_PASSWORD=your_strong_db_password -p 5432:5432 -d postgres
```
IMPORTANT: Replace your_strong_db_password with a secure password. If your password contains special characters like @, you might need to URL-encode it (e.g., @ becomes %40). For simplicity, consider a password without special characters for this assignment.

Verify Container is Running:
```
docker ps
```
You should see sarva-postgres-db listed.

Connect to the Container and Create Your Database:
```
docker exec -it sarva-postgres-db psql -U postgres
```
Enter your your_strong_db_password when prompted.
At the postgres=# prompt, create the database:

CREATE DATABASE sarva_form_db;
```
\q
```
(You can verify it exists with \l before quitting psql).

6. Configure Environment Variables
Create or update the .env file in your project's root directory (e.g., E:\Sarva sividhan pv.ltd\.env).

# PostgreSQL Database URL
# Format: postgresql://user:password@host:port/database_name
# Example: DATABASE_URL="postgresql://postgres:MyStrongPassword123@localhost:5432/sarva_form_db"
```
DATABASE_URL="postgresql://postgres:your_strong_db_password@localhost:5432/sarva_form_db"
```
# Dummy Login Credentials (as provided in the assignment)
```
LOGIN_PHONE_NUMBER=7760873976
LOGIN_PASSWORD=to_share@123
```
Ensure your_strong_db_password matches the one you used in the docker run command.

7. Run the FastAPI Application
From your project's root directory (e.g., E:\Sarva sividhan pv.ltd), with your virtual environment activated, run the FastAPI application:

uvicorn sarva_api.main:app --reload

You should see output indicating that the server is running, typically at ```http://127.0.0.1:8000```. SQLAlchemy will automatically create your database tables (bogie_checksheets and wheel_specifications) on startup if they don't exist.

8. Access API Documentation (Swagger UI)
Once the server is running, open your web browser and go to:
```
http://127.0.0.1:8000/docs
```
Here you can interact with and test your implemented API endpoints.

9. Populate Dummy Data (Optional)
To easily test the GET /api/forms/wheel-specifications endpoint, you can populate some dummy data by making a POST request to:
```
http://127.0.0.1:8000/populate-dummy-wheel-data
```
Send an empty POST request to this URL using Postman or Swagger UI's "Try it out" feature.

10. Test with Postman
Import the original Postman Collection: Import the Sarva_form data.postman_collection.json file into your Postman application.
```
Update Base URL: Change the base URL for the requests in the collection from https://railops-uat-api.biputri.com to your local server address: http://127.0.0.1:8000. This can often be done by setting a collection variable.
```
Test Endpoints:

POST /api/forms/bogie-checksheet: Use the example request body from the "Implemented APIs" section above. Remember to change the formNumber for each new submission to avoid 400 Bad Request errors (due to the unique constraint).

GET /api/forms/wheel-specifications: Test with and without query parameters (formNumber, submittedBy, submittedDate).

POST /login: Test the placeholder login endpoint.

Export Updated Collection: After successfully testing your APIs, export the modified Postman collection. This will be part of your submission.

Limitations and Assumptions
Authentication: The /login endpoint is a placeholder and does not implement a full authentication system (e.g., JWT token validation for subsequent API calls). The two implemented form APIs do not require authentication for this assignment's scope.

Error Handling: Basic error handling is in place (e.g., 404 for not found, 400 for duplicate formNumber), but a more comprehensive error handling strategy would be implemented in a production application.

Database Migrations: Database schema changes are handled by models.Base.metadata.create_all(bind=engine) which creates tables if they don't exist. For production, a dedicated migration tool like Alembic would be used.

Complex Data Types: Nested JSON objects are stored directly as JSONB columns in PostgreSQL for simplicity.

Filtering: The GET endpoint for wheel-specifications implements basic equality filtering. More advanced filtering could be added.

Dummy Data Population: A helper endpoint /populate-dummy-wheel-data is provided for convenience during testing. This should be removed or secured in a production environment.

Contact:

For any questions or clarifications, please contact modiutsav2003@gmail.com
