__author__ = '15090944'
from neutronclient.v2_0 import client
from npt.utils import Excutor
from oslo.config import cfg

from neutron import context
import neutron .agent.rpc as nu_rpc
from neutron .common import rpc


NETWORK_NAME_PREFIX="TEST_NETWORK_"
class TestCreateNetwork(Excutor):
    def get_netron_client(self):
        return client.Client(**self.credentials)

    def create_network(self):
        network_name = NETWORK_NAME_PREFIX + str(self.threadnum%(self.maxnum+1))

        body_sample = {'network': {'name': network_name,
                       'admin_state_up': True}}
        neutron = self.get_netron_client()
        netw = neutron.create_network(body=body_sample)
        net_dict = netw['network']
        network_id = net_dict['id']
        body_create_subnet = {'subnets': [{'cidr': '192.168.199.0/24',
                              'ip_version': 4, 'network_id': network_id}]}
        subnet = neutron.create_subnet(body=body_create_subnet)
        body_value = {
                         "port": {
                                 "admin_state_up": True,
                                 "network_id": network_id
                          }
                     }
        for i in range(1,5):
            neutron.create_port(body=body_value)

    def test_method(self):
        try:
            self.create_network()
            self.curnum=self.curnum + 1
        except:
            self.failnum=self.failnum + 1




class TestDeleteNetwork(Excutor):
    def get_neutron_client(self):
        return client.Client(**self.credentials)

    def get_network(self):
        neutron = self.get_neutron_client()
        netws = neutron.list_networks(name=NETWORK_NAME_PREFIX + str(self.threadnum%(self.maxnum+1)))
        return netws['networks'][0]


    def del_network(self, network_id):
        neutron = self.get_neutron_client()
        neutron.delete_network(network_id)


    def get_subnet(self, network_id):
        neutron = self.get_neutron_client()
        subns = neutron.list_subnets(network_id=network_id)
        if len(subns['subnets'])==1:
            return subns['subnets'][0]
        else:
            return None


    def del_subnet(self, subnet_id):
        neutron = self.get_neutron_client()
        neutron.delete_subnet(subnet_id)


    def get_port(self, network_id):
        neutron = self.get_neutron_client()
        ports=neutron.list_ports(network_id=network_id)
        return ports['ports'][0]


    def get_ports(self, network_id):
        neutron = self.get_neutron_client()
        ports=neutron.list_ports(network_id=network_id)
        return ports['ports']


    def del_port(self, port_id):
        neutron = self.get_neutron_client()
        ports=neutron.delete_port(port_id)


    def release_network(self):
        network=self.get_network()
        for port in self.get_ports(network['id']):
            self.del_port(port['id'])

        subnet=self.get_subnet(network['id'])
        if subnet:
            self.del_subnet(subnet['id'])
        self.del_network(network['id'])


    def test_method(self):
        try:
            self.release_network()
            self.curnum=self.curnum + 1
        except:
            self.failnum=self.failnum + 1

class TestGetNetworkInfo(Excutor):

    def get_neutron_client(self):
        return client.Client(**self.credentials)

    def get_network(self):
        neutron = self.get_neutron_client()
        netws = neutron.list_networks(name=NETWORK_NAME_PREFIX + str(self.threadnum%(self.maxnum+1)))
        return netws['networks'][0]


    def get_subnet(self, network_id):
        neutron = self.get_neutron_client()
        subns = neutron.list_subnets(network_id=network_id)
        return subns['subnets'][0]


    def get_port(self, network_id):
        neutron = self.get_neutron_client()
        ports=neutron.list_ports(network_id=network_id)
        return ports['ports'][0]


    def get_ports(self, network_id):
        neutron = self.get_neutron_client()
        ports=neutron.list_ports(network_id=network_id)
        return ports['ports']


    def get_networkinfo(self):
        network=self.get_network()
        self.get_ports(network['id'])
        self.get_subnet(network['id'])


    def test_method(self):
        try:
            self.get_networkinfo()
            self.curnum=self.curnum + 1
        except:
            self.failnum=self.failnum + 1


NEUTRON_FAKE_HOST='NEUTRON_FAKE_HOST_'
class TestRpcReportState(Excutor):
    def __init__(self, **kwargs):
        super(TestRpcReportState, self).__init__(**kwargs)
        cfg.CONF([], project='neutron', default_config_files=['/etc/neutron/neutron.conf'])
        rpc.init(cfg.CONF)
        self.ctxt = context.get_admin_context_without_session()
        self.agent_state = {
                           'binary': 'neutron-openvswitch-agent',
                           'host': 'fakehost.com',
                           'topic': 'N/A',
                           'configurations': {'bridge_mappings': {"physnet2": "br-bond1"},
                                              'tunnel_types': [],
                                              'tunneling_ip': "",
                                              'l2_population': False},
                           'agent_type': "Open vSwitch agent",
                           'start_flag': True
                          }

        self.state_rpc = nu_rpc.PluginReportStateAPI('q-plugin')

    def report_status(self):
        self.agent_state['host']= NEUTRON_FAKE_HOST+ str(self.threadnum%(self.maxnum+1))
        self.state_rpc.report_state(self.ctxt, self.agent_state)

    def test_method(self):
        try:
            self.report_status()
            self.curnum=self.curnum + 1
        except:
            self.failnum=self.failnum + 1