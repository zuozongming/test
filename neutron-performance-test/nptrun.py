__author__ = '15090944'
import argparse
from oslo.config import cfg
from oslo import messaging
from npt.utils import get_credentials
import sys

parser = argparse.ArgumentParser(description="Test Neutron's performance from API and RPC")
parser.add_argument("-t","--thread", type=int, help="thread to spawn", default=24)
parser.add_argument("-m","--maxnum", type=int, help="test numbers to spawn", default=200)
parser.add_argument("-a","--api", type=bool, help="run api test", default=False)
parser.add_argument("-r","--rpc", type=bool, help="run rpc test", default=False)
parser.add_argument("--config", help="neutron config file", default="/etc/neutron/neutron.conf")
parser.add_argument("--username", help="username")
parser.add_argument("--password", help="password")
parser.add_argument("--auth_url", help="auth_url: example http://192.168.75.150:5000/v2.0/")
parser.add_argument("--tenant_name", help="tenant name ")
parser.add_argument("--testclass", help="test class name")


args = parser.parse_args()
cfg.CONF([], project='test', default_config_files=[args.config])

if args.api:
    tests = ['TestGetToken',
             'TestAuthToken',
             'TestCreateTenant',
             'TestDeleteTenant',
             'TestCreateNetwork',
             'TestGetNetworkInfo',
             'TestDeleteNetwork',]

    for t in tests:
        module_meta = sys.modules["npt.tests"]
        class_meta = getattr(module_meta, t)
        test = class_meta(thread=args.thread, maxnum=args.maxnum, credentials=get_credentials(args))
        test.run()
        print test.get_result()



if args.rpc:
    pass
if args.testclass:
    module_meta = sys.modules["npt.tests"]
    class_meta = getattr(module_meta, args.testclass)
    test = class_meta(thread=args.thread, maxnum=args.maxnum, credentials=get_credentials(args))
    test.run()
    print test.get_result()



