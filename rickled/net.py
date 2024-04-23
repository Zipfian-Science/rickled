import sys
import traceback
import warnings
import json

import yaml

from rickled import Rickle

try:
    from twisted.web import server, resource
    from twisted.internet import reactor, endpoints, ssl
    from twisted.python import log
except ModuleNotFoundError as exc:
    warnings.warn('Required Python package not found.', ImportWarning)
except ImportError as exc:
    warnings.warn('Required Python package "twisted" not found.', ImportWarning)

try:
    from twisted.internet import ssl
except ModuleNotFoundError as exc:
    warnings.warn('Required Python package not found.', ImportWarning)
except ImportError as exc:
    warnings.warn('Required Python package "pyopenssl" not found.', ImportWarning)


class HttpResource(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def __init__(self, rickle, serialised: bool = False, output_type: str = 'json'):
        self.rickle = rickle
        self.serialised = serialised
        self.output_type = output_type.strip().lower()
        super().__init__()

    def render_GET(self, request):

        uri = request.uri.decode("utf-8")

        try:
            content = self.rickle(uri)
        except NameError as exc:
            request.setResponseCode(404)
            request.setHeader(b"content-type", b"text/html")
            response = f"<html><h1>Not Found</h1> {str(exc)}</html>"
            return response.encode("utf-8")

        request.setResponseCode(200)
        try:
            if isinstance(content, Rickle):
                response = content.dict(self.serialised)
                if self.output_type == 'json':
                    request.setHeader(b"content-type", b"application/json")
                    response = json.dumps(response)
                else:
                    request.setHeader(b"content-type", b"application/yaml")
                    response = yaml.safe_dump(response)
            elif isinstance(content, dict) or isinstance(content, list):
                if self.output_type == 'json':
                    request.setHeader(b"content-type", b"application/json")
                    response = json.dumps(content)
                else:
                    request.setHeader(b"content-type", b"application/yaml")
                    response = yaml.safe_dump(content)
            elif isinstance(content, bytes):
                request.setHeader(b"content-type", b"application/x-binary")
                return content
            elif isinstance(content, str):
                request.setHeader(b"content-type", b"text/html")
                response = content
            elif isinstance(content, int) or isinstance(content, float) or isinstance(content, bool):
                request.setHeader(b"content-type", b"text/html")
                response = str(content)
            else:
                response = content
        except:
            request.setResponseCode(500)
            request.setHeader(b"content-type", b"text/html")
            response = traceback.format_exc()


        return response.encode("utf-8")

def serve_rickle_http(rickle, port: int = 8080, interface: str = '', serialised : bool = False, output_type: str = 'json'):
    log.startLogging(sys.stdout)
    site = server.Site(HttpResource(rickle, serialised=serialised, output_type=output_type))
    reactor.listenTCP(port, site, interface=interface)
    reactor.run()

def serve_rickle_https(rickle, path_to_private_key: str, path_to_certificate: str, port: int = 8080,
                       interface: str = '', serialised : bool = False, output_type: str = 'json'):
    log.startLogging(sys.stdout)
    ssl_context = ssl.DefaultOpenSSLContextFactory(
        path_to_private_key,
        path_to_certificate,
    )

    site = server.Site(HttpResource(rickle, serialised=serialised, output_type=output_type))

    reactor.listenSSL(port, site, ssl_context, interface=interface)
    reactor.run()
