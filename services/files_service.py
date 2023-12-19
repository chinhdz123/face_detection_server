import os 
import yaml
import time
import random

# handle file 
def yaml2dict(filename):
    try:
        exist = os.path.exists(filename)
        if not exist:
            f = open(filename, 'w+')
            f.close()
        file = open(filename, 'r', encoding='utf8')
        res = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return res
    except:
        return {}

def dict2yaml(dict_, filename):
    with open(filename, 'w', encoding='utf-8') as outfile:
        yaml.dump(dict_, outfile, default_flow_style=False, allow_unicode=True)



def create_random_filename(filename):
    return str(time.time())+"_"+str(random.randint(100000, 999999))+"."+filename