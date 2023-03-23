# to connect and interact to DB
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:postgres@localhost:5431/AtomCorp')
engine.connect()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    employees = relationship('Employee', back_populates="department")

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    resign_on = Column(DateTime)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship(Department, back_populates="employees")
    employee_information = relationship('EmployeeInformation', back_populates='employee')
    employee_project_mappings = relationship('EmployeeProjectMapping', back_populates='employees')

class EmployeeInformation(Base):
    __tablename__ = 'employee_informations'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    address = Column(String)
    birthdate = Column(DateTime)
    is_active = Column(Boolean)
    resign_on = Column(DateTime)
    employee = relationship(Employee, back_populates="employee_information")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(DateTime)
    expected_end_date = Column(DateTime)
    actual_end_date = Column(DateTime)
    employee_project_mappings = relationship('EmployeeProjectMapping', back_populates='projects')

class EmployeeProjectMapping(Base):
    __tablename__ = 'employee_project_mapping'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    employees = relationship(Employee, back_populates='employee_project_mappings')
    projects = relationship(Project, back_populates='employee_project_mappings')



Base.metadata.create_all(engine)