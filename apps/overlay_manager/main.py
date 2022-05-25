import os
import requests
import json
import sys
from requests.structures import CaseInsensitiveDict

import re

def refresh_token(device_id, token):
    print(token)
    print("token")
    headers = CaseInsensitiveDict()
    headers["Accept"] = "*/*"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + token
    url = "http://meshmash.vikaa.fi:49177"+ "/devices/" + device_id + "/token"
    resp = requests.get(url, headers=headers)


    print("response")
    print(resp.json())


    return resp.json()["token"]

def main():
    print(sys.argv[3])
    overlay_id = sys.argv[1]
    device_id = sys.argv[2]

    with open("token.txt", "r") as file:
        token = file.read().strip()
    print(token)

    token = refresh_token(device_id, token)

    config = requests.get(f'http://meshmash.vikaa.fi:49177/overlays/{overlay_id}/devices/{device_id}/wgconfig?', headers={'Authorization': f'Bearer {token}'})
    final_config = re.sub(r"Peer \d+", "Peer", config.content.decode("utf-8"))
    final_config = final_config.replace(": 51820", ":5555")
    print("final_config")
    print(final_config)


    with open("sample.txt", "r") as file:
        sample_interface = file.read()

    with open("private.key", "r") as file:
        private_key = file.read()

    sample_interface = sample_interface.format(private_key=private_key, virtual_address=sys.argv[3])

    with open("/etc/wireguard/wg0.conf", "w") as file:
        file.write(sample_interface + "\n" +final_config)

    os.system("sudo systemctl enable wg-quick@wg0.service")
    os.system("sudo systemctl start wg-quick@wg0.service")


if __name__ == "__main__" :
    main()