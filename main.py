import secrets
from fastapi import FastAPI, HTTPException, Header, Request

app = FastAPI()

employees = {
    "EMP1001": {
        "employeeId": "EMP1001",
        "name": "Rahul Sharma",
        "department": "IT"
    }
}



@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):
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
def create_employee(employee: Employee):
    
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