import re
import json
import urllib.request
from distutils.version import StrictVersion,LooseVersion
from itertools import product
import delegator
import os

def versions(package_name,version_no,char):

    url = "https://pypi.python.org/pypi/%s/json" % (package_name,)
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    versions = data["releases"].keys()
    versions = list(versions)
    b = ["rc","b","p1","b1"]
    versions = [x for x in versions if not any(y in x for y in b)]

    if char == "==" or char =="===":
        versions = [x for x in versions if LooseVersion(x) == LooseVersion(version_no)]
    elif char == ">":
        versions = [x for x in versions if LooseVersion(x) > LooseVersion(version_no)]
    elif char ==">=":
        versions = [x for x in versions if LooseVersion(x) >= LooseVersion(version_no)]
    elif char == "<":
        versions = [x for x in versions if LooseVersion(x) < LooseVersion(version_no)]
    elif char == "<=":
        versions = [x for x in versions if LooseVersion(x) <= LooseVersion(version_no)]
    elif char == "!=":
        versions = [x for x in versions if LooseVersion(x) != LooseVersion(version_no)]

    sorted(versions,key=LooseVersion)
    return versions

with open("stack.txt","r") as f:
    package_versions = dict()
    for line in f:
        cleaned_line = line.strip()
        
        pckg_name = re.findall("[a-zA-Z]+", cleaned_line)
        ver_no = re.findall(r'\s*([\d.]+)', cleaned_line)
        if not ver_no:
            ver_no = "0"
        else:
            ver_no = ver_no[0]

        char = re.sub("[\w+.]", "", cleaned_line)

        if not char:
            char = ">"

        print(ver_no,char)
        temp_dict = dict()
        temp_dict = {pckg_name[0]:versions(pckg_name[0],ver_no,char)}
        package_versions = {**package_versions,**temp_dict}

#for key,value in package_versions.items():
    #print(key,value)
print(package_versions)
my_list = [dict(zip(package_versions,v)) for v in product(*package_versions.values())]


y = 1
for d in my_list:
    filename = "requirements{0}.txt".format(y)
    with open(filename,'w') as file:
        for key,value in d.items():
            file.write('{0}=={1}\n'.format(key,value))
    y=y+1

directory = "/home/aparekh/try2"
for name in os.listdir(directory):
    filename = os.fsdecode(name)
    command_name = "pip-compile"
    if filename.startswith("requirements1"):
        cmd = '{0} {1}'.format(command_name,filename)
        #os.subproces
        #c = delegator.run('pip-compile requirements1.txt -o req1-locked.txt',block = True)
        #c.err
        #c.out
        #c.std_err
    else:
        continue

