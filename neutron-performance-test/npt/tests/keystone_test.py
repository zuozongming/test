from npt.utils import Excutor
from keystoneclient.v2_0 import client
from oslo.config import cfg
import httplib
import json
import urlparse

class TestGetToken(Excutor):
    def getToken(self):
        params = '{"auth": {"tenantName": "%s", "passwordCredentials":' \
                 ' {"username": "%s", "password": "%s"}}}' \
                 %(self.credentials["tenant_name"],
                   self.credentials["username"],
                   self.credentials["password"])
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        auth_url=self.credentials["auth_url"]
        parsedTuple = urlparse.urlparse(auth_url)
        addr = parsedTuple.netloc.split(":")[0]
        port = parsedTuple.netloc.split(":")[1]
        conn = httplib.HTTPConnection(addr, port, False, 120)
        conn.request("POST", "/v2.0/tokens", params, headers)
        response = conn.getresponse()
        data = response.read()
        dd = json.loads(data)
        conn.close()

    def test_method(self):
        try:
            self.getToken()
            self.curnum=self.curnum + 1
        except:
            self.failnum=self.failnum + 1

class TestAuthToken(Excutor):
    def __init__(self, **kwargs):
        super(TestAuthToken, self).__init__(**kwargs)
        self.token=None

    def authToken(self):
        params = '{"auth": {"token": {"id":"%s"}}}' % self.token
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        auth_url=self.credentials["auth_url"]
        parsedTuple = urlparse.urlparse(auth_url)
        addr = parsedTuple.netloc.split(":")[0]
        port = parsedTuple.netloc.split(":")[1]
        conn = httplib.HTTPConnection(addr, port, False, 120)
        conn.request("POST", "/v2.0/tokens", params, headers)
        response = conn.getresponse()
        data = response.read()
        dd = json.loads(data)
        conn.close()

    def test_method(self):
        if self.token:
            try:
                self.authToken()
                self.curnum=self.curnum + 1
            except:
                self.failnum=self.failnum + 1
        else:
            try:
                keystone = client.Client(username=self.credentials["username"],
                                         password=self.credentials["password"],
                                         tenant_name=self.credentials["tenant_name"],
                                         auth_url=self.credentials["auth_url"])
                self.token=keystone.tokens.authenticate(username=self.credentials["username"],
                                                        password=self.credentials["password"],
                                                        tenant_name=self.credentials["tenant_name"]).id

            except:
                pass


TENANT_NAME_PREFIX="TEST_TENANT_"
class TestCreateTenant(Excutor):
    def __init__(self, **kwargs):
        super(TestCreateTenant, self).__init__(**kwargs)
        self.keystone=None
        self.userid=None
        self.adminroleid=None

    def get_keystone_client(self):
        try:
            keystone = client.Client(username=self.credentials["username"],
                                     password=self.credentials["password"],
                                     tenant_name=self.credentials["tenant_name"],
                                     auth_url=self.credentials["auth_url"])
            token = self.keystone.tokens.authenticate(username=self.credentials["username"],
                                          password=self.credentials["password"],
                                          tenant_name=self.credentials["tenant_name"])
            self.userid = token.user['id']
            self.adminroleid = token.metadata['roles'][0]
            return keystone
        except:
            return None

    def create_tenant_and_add_role(self):
        tenant = self.keystone.tenants.create(tenant_name=TENANT_NAME_PREFIX+str(self.threadnum%(self.maxnum+1)),
                                         description="test tenant", enabled=True)
        admin_user = self.keystone.users.get(self.userid)
        admin_role = self.keystone.roles.get(self.adminroleid)
        self.keystone.roles.add_user_role(admin_user, admin_role, tenant)

    def test_method(self):
        if not self.keystone:
            self.keystone=self.get_keystone_client()
        try:
            self.create_tenant_and_add_role()
            self.curnum=self.curnum + 1
        except:
            self.keystone=self.get_keystone_client()
            self.failnum=self.failnum + 1

class TestDeleteTenant(Excutor):
    def __init__(self, **kwargs):
        super(TestDeleteTenant, self).__init__(**kwargs)
        self.keystone=None

    def get_keystone_client(self):
        try:
            keystone = client.Client(username=self.credentials["username"],
                                     password=self.credentials["password"],
                                     tenant_name=self.credentials["tenant_name"],
                                     auth_url=self.credentials["auth_url"])
            return keystone
        except:
            return None

    def delete_tenant(self):
        tenants = self.keystone.tenants.list()
        for t in tenants:
            if str(t.name).startswith(TENANT_NAME_PREFIX):
                self.keystone.tenants.delete(t)
                print 'tenant deleted ' + t.name
                break

    def test_method(self):
        if not self.keystone:
            self.keystone=self.get_keystone_client()

        try:
            self.delete_tenant()
            self.curnum=self.curnum + 1
        except:
            self.keystone=self.get_keystone_client()
            self.failnum=self.failnum + 1