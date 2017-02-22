from itsdangerous import URLSafeSerializer as utsr



class Token(object):
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = security_key
    def generate_validate_token(self,username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self,token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt,)
    def remove_validate_token(self,token):
        serializer = utsr(self.security_key)
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)



