import http.client
import urllib.parse
import copy
import json
import logging

from . import WeclappBaseException

log = logging.getLogger("weclapp-cli")

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

        if method in [ 'POST', 'PUT' ]:
            headers['Content-Type'] = 'application/json'

        log.debug('HTTP %s %s', method, url)
        conn = klass(self.config['domain'])
        try:
            conn.request(method, url, headers=headers, body=body)
            resp = conn.getresponse()
        except Exception as e:
            raise WeclappError('Unable to make the API call: %s' % str(e))

        log.debug('HTTP call returned: %s', resp.status)

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
