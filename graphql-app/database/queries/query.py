import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from database.models import db_session
from database.schema import Employee, Department, EmployeeInformation, Project, EmployeeProjectMapping, DepartmentModel, EmployeeModel
from database.mutations.mutation import Mutation

class DepartmentEmployee(graphene.ObjectType):
    department_name = graphene.String()
    employees = graphene.List(Employee)

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(Employee.connection)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)
    all_employee_informations = SQLAlchemyConnectionField(EmployeeInformation.connection, sort=None)
    all_projects = SQLAlchemyConnectionField(Project.connection, sort=None)
    all_employee_project_mapping = SQLAlchemyConnectionField(EmployeeProjectMapping.connection, sort=None)

    #filter query
    find_department = graphene.List(Department, name = graphene.String())
    def resolve_find_department(self, info, name):
        department = Department.get_query(info)\
                                .filter(DepartmentModel.name == name)
        return department
    
    find_employee = graphene.List(Employee, name = graphene.String())
    def resolve_find_employee(self, info, name):
        like_query = '%{0}%'.format(name)
        employee = (Employee.get_query(info)
                    .filter(EmployeeModel.name.ilike(like_query)))

        return employee       

schema = graphene.Schema(query=Query, mutation=Mutation)