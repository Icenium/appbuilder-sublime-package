import os
import json
import codecs

class Project(object):
    PROJECT_FILE_NAME = ".abproject"

    @staticmethod
    def get_project_dir(path):
        pair = [path, ".."]
        while bool(pair[1]):
            if Project._has_project_file(pair[0]):
                return pair[0]
            else:
                pair = os.path.split(pair[0])
        return ""

    @staticmethod
    def _has_project_file(path):
        if os.path.exists(path):
            files = map((lambda filename: os.path.basename(filename)), os.listdir(path))
            return Project.PROJECT_FILE_NAME in files
        return False

    @staticmethod
    def get_project_name(path):
        try:
            json_data = codecs.open(os.path.join(path, Project.PROJECT_FILE_NAME), "r", "utf-8")
            project_data = json.load(json_data)
            return project_data["DisplayName"]
        except UnicodeError as e:
            print("Unable to parse project file: " + Project.PROJECT_FILE_NAME)
            # Do not raise error here, just return empty string. The calling method will start the first project in the dir, so getting DisplayName is optional
            return ""
