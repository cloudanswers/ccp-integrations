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


def sync(pivotal_ids=None, pivotal_project_id=None):
    logging.info('starting sync of pivotal to toggl')
    if not pivotal_project_id:
        pivotal_project_id = getenv('PIVOTALTRACKER_PROJECT_ID')
    toggl_clients = toggl.get_clients(getenv('TOGGL_WORKSPACE_ID'))
    logging.info('retrieved %s toggl clients' % len(toggl_clients))
    pivotal_stories = pivotal.get_stories(pivotal_project_id,
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
        project_marker = ' #%s' % pivotal_story.get('id')
        new_project_name = pivotal_story.get('name') + project_marker
        new_project = {
            'wid': int(getenv('TOGGL_WORKSPACE_ID')),
            'cid': __toggl_client_id(pivotal_story, toggl_clients),
            'name': new_project_name,
            'estimated_hours': pivotal_story.get('estimate'),
            'active': True,
            'is_private': False,
        }

        if pivotal_story.get('story_type') not in ('feature', 'bug', 'chore'):
            logging.info('not a target story type, skipping')
            continue

        existing_found = None
        for toggl_project in toggl_projects:
            if project_marker in toggl_project.get('name'):
                existing_found = toggl_project
                break

        if existing_found:
            new_project['id'] = existing_found.get('id')
            new_project['active'] = existing_found.get('active')

        if pivotal_story.get('current_state') == 'accepted':
            if not existing_found or not existing_found.get('active'):
                logging.debug('already archived, skipping')
                continue
            new_project['active'] = False

        if pivotal_story.get('current_state') == 'unscheduled':
            logging.info('not a target story state, skipping')
            continue

        def need_update(l, r):
            for (k, v) in l.items():
                if r.get(k) != v:
                    logging.debug('%s different, %s vs %s' % (k, v, r.get(v)))
                    return True

        if existing_found and not need_update(new_project, existing_found):
            logging.info('records in sync, no update')
            continue
        logging.info('going to update %s vs %s' % (new_project, existing_found))
        toggl.save_project(new_project)
