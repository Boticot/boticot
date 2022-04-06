import json
import bcrypt
from persistence.users_repository import UsersRepository

class UsersService(object):

    __instance = None

    @staticmethod 
    def get_instance():
      """ Static access method. """
      if UsersService.__instance is None:
         UsersService()
      return UsersService.__instance
      
    def __init__(self):
      """ Virtually private constructor. """
      if UsersService.__instance is not None:
         raise Exception("UsersService is a singleton!")
      else:
         self.users_repository = UsersRepository()
         UsersService.__instance = self

    def add_new_user(self, email, first_name, last_name, password, role, agents):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        user = {
                    "email": email, 
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                    "role": role,
                    "agents": agents,
                    "is_first_login": True
                }
        self.users_repository.add_user(user)

    def find_user(self, email):
        return self.users_repository.get_user(email)

    def exist_super_admin_user(self):
        if self.users_repository.get_one_user_by_role("super-admin"):
            return True
        else:
            return False

    def check_user(self, email, password):
        user = self.users_repository.get_user(email)
        if user:
            a = password.encode()
            b = user.get("password")
            if bcrypt.checkpw(a, b):
                return user
        return None

    def reset_user_password(self, email, new_password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(new_password.encode(), salt)
        self.users_repository.update_user_password(email, bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()))

    def update_user_information(self, email, first_name, last_name, role, agents):
        self.users_repository.update_user_data(email, first_name, last_name, role, agents)

    def get_all_users(self):
        db_users = self.users_repository.find_all_users()
        users = []
        for entry in db_users:
            del entry["_id"]
            del entry["password"]
            users.append(entry)
        return { 
            "count" : len(users),
            "users": users
            }

    def get_user_information(self, email):
        db_user = self.users_repository.get_user(email)
        del db_user["_id"]
        del db_user["password"]
        return db_user
    
    def delete_user(self, email):
        self.users_repository.delete_user(email)

    def is_user_super_admin(self, email):
        user = self.find_user(email)
        return user.get("role") == "super-admin"

    def is_role_super_admin(self, role):
        return role == "super-admin"

    def remove_agent_from_all_attached_users(self, agent_name):
        db_users = self.users_repository.get_users_by_agent_access(agent_name)
        for user in db_users:
            self.users_repository.delete_user_agent(user["email"], agent_name)
