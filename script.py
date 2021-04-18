from os.path import  join
import yaml
import argparse
import sys
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException



def parse_args():
		parser = argparse.ArgumentParser()
		#parser.add_argument('', nargs='+',help = "")		
		return parser.parse_args()


def get_params():
    with open("params.yaml", 'r') as stream:
        try:
            data = (yaml.safe_load(stream))
        except yaml.YAMLError as e:
            print(e)
            exit(1)
    return data


def get_credentials():
    username = input("Username : ")
    password = getpass(prompt= "Password : ")
    return {"username" : username,
            "password" : password,
            "secret"   : ""
    }

def get_connection(host, credentials):
    print(f"Connecting to {host} : ", end="")
    
    props = {
    'device_type': 'cisco_ios',
    'host'      : host,
    'username'  : credentials["username"],
    'password'  : credentials["password"],
    'secret'    : credentials["secret"]
    }

    try:
        conn =  ConnectHandler(**props)
    except NetmikoAuthenticationException as e:
        print(f"FAILED - Invalid credentials")
        return
    except Exception as e:
        print(f"FAILED - exception")
        return

    print("OK")

    return conn
    


def backup_config(conn, suffix):
    config   = conn.send_command('show run')
    filename = conn.host + "_"  + suffix + ".txt"
    path     =  join("configs", filename)
    with open(path, 'w') as f:
        f.write(config)
    print(f"\t{suffix} config saved to {path}")
    
def update_acl(conn, acl_config):
    
    for acl, config in acl_config.items():
        
        print(f"\tUpdating {acl}")

        if "access-list" not in acl:
            print(f"Invalid acl {acl}")
            continue
        
        config  = ["no " + acl] + config
        output  = conn.send_config_set(config)
        if "Invalid input" in output:            
            print(output)
            print("\tError update ACL")
            exit(1)
        else:
            print("\tupdate successful.")
    
def save_config(conn):
    output = conn.send_command('write mem')
    if "Invalid input" in output:            
        print(output)
        print("\tError saving config.")
    else:
        print("\tsave config.")


def main():
    args    = parse_args()
    creds   = get_credentials()    
    params  = get_params()

    for host in params['hosts']:
        conn    = get_connection(host, creds)        
        if not conn:
            continue
        backup_config(conn, "before")
        update_acl(conn, params['access-list'] )
        backup_config(conn, "after")
        save_config(conn)

if __name__ == "__main__":
    main()