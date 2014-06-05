from os import getenv
from services import pivotal
from services import toggl


def __toggl_client_id(pivotal_story, toggl_clients):
    def clean(x):
        return x.strip().lower()
    for label in pivotal_story.get('labels'):
        for client in toggl_clients:
            if clean(label.get('name')) == clean(client.get('name')):
                return client.get('id')


def sync():
    toggl_clients = toggl.get_clients(getenv('TOGGL_WORKSPACE_ID'))
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
            new_project_name = pivotal_story.get('name') + project_marker
            client_id = __toggl_client_id(pivotal_story, toggl_clients)
            toggl.create_project(new_project_name,
                                 getenv('TOGGL_WORKSPACE_ID'),
                                 client_id)

if __name__ == '__main__':
    sync()