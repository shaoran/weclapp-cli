import http.client
import urllib.parse
import copy
import json

from . import WeclappBaseException

class WeclappError(WeclappBaseException):
    pass


class WeclappAPI(object):
    def __init__(self, config):
        """
        config is a dictionary with the following keys:

         - domain
         - path
         - apitoken
         - ssl
        """
        self.config = config

    def urljoin(self, *args):
        """
        Helper that joins URL path, works like os.path.join
        """
        args = copy.copy(args)
        n = []
        for arg in args:
            arg = arg.strip()
            if arg.endswith('/'):
                arg = arg[0:-1]
            n.append(arg)

        return '/'.join(n)

    def call(self, command, method, query = {}, body = None, expected_status_code = 200):
        """
        Make an API call
        """

        params = urllib.parse.urlencode(query)

        if self.config['ssl']:
            klass = http.client.HTTPSConnection
        else:
            klass = http.client.HTTPConnection

        url = self.urljoin(self.config['path'], command)
        headers = {
            "AuthenticationToken": self.config['apitoken'],
        }

        if params != '':
            url = "%s?%s" % (url, params)

        conn = klass(self.config['domain'])
        try:
            conn.request(method, url, headers=headers, body=body)
            resp = conn.getresponse()
        except Exception as e:
            raise WeclappError('Unable to make the API call: %s' % str(e))

        data = None
        if resp.status != expected_status_code:
            try:
                data = resp.read()
            except:
                pass

            raise WeclappError('Unable to make the API call: HTTP CODE %s :: %s' % (resp.code, data))

        try:
            data = resp.read()
        except Exception as e:
            raise WeclappError('Unable to read response from call: %s' % str(e))

        conn.close()

        content_type = resp.headers.get('Content-Type', None)

        if content_type is None:
            return data

        cts = content_type.split(';')
        if cts[0] == 'application/json':
            kwargs = {}
            if len(cts) > 1 and cts[1].startswith('charset'):
                enc = cts[1].split("=")
                if len(enc) > 1:
                    kwargs['encoding'] = enc[1]

            try:
                data = json.loads(data, **kwargs)
            except Exception as e:
                raise WeclappError('Unable to get JSON response: %s' % str(e))

        return data

    def fetch_projects(self):
        """
        Fetches the projects only, without tasks and without
        time records (activities)
        """
        # avoid circular dependencies when loading the modul
        from .models import WeclappProject

        res = self.call('project', 'GET')

        return [ WeclappProject(**p) for p in res['result'] ]

    def fetch_project_tasks(self):
        """
        Fetches the tasks only, without time records (activities)
        """
        # avoid circular dependencies when loading the modul
        from .models import WeclappTask

        res = self.call('projectTask', 'GET')

        return [ WeclappTask(**p) for p in res['result'] ]


    def fetch_time_records(self):
        """
        Fetches the time records (activities)
        """
        # avoid circular dependencies when loading the modul
        from .models import WeclappTimeRecord

        res = self.call('timeRecord', 'GET', query={'serializeNulls': 1})

        return [ WeclappTimeRecord(**p) for p in res['result'] ]


    def load_projects(self, cache=True):
        """
        Loads all projects, tasks and time records and associate tasks and
        time records with the projects

        If cache is set to True, then the result will be cached
        """
        projects = self.fetch_projects()
        tasks = self.fetch_project_tasks()
        time_records = self.fetch_time_records()

        projects_map = { i.id: i for i in projects }
        tasks_map = { i.id: i for i in tasks }
        time_records_map = { i.id: i for i in time_records }

        for record in time_records:
            if record.task_id not in tasks_map:
                continue

            task = tasks_map[record.task_id]
            task.add_time_record(record)
            record.task = task

        for task in tasks:
            if task.project_id not in projects_map:
                continue

            proj = projects_map[task.project_id]
            proj.add_task(task)
            task.project = proj

        return projects
