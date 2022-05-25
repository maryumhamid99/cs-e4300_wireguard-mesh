import os
import requests 
import json
import sys
import re


def main():
    overlay_id = sys.argv[1]
    device_id = sys.argv[2]
    device_id2 = sys.argv[3]
 

    with open("token.txt", "r") as file:
        response_token = file.read()

    response = json.loads(response_token)


    # with open("api.key", "r") as file:
    #     api_key = file.read()

    # response = requests.get(f'http://meshmash.vikaa.fi:49177/devices/{device_id}/token', headers={"x-api-key" : f'{api_key}'})
  
    print("response_token")

    print(response_token)
    print(type(response_token))



    token = response["token"]
    print("token")

    print(token)
    print(type(token))
    
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

