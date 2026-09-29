import os
import base64
import secrets
from fastapi import FastAPI, HTTPException, Header, Request


OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")

ACCESS_TOKEN = os.getenv("HR_API_TOKEN")


app = FastAPI()

@app.post("/oauth/token")
async def oauth_token(request: Request):

    form = await request.form()

    grant_type = form.get("grant_type")

    # Read client credentials from HTTP Basic Auth
    authorization = request.headers.get("Authorization")

    client_id = None
    client_secret = None

    if authorization and authorization.startswith("Basic "):
        encoded = authorization[6:]

        try:
            decoded = base64.b64decode(encoded).decode("utf-8")
            client_id, client_secret = decoded.split(":", 1)
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Invalid client authentication"
            )

    # Fallback: credentials in request body
    if not client_id:
        client_id = form.get("client_id")

    if not client_secret:
        client_secret = form.get("client_secret")

    if grant_type != "client_credentials":
        raise HTTPException(
            status_code=400,
            detail="Unsupported grant_type"
        )

    if (
        client_id != OAUTH_CLIENT_ID
        or client_secret != OAUTH_CLIENT_SECRET
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid client credentials"
        )

    return {
        "access_token": ACCESS_TOKEN,
        "token_type": "Bearer",
        "expires_in": 3600
    }


employees = {
    "EMP1001": {
        "employeeId": "EMP1001",
        "name": "Rahul Sharma",
        "department": "IT"
    }
}


@app.get("/employees/{employee_id}")
def get_employee(
    employee_id: str,
    authorization: str = Header(None)
    ):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if employee_id in employees:
        return {
            "exists": True,
            "employeeId": employee_id,
            "message": "Employee already exists"
        }

    return {
        "exists": False,
        "employeeId": employee_id,
        "message": "Employee does not exist"
    }

from pydantic import BaseModel


class Employee(BaseModel):
    employeeId: str
    firstName: str
    lastName: str
    email: str
    department: str
    designation: str
    joiningDate: str
    salary: float



@app.post("/employees", status_code=201)
def create_employee(
    employee: Employee,
    authorization: str = Header(None)
    ):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    
    if employee.employeeId in employees:

        raise HTTPException(
            status_code=409,
            detail={
                "success": False,
                "message": "Employee already exists",
                "employeeId": employee.employeeId
            }
        )

    employees[employee.employeeId] = {
        "employeeId": employee.employeeId,
        "name": f"{employee.firstName} {employee.lastName}",
        "department": employee.department
    }

    return {
        "success": True,
        "message": "Employee created successfully",
        "employeeId": employee.employeeId,
        "status": "CREATED"
    }