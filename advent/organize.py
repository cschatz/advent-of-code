from glob import glob
from os import mkdir, path, system
import re

# old_days = glob("years/_2023/solvers/day*.py")

# for old_day in old_days:
#     match = re.search(r"day(\d+).py", old_day)
#     day = match.group(1)
#     try:
#         mkdir(f"years/_2023/day{day}")
#     except:
#         pass
#     system(f"cp {old_day} years/_2023/day{day}/solver.py")
    
inputs = glob("years/_2023/inputs/*")

for input_file in inputs:
    name = path.basename(input_file)
    components = name.split("-")
    daynum = components[0]
    try:
        mkdir(f"years/_2023/{daynum}/inputs")
    except:
        pass
    if len(components) == 2:
        test = components[1]
        system(f"cp {input_file} years/_2023/{daynum}/inputs/{test}")
    else:
        system(f"cp {input_file} years/_2023/{daynum}/inputs/puzzle")
    # print(input_file, path.basename(input_file))