import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from database.models import db_session
from database.entity import Employee, Department, EmployeeInformation, Project, EmployeeProjectMapping, DepartmentModel, EmployeeModel
from database.mutations.mutation import Mutation
from database.queries.employee_queries import GetEmployees

class DepartmentEmployee(graphene.ObjectType):
    department_name = graphene.String()
    employees = graphene.List(Employee)

class Query(graphene.ObjectType):
    departments = graphene.List(Department, name = graphene.String(required=False))
    def resolve_departments(self, info, name=''):
        query = Department.get_query(info)

        if name != '':
            query = query.filter(DepartmentModel.name == name)

        return query

    employees = graphene.List(Employee, name=graphene.String(required=False))
    def resolve_employees(self, info, name=''):
        query = Employee.get_query(info)

        if name != '':
            like_query = '%{0}%'.format(name)
            query = query.filter(EmployeeModel.name.ilike(like_query))

        return query
    
    employee_informations = graphene.List(EmployeeInformation)
    def resolve_employee_informations(self, info):
        query = EmployeeInformation.get_query(info)
        return query

    projects = graphene.List(Project)
    def resolve_projects(self, info):
        query = Project.get_query(info)
        return query
    
    employee_project_mapping = graphene.List(EmployeeProjectMapping)
    def resolve_employee_project_mapping(self, info):
        query = EmployeeProjectMapping.get_query(info)
        return query