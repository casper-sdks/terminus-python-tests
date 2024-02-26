import configparser


# Provides the test properties configurations

class CONFIG:
    config = configparser.ConfigParser()
    config.read('config.ini')

    def get_docker_name(self):
        return self.config.get("test.properties", "docker_image")

    def get_node_host(self):
        return self.config.get("test.properties", "node_host")

    def get_node_port_rest(self):
        return self.config.get("test.properties", "node_port_rest")

    def get_node_port_rpc(self):
        return self.config.get("test.properties", "node_port_rpc")

    def get_node_port_sse(self):
        return self.config.get("test.properties", "node_port_sse")

    def get_node_port_spec(self):
        return self.config.get("test.properties", "node_port_spec")

    def get_node_chain_name(self):
        return self.config.get("test.properties", "chain_name")

