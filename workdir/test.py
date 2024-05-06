
import yaml

filename = "mist.openapi"
verbs = ["get", "post", "put", "delete"]

def open_src():
    oas = ""
    with open(f"./{filename}.yml", 'r') as oas_in_file:
        oas = yaml.safe_load(oas_in_file)
    return oas

req_count = 0
resp_count = 0
count = 0
if __name__ == "__main__":
    data = open_src()
    paths = data.get("paths", {})
    for endpoint in paths:
        for verb in paths[endpoint]:
            if verb in verbs:
                operation_id = paths[endpoint][verb]["operationId"]
                request_content = paths[endpoint][verb].get("requestBody", {}).get("content")
                if request_content and len(request_content.items()) > 1:
                    print(f"-------- {operation_id}")
                    count += 1
                    for item in request_content.items():
                        print(item)
                
                # request = False
                # response = False
                # operationId = paths[endpoint][verb]["operationId"]
                # if "requestBody" in paths[endpoint][verb]:
                #     schema = paths[endpoint][verb]["requestBody"].get("content", {}).get("application/json", {}).get("schema")
                #     if schema and not "$ref" in schema:
                #         request = True
                #         req_count +=1
                # if "responses" in paths[endpoint][verb]:
                #     if not "$ref" in paths[endpoint][verb]["responses"]["200"]:
                #         response = True
                #         resp_count +=1
                # if request or response:
                #     print(f" {operationId} ".center(80, "-"))
                #     if request: print("Request")
                #     if response: print("Response")
            
print()
# print(f"Requests : {req_count}")
# print(f"Responses: {resp_count}")
print(f"count: {count}")