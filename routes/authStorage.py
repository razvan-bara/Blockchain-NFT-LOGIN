from models.user import User

class AuthStorage(object):
  
  auth_user : User = None

  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(AuthStorage, cls).__new__(cls)
    return cls.instance

  def set_auth_user(self, user : User):
    self.auth_user = user
   
   
auth_storage = AuthStorage()