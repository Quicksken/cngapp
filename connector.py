import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import pymysql


ssh_host = 'sanderdq.hosted-power.dev'
ssh_username = 'cngapp'
ssh_key_path = 'venv/.ssh/key.txt'
ssh_private_key_password = open('venv/.ssh/pwd.txt').readline()
database_username = 'cngapp_db'
database_password = '62PDWXLqMfU6HgF7'
database_name = 'cngapp_db'
localhost = '127.0.0.1'


def open_ssh_tunnel(verbose=False):
    """Open an SSH tunnel and connect using a username and password.

    :param verbose: Set to True to show logging
    :return tunnel: Global SSH tunnel connection
    """

    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_private_key=ssh_key_path,
        ssh_private_key_password=ssh_private_key_password,
        remote_bind_address=('localhost', 3306)
    )

    tunnel.start()
    return tunnel

def mysql_connect(tunnel=False):
    """Connect to a MySQL server using the SSH tunnel connection

    :return connection: Global MySQL database connection
    """
    if not tunnel:
        port = 3306
    else:
        port = tunnel.local_bind_port
    mysql_connection = pymysql.connect(
        host='localhost',
        user=database_username,
        passwd=database_password,
        db=database_name,
        port=port
    )
    mysql_cursor = mysql_connection.cursor()
    return mysql_connection, mysql_cursor

