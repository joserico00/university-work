from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform

# OpenVAS configuration
OPENVAS_HOST = "localhost"  # Replace with your OpenVAS server's IP if not local
OPENVAS_PORT = 9390  # GMP uses port 9390
USERNAME = "admin"
PASSWORD = "admin"

def test_openvas_connection():
    # Establish TLS connection
    connection = TLSConnection(hostname=OPENVAS_HOST, port=OPENVAS_PORT)
    
    try:
        # Create a GMP object with the connection
        with Gmp(connection=connection, transform=EtreeTransform()) as gmp:
            # Authenticate
            gmp.authenticate(username=USERNAME, password=PASSWORD)
            print("Authenticated successfully with OpenVAS!")
            
            # Fetch version information
            version = gmp.get_version()
            print(f"OpenVAS Version: {version}")
            
            # List all tasks (example)
            tasks = gmp.get_tasks()
            print("Tasks:")
            print(tasks)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_openvas_connection()

