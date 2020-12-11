from persistence.users_repository import UsersRepository
import json
import bcrypt

class UserService(object):

    __instance = None

    @staticmethod 
    def get_instance():
      """ Static access method. """
      if UserService.__instance is None:
         UserService()
      return UserService.__instance
      
    def __init__(self):
      """ Virtually private constructor. """
      if UserService.__instance is not None:
         raise Exception("UserService is a singleton!")
      else:
         self.users_repository = UsersRepository()
         UserService.__instance = self

    def add_new_user(self, email, first_name, last_name, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        user = {"email": email, "first_name": first_name, "last_name": last_name, "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt())}
        self.users_repository.add_user(user)

    def find_user(self, email):
        return self.users_repository.get_user(email)

    def exist_user(self):
        if self.users_repository.get_one_user():
            return True
        else:
            return False

    def check_user(self, email, password):
        user = self.users_repository.get_user(email)
        if user:
            a = password.encode()
            b = user.get("password")
            if bcrypt.checkpw(a, b):
                return True
        return False