import re

def parse_version_string(version_string):
    return re.split("[\.-]", version_string.strip())[:3]