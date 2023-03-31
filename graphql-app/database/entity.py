import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.models import Department as DepartmentModel\
    , Employee as EmployeeModel\
    , EmployeeInformation as EmployeeInformationModel\
    , Project as ProjectModel\
    , EmployeeProjectMapping as EmployeeProjectMappingModel

# to connect between GraphQL and SQLAlchemy

class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )

class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )

    employees = graphene.Field(graphene.List(Employee), name = graphene.String())
    def resolve_employees(self, info, name):
        return Employee.get_query(info)\
                        .filter(EmployeeModel.department == self)\
                        .filter(EmployeeModel.name == name)

class EmployeeInformation(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeInformationModel
        interfaces = (relay.Node, )

class Project(SQLAlchemyObjectType):
    class Meta:
        model = ProjectModel
        interfaces = (relay.Node, )

class EmployeeProjectMapping(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeProjectMappingModel
        interfaces = (relay.Node, )

