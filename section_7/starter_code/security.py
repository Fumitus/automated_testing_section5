from werkzeug.security import safe_str_cmp
from section_7.starter_code.models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when a user call endpoint /auth
    wit there username and password.
    :param username: User's username is string format.
    :param password: User's un-encripted password is string format.
    :return: A UserModel if authentication was successful. Otherwise None.
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """
    Function that gets called when user already authenticated, and FLAS-JWT verified
    their authorization header is correct.
    :param payload: A dictionary with 'identity' key which is user id.
    :return:A UserModel object.
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

