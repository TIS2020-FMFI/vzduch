from sshtunnel import SSHTunnelForwarder


class Tunnel:
    @staticmethod
    def initialize(username, password):
        tunnel = SSHTunnelForwarder(('hpcdev02', 22), ssh_password=password, ssh_username=username,
                                    remote_bind_address=('srv-mondo', 3306))
        tunnel.start()
