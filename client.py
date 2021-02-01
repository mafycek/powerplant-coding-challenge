import requests
import json

send_request = False

localhost_url = 'http://127.0.0.1:8888/productionplan'
docker_url = 'http://172.17.0.2:8888/productionplan'

if __name__ == "__main__":
    filename = "example_payloads/payload1.json"

    with open(filename, "rt") as file_handler:
        payload = json.load(file_handler)

    if send_request:
        json_paylod = json.dumps(payload)
        answer = requests.post(docker_url, json=json_paylod)
        if answer.ok:
            print("Correctly processed")

            print(answer.text)
        else:
            print("Error happened")
    else:
        from powerplant_payload import processing_output

        output = processing_output(payload)
        print(output)