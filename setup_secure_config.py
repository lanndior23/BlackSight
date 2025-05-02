from core.secure_config import encrypt_config

data = {
    "SHODAN_API_KEY": "s2dddvhbEAUEzYTPRAQGxxixngP4vcwe",
    "VIRUSTOTAL_API_KEY": "c78d370ae6aba2896d76a3120f60894ac1ff99074c13e030b3aec90862d529f4"
}

encrypt_config(data, password="blacksight", config_file="custom_config.sec")
