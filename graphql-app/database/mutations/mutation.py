import graphene
from database.mutations.employee_mutations import CreateEmployee, UpdateEmployee, DeleteEmployee

class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
    