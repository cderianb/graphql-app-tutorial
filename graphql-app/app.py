from flask import Flask
from flask_cors import CORS, cross_origin
from flask_graphql import GraphQLView
from database.models import db_session
from database.schema import schema
from flask import request

app = Flask(__name__)
CORS(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface,
    )
)

@app.before_request
def validate_request():
    scm_username = request.headers.get('SCM-Username')
    scm_organization = request.headers.get('SCM-Organization')

    # hit using postman, uncomment below
    # if scm_username is None or scm_organization is None:
    #     return "Error"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=False)
    