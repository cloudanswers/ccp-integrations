import logging
from os import getenv
from services import pivotal
from services import toggl


def __toggl_client_id(pivotal_story, toggl_clients):
    """
    find a matching toggl client based on pivotaltracker tag
    :param pivotal_story: dict from pivotal api
    :param toggl_clients: list of toggl clients to match to
    :return: id of toggl client
    """
    def clean(x):
        return x.strip().lower()
    for label in pivotal_story.get('labels'):
        for client in toggl_clients:
            if clean(label.get('name')) == clean(client.get('name')):
                return client.get('id')


def sync(pivotal_ids=None):
    logging.info('starting sync of pivotal to toggl')
    toggl_clients = toggl.get_clients(getenv('TOGGL_WORKSPACE_ID'))
    logging.info('retrieved %s toggl clients' % len(toggl_clients))
    pivotal_stories = pivotal.get_stories(getenv('PIVOTALTRACKER_PROJECT_ID'),
                                          ids=pivotal_ids)
    logging.info('retrieved %s pivotal stories' % len(pivotal_stories))
    toggl_projects = toggl.get_projects(getenv('TOGGL_WORKSPACE_ID'))
    logging.info('retrieved %s toggl projects' % len(toggl_projects))

    if pivotal_ids:
        logging.info('filtering pivotal stories to %s' % pivotal_ids)
        logging.debug('all pivotal stories: %s' % pivotal_stories)
        pivotal_stories = filter(lambda x: x.get('id') in pivotal_ids,
                                 pivotal_stories)
        logging.debug('filtered pivotal stories: %s' % pivotal_stories)

    for pivotal_story in pivotal_stories:
        logging.info('processing pivotal story %s' % pivotal_story.get('id'))

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

        if existing_found:
            logging.info('existing found, skipping')

        if not existing_found:
            new_project_name = pivotal_story.get('name') + project_marker
            client_id = __toggl_client_id(pivotal_story, toggl_clients)
            toggl.create_project(new_project_name,
                                 getenv('TOGGL_WORKSPACE_ID'),
                                 client_id)
