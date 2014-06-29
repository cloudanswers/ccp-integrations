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
        project_marker = ' #%s' % pivotal_story.get('id')
        new_project_name = pivotal_story.get('name') + project_marker
        client_id = __toggl_client_id(pivotal_story, toggl_clients)

        if pivotal_story.get('story_type') not in ('feature', 'bug', 'chore'):
            logging.info('not a target story type, skipping')
            continue

        if pivotal_story.get('current_state') in ('accepted', 'unscheduled'):
            logging.info('not a target story state, skipping')
            continue

        existing_found = None
        for toggl_project in toggl_projects:
            if project_marker in toggl_project.get('name'):
                existing_found = toggl_project
                break

        if existing_found:
            logging.info('existing found')
            compare = (
                ('estimate', 'estimated_hours'),
                ('name', 'name'),
            )
            need_update = False
            for (l, r) in compare:
                left = pivotal_story.get(l)
                right = existing_found.get(r)
                if r == 'name' and right.endswith(project_marker):
                    right = right[:-1*len(project_marker)]
                if pivotal_story.get(left) != existing_found.get(right):
                    logging.info('diff in %s "%s" vs "%s"' % (l, left, right))
                    need_update = True
                    break
            if need_update:
                logging.info('story needs update')
                toggl.save_project(
                    getenv('TOGGL_WORKSPACE_ID'),
                    client_id,
                    name=new_project_name,
                    estimated_hours=pivotal_story.get('estimate'),
                    id=existing_found.get('id')
                )
        else:
            toggl.save_project(
                getenv('TOGGL_WORKSPACE_ID'),
                client_id,
                name=new_project_name,
                estimated_hours=pivotal_story.get('estimate'))
