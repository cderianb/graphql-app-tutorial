import graphene
from database.mutations.mutation import Mutation
from database.queries.query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)