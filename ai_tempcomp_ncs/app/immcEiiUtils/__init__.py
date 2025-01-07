import eii.msgbus as mb
import os
import sys
import cfgmgr.config_manager as cfg

# callback function gets called upon watch notification on <key>
def callback_func(key, json):
    print('key {} has been updated, restarting the service'.format(key))
    sys.exit(0)

class EiiConfigMgr:
    def __init__(self):
        # Intialize the message buxs context with config manager
        print('[INFO] Initializing message bus context')
        self.ctx = cfg.ConfigMgr()
        self.watch_cfg = self.ctx.get_watch_obj()
        
        # Watch on key /<AppName>
        key_to_watch = '/' + os.environ['AppName'] + '/'
        self.watch_cfg.watch_prefix(key_to_watch, callback_func)

    def get_config_dict(self) -> dict:
        return self.ctx.get_app_config().get_dict()
    
class EiiClient:
    def __init__(self, cfgMgrCtx: EiiConfigMgr, name):
        # Intialize the client
        if cfgMgrCtx.ctx.get_num_clients() == -1:
            raise "No client instances found, exiting..."
        self.ctx = cfgMgrCtx.ctx.get_client_by_name(name)
        msgbus_cfg = self.ctx.get_msgbus_config()

        self.msgbus = mb.MsgbusContext(msgbus_cfg)
        print(f'[INFO] Initializing service for {name}')
        self.client = self.msgbus.get_service(name)
        print(f'[INFO] Client {name} Running...')

    def request(self, request):
        self.client.request(request)
    
    def recv(self, timeout=None, blocking=None):
        if timeout and blocking:
            return self.client.recv(timeout=timeout, blocking=blocking)
        elif timeout:
            return self.client.recv(timeout=timeout)
        elif blocking:
            return self.client.recv(blocking=blocking)
        else:
            return self.client.recv()
        
    def close(self):
        self.client.close()

class EiiServer:
    def __init__(self, cfgMgrCtx: EiiConfigMgr, name):
        # Initialize the server
        if cfgMgrCtx.ctx.get_num_servers() == -1:
            raise "No server instances found, exiting..."
        self.ctx = cfgMgrCtx.ctx.get_server_by_name(name)
        msgbus_cfg = self.ctx.get_msgbus_config()

        self.msgbus = mb.MsgbusContext(msgbus_cfg)
        print(f'[INFO] Initializing service for {name}')
        self.server = self.msgbus.new_service(name)
    
    def response(self, response):
        self.server.response(response)

    def recv(self, timeout=None, blocking=None):
        if timeout and blocking:
            return self.server.recv(timeout=timeout, blocking=blocking)
        elif timeout:
            return self.server.recv(timeout=timeout)
        elif blocking:
            return self.server.recv(blocking=blocking)
        else:
            return self.server.recv()
    
    def close(self):
        self.server.close()

class EiiSubscriber:
    def __init__(self, cfgMgrCtx: EiiConfigMgr, name, topic):
        # Intialize the subscriber
        if cfgMgrCtx.ctx.get_num_subscribers() == -1:
            raise "No subscriber instances found, exiting..."
        self.ctx = cfgMgrCtx.ctx.get_subscriber_by_name(name)

        msgbus_cfg = self.ctx.get_msgbus_config()
        print(f'[INFO] Initializing message bus context')
        self.msgbus_sub = mb.MsgbusContext(msgbus_cfg)
        print(f'[INFO] Initializing subscriber for topic "{topic}"')
        self.subscriber = self.msgbus_sub.new_subscriber(topic)
        print(f'[INFO] Subscriber Running...')

    def recv(self, timeout=None, blocking=None):
        if timeout and blocking:
            return self.subscriber.recv(timeout=timeout, blocking=blocking)
        elif timeout:
            return self.subscriber.recv(timeout=timeout)
        elif blocking:
            return self.subscriber.recv(blocking=blocking)
        else:
            return self.subscriber.recv()
    
    def close(self):
        self.subscriber.close()
        
class EiiPublisher:
    def __init__(self, cfgMgrCtx: EiiConfigMgr, name, topic):
        # Initialize the publisher
        if cfgMgrCtx.ctx.get_num_publishers() == -1:
            raise "No publisher instances found, exiting..."
        self.ctx = cfgMgrCtx.ctx.get_publisher_by_name(name)
        msgbus_cfg = self.ctx.get_msgbus_config()

        print(f'[INFO] Initializing message bus context')
        self.msgbus_pub = mb.MsgbusContext(msgbus_cfg)
        print(f'[INFO] Initializing publisher for topic "{topic}"')
        self.publisher = self.msgbus_pub.new_publisher(topic)
        print(f'[INFO] Publisher Running...')
    
    def publish(self, message):
        self.publisher.publish(message)

    def close(self):
        self.publisher.close()
