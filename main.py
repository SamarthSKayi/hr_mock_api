from fastapi import FastAPI


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