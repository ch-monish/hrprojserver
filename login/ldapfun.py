
from ldap3 import Connection,SUBTREE
from decouple import config

def connecttoad(email,password):
    try:
        con=Connection(config("LDAPIP"),email,password,auto_bind=True)
        if con.result['description']=="success":
            con.unbind()
            return True
        else:
            return False
    except Exception as e:
        return e
