from flask import Flask, request, jsonify, logging
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api, fields, Resource
from http import HTTPStatus
from flask_cors import cross_origin

load_dotenv()

# PostgreSQL Database credentials loaded from the .env file
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

app = Flask(__name__)


# CORS implemented so that we don't get errors when trying to access the server from a different server location
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

# Swagger API and Namespace Starts
api = Api(
    app,
    version='1.0',
    title='Amarnath Assessment Swagger Documentation',
    description='This backend is build with flask'
)

ns = api.namespace("teams", description="Team operations")
api.add_namespace(ns)

# Swagger API and Namespace Starts


# Database  Start
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + \
    DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@localhost/' + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database End


# Database Table Start
class TeamModel(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String())
    role_name = db.Column(db.String())

    def __init__(self, team_name, role_name):
        self.team_name = team_name
        self.role_name = role_name

    def __repr__(self):
        return f"<Team {self.team_name}>"

# Database Table End


# API Models Starts
team_model = api.model('Team', {
    'team_name': fields.String(required=True),
    'role_name': fields.String(required=True),
})

team_create_success_model = api.model("TeamCreateSuccess", {
    "status": fields.String,
    "team": fields.Nested(team_model)
})

role_search_success_model = api.model("RoleSearchSuccess", {
    "status": fields.String,
    "team": fields.String
})

role_search_error_model = api.model("RoleSearchError", {
    "status": fields.String,
    "message": fields.String
})

# API Models End


# Route Starts
@ns.route('/')
class TeamCreate(Resource):
    @api.expect(team_model, validate=True)
    @api.response(200, 'Success', team_create_success_model)
    def post(self):
        data = request.get_json()
        new_team = TeamModel(
            team_name=data['team_name'], role_name=data['role_name'])
        db.session.add(new_team)
        db.session.commit()
        return {
            "status": "success",
            "team": {
                "team_name": new_team.team_name,
                "role": new_team.role_name
            }
        }, 200


@ns.route('/<string:team_name>', methods=['GET'])
class TeamRead(Resource):
    @api.response(200, 'Success', role_search_success_model)
    @api.response(404, 'Error', role_search_error_model)
    def get(self, team_name):
        team = TeamModel.query.filter_by(team_name=team_name).first()
        if team is None:
            return {"status": "error",  "message": "Team not found"}, 404
        else:
            return {"status": "success",  "role_name": team.role_name}, 200

# Route End


if __name__ == '__main__':
    app.run(debug=True)
