import configparser


# Provides the test properties configurations

class CONFIG:
    config = configparser.ConfigParser()
    config.read('config.ini')

    def get_docker_name(self):
        return self.config.get("test.properties", "docker_image")

    def get_nctl_host(self):
        return self.config.get("test.properties", "nctl_host")

    def get_nctl_port_rest(self):
        return self.config.get("test.properties", "nctl_port_rest")

    def get_nctl_port_rpc(self):
        return self.config.get("test.properties", "nctl_port_rpc")

    def get_nctl_port_sse(self):
        return self.config.get("test.properties", "nctl_port_sse")
