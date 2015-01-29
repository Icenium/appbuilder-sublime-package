import re

def get_major_minor_version_from_string(version_string):
    return re.split("[\.-]", version_string.strip())[:2]
