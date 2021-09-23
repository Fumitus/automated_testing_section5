from flask_restful import Resource, reqparse
from section_7.starter_code.models.user import UserModel


class UserRegister(Resource):
    """
    This resource allows user to register bys sending a
    POST request with username and password
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username field cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User was created successfully'}, 201

