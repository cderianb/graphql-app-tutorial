import graphene
from database.models import Employee, db_session, Department

class CreateEmployee(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        department_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, _, info, name, department_id):
        department = Department.query.filter_by(id=department_id).first()
        if department is None:
            return CreateEmployee(success=False, message="department_id is not valid")
        new_employee = Employee(
            name = name,
            department_id = department_id
        )
        db_session.add(new_employee) # store it in flask memory
        db_session.commit() # store it to database
        return CreateEmployee(success=True, message="success creating employee")

class UpdateEmployee(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        employee_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, _, info, name, employee_id):
        query = db_session.query(Employee)\
                    .filter(Employee.id==employee_id)

        employee = query.first()
        
        if employee is None:
            return UpdateEmployee(success=False, message="employee_id is not valid")
        
        query.update({
                        'name': name
                    })

        db_session.commit() # store it to database
        return UpdateEmployee(success=True, message="success creating employee")
    
class DeleteEmployee(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        employee_ids = graphene.List(graphene.Int, required=True)

    @classmethod
    def mutate(cls, _, info, employee_ids):      
        query = db_session.query(Employee)\
                    .filter(Employee.id.in_(employee_ids))
        employee = query.all()
        print(employee)
        if len(employee) == 0:
            return DeleteEmployee(success=False, message="employee_id is not valid")
        
        query.delete()

        db_session.commit() # store it to database
        return DeleteEmployee(success=True, message="success creating employee")