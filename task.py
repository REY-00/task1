import os
from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

# Create the Flask application
app = Flask(__name__)
app.config['DEBUG'] = True

file_path = os.path.abspath(os.getcwd())+"/database.db"


# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:'+file_path
db = SQLAlchemy(app)

app.app_context().push()

# Create data storage in database
class Board(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_creation = db.Column(db.DateTime)
  date_modified = db.Column(db.DateTime)
  status = db.Column(db.String)


class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_creation = db.Column(db.DateTime)
  date_modified = db.Column(db.DateTime)
  status = db.Column(db.Boolean)
  text = db.Column(db.Boolean)
  board = db.Column(db.Integer, db.ForeignKey('board.id'))

db.create_all()

# Logical data abstraction
class BoardSchema(Schema):
  class Meta:
    type_ = 'board'
    self_view = 'board_detail'
    self_view_kwargs = {'id': '<id>'}
    self_view_many = 'board_list'

  id = fields.Integer(as_string=True, dump_only=True)
  date_creation = fields.Time(required=True)
  date_modified = fields.Time()
  status = fields.Str()

class TaskSchema(Schema):
  class Meta:
    type_ = 'task'
    self_view = 'task_detail'
    self_view_kwargs = {'id': '<id>'}
    self_view_many = 'task_list'

  id = fields.Integer(as_string=True, dump_only=True)
  date_creation = fields.Time(required=True)
  date_modified = fields.Time()
  status = fields.Bool()
  text = db.Str()
  board = Relationship(self_view='task_board',
                       self_view_kwargs={'id': '<id>'},
                       related_view='board_list',
                       related_view_kwargs={'id': '<id>'},
                       schema='BoardSchema',
                       type_='board',
                       id_field='board_id')

# Resource manager
class BoardList(ResourceList):
  schema = BoardSchema
  data_layer = {'session': db.session,
                'model': Board}
class BoardDetail(ResourceDetail):
  schema = BoardSchema
  data_layer = {'session': db.session,
                'model': Board}
class TaskList(ResourceList):
  schema = TaskSchema
  data_layer = {'session': db.session,
                'model': Task}

# Create endpoints
api = Api(app)
api.route(BoardList, 'board_list', '/boards')
api.route(BoardDetail, 'Board_detail', '/boards/<int:id>')
api.route(TaskList, 'task_list', '/tasks')

if __name__ == '__main__':
  app.run(debug=true)
