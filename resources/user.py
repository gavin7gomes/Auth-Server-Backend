import bcrypt
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import JWT, jwt_required

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return { "message": "A user with that username already exists"}, 409
        
        hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
    

        user = UserModel(**data)
        user.password = hashed_password.decode("utf-8")
        user.save_to_db()

        return { "message": "User created successfully"}, 201


class UserList(Resource):
    @jwt_required()
    def get(self):
        return { "items": [x.json() for x in UserModel.query.all()]}