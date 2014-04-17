from .command_executor import show_quick_panel
from .project import Project
from .notifier import log_info, log_error

def select_project(app_builder_command, on_project_selected):
    projects = []
    project_dir = Project.get_project_dir(app_builder_command.get_working_dir())
    if (bool(project_dir)):
        projects.append(project_dir)

    for index, value in enumerate(app_builder_command.get_window().folders()):
        project_dir = Project.get_project_dir(value)
        if (bool(project_dir)):
            projects.append(project_dir)

    projects = list(set(projects))
    projects = list(map((lambda project: [Project.get_project_name(project), project]), projects))

    projectsCount = len(projects)
    if projectsCount == 1:
        on_project_selected(projects[0])
    elif projectsCount > 1:
        show_quick_panel(app_builder_command.get_window(), projects, lambda project_index: on_project_selected(projects[project_index]) if project_index >= 0 else on_project_selected(None))
    else:
        log_info("There are no projects in your currently opened folders")
