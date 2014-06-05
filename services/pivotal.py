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


def get_stories(project_id):
    url = '/services/v5/projects/%s/stories?filter=state:delivered,finished,rejected,started&limit=500' % project_id
    res = get(url)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception('Error getting stories (%s): %s, %s' %
                        (url, res.status_code, res.content))
