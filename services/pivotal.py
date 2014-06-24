from os import getenv
import requests

session = None


def get_session():
    global session
    if not session:
        session = requests.session()
        session.headers['X-TrackerToken'] = getenv('PIVOTALTRACKER_API_TOKEN')
    return session


def get(url):
    if not url.startswith('http'):
        url = "https://www.pivotaltracker.com/" + url
    return get_session().get(url)


def get_stories(project_id, ids=None):
    params = {'limit': 500}
    if ids:
        params['filter'] = 'id:%s' % ','.join(map(unicode, ids))
    url = '/services/v5/projects/%s/stories' % project_id
    res = get(url, params=params)
    if res.status_code == 200:
        if res.headers.get('X-Tracker-Pagination-Total'):
            total = res.headers.get('X-Tracker-Pagination-Total')
            offset = res.headers.get('X-Tracker-Pagination-Total')
        return res.json()
    else:
        raise Exception('Error getting stories (%s): %s, %s' %
                        (url, res.status_code, res.content))
