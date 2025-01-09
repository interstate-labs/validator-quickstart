import subprocess
import re

# Function to parse ports from Docker container names
def get_ports_and_names():
    docker_ps_output = subprocess.check_output(["docker", "ps", "-a"]).decode("utf-8")
    lines = docker_ps_output.split("\n")[1:]  # Skip the header
    container_ports = {}

    for line in lines:
        if not line.strip():
            continue
        # Split the line dynamically, keeping the last field as 'name'
        parts = re.split(r'\s{2,}', line)
        name = parts[-1]
        ports = parts[-2] if len(parts) > 6 else ""
        container_ports[name] = ports.split(", ") if ports else []
    
    return container_ports

# Populate environment variables
def populate_env(container_ports):
    env_vars = {
        "COMMITMENT_PORT": "9061",
        "METRICS_PORT": "8018",
        "CHAIN": "kurtosis",
        "VALIDATOR_INDEXES": "0..64",
        "BEACON_API_URL": "http://cl-1-lighthouse-geth:4000",
        "EXECUTION_API_URL": "http://el-1-geth-lighthouse:8545",
        "ENGINE_API_URL": "http://el-1-geth-lighthouse:8551",
        "COLLECTOR_URL": "http://cb_pbs:18550",
        "COLLECTOR_SOCKET": "ws://127.0.0.1:4000/ws",
        "BUILDER_PORT": "9062",
        "JWT": "dc49981516e8e72b401a63e6405495a32dafc3939b5d6d83cc319ac0388bca1b",
        "SLOT_TIME": "2",
        "COMMITMENT_DEADLINE": "100",
        "FEE_RECIPIENT": "0x8aC112a5540f441cC9beBcC647041A6E0D595B94",
        "KEYSTORE_SECRETS_PATH": "/app/keystores/secrets",
        "KEYSTORE_PUBKEYS_PATH": "/app/keystores/keys",
        "DELEGATIONS_PATH": "/app/delegations.json",
        "GATEWAY_CONTRACT": "0x6db20C530b3F96CD5ef64Da2b1b931Cb8f264009",
    }

    # Update environment variables dynamically
    for name, ports in container_ports.items():
        if "cl-1-lighthouse-geth" in name and ports:
            env_vars["BEACON_API_URL"] = f"http://{name}:{ports[0].split('->')[1].split('/')[0]}"
        if "el-1-geth-lighthouse" in name and ports:
            for port_mapping in ports:
                host_port, container_port = port_mapping.split("->")
                if container_port.startswith("8551"):
                    env_vars["ENGINE_API_URL"] = f"http://{name}:{host_port}"
                if container_port.startswith("8545"):
                    env_vars["EXECUTION_API_URL"] = f"http://{name}:{host_port}"

        if "kurtosis-logs-collector" in name and ports:
            env_vars["COLLECTOR_SOCKET"] = f"ws://127.0.0.1:{ports[0].split('->')[0]}/ws"

    # Write the .env file
    with open(".config", "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

# Main function
if __name__ == "__main__":
    container_ports = get_ports_and_names()
    populate_env(container_ports)
    print(".config file has been populated.")
