from os import getenv
import pivotal
import toggl


def sync():
    pivotal_stories = pivotal.get_stories(getenv('PIVOTALTRACKER_PROJECT_ID'))
    toggl_projects = toggl.get_projects(getenv('TOGGL_WORKSPACE_ID'))

    for pivotal_story in pivotal_stories:
        if pivotal_story.get('kind') != 'story':
            continue

        if pivotal_story.get('current_state') == 'accepted':
            continue

        existing_found = False
        for toggl_project in toggl_projects:
            project_marker = ' #%s' % pivotal_story.get('id')
            if project_marker in toggl_project.get('name'):
                existing_found = True
                break
        if not existing_found:
            # TODO: create a new one
            new_project_name = pivotal_story.get('name') + project_marker
            toggl.create_project(new_project_name, getenv('TOGGL_WORKSPACE_ID'))

if __name__ == '__main__':
    sync()