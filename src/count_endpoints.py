import yaml
import os
from tabulate import tabulate

files_path = "./../v2"
files = os.listdir(files_path)
files.sort()
headers = ["Category", "#Endpoints", "#Requests", "#GET", "#POST", "#PUT", "#DELETE"]
result = [["Total", 0, 0, 0, 0, 0, 0]]
i=0
for file in files:
    if file.endswith(".yml"):
        result.append([file.replace('mist.openapi.', '').replace('.yml', ''),0,0,0,0,0,0])
        i+=1
        #print(f" {file.replace('mist.openapi.', '').replace('.yml', '')} ".center(80, "-"))
        with open(f"{files_path}/{file}", 'r') as f:            
            content = yaml.load(f, Loader=yaml.SafeLoader)
            # get=0
            # post=0
            # put=0
            # delete=0
            # total=0
            result[i][1] = len(content['paths'])
            result[0][1] += len(content['paths'])
            for path in content["paths"]:
                if "get" in content["paths"][path]:
                    # get+=1
                    # total+=1
                    result[i][2]+=1
                    result[i][3]+=1
                    result[0][2]+=1
                    result[0][3]+=1
                if "post" in content["paths"][path]:
                    # get+=1
                    # total+=1
                    result[i][2]+=1
                    result[i][4]+=1
                    result[0][2]+=1
                    result[0][4]+=1
                if "put" in content["paths"][path]:
                    # get+=1
                    # total+=1
                    result[i][2]+=1
                    result[i][5]+=1
                    result[0][2]+=1
                    result[0][5]+=1
                if "delete" in content["paths"][path]:
                    # get+=1
                    # total+=1
                    result[i][2]+=1
                    result[i][6]+=1
                    result[0][2]+=1
                    result[0][6]+=1
print(tabulate(result, headers, tablefmt="github"))
#             total_endpoints += len(content['paths'])
#             total_requests += total
#             print(f"Endpoints   : {len(content['paths'])}")
#             print(f"API Requests: {total} (GET: {get}, POST: {post}, PUT: {put}, DELETE: {delete})")
#             print()
# print("".center(80,"-"))
# print()
# print(f"Totlal Endpoints   : {total_endpoints}")
# print(f"Total API Requests: {total_requests}")
