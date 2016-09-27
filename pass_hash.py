__author__ = 'jade'
from flask.ext.bcrypt import Bcrypt
bcrpt = Bcrypt()
class Hssh:
    def __init__(self, password):
        self.setpassword = password

    def hashpassword(self):
        return bcrpt.generate_password_hash(str(self.setpassword))

    def chkpassword(self,new):
        return bcrpt.check_password_hash(new, self.setpassword)



#me = Hssh('12345678')
#print me.hashpassword()
#print me.chkpassword('$2b$12$evOdjOlsaWxT1zloZMPReOK9izjvtjXR7hcAh28YCMftrQ0Xwe3b2')

#print me.chkpassword('hirok')