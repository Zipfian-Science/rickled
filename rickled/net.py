import traceback
import warnings
import json

from rickled import Rickle

try:
    from twisted.web import server, resource
    from twisted.internet import reactor, endpoints, ssl
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

    def __init__(self, rickle):
        self.rickle = rickle
        super().__init__()

    def render_GET(self, request):

        content = self.rickle(request.uri.decode("utf-8"))

        try:
            if isinstance(content, Rickle):
                request.setHeader(b"content-type", b"application/json")
                response = content.dict(True)
                response = json.dumps(response)
            elif isinstance(content, dict) or isinstance(content, list):
                request.setHeader(b"content-type", b"application/json")
                response = json.dumps(content)
            elif isinstance(content, str):
                request.setHeader(b"content-type", b"text/html")
                response = content
            else:
                response = content
        except:
            request.setResponseCode(500)
            request.setHeader(b"content-type", b"text/html")
            response = traceback.format_exc()

        return response.encode("utf-8")

def serve_rickle_http(rickle, port: int = 8080):
    site = server.Site(HttpResource(rickle))
    reactor.listenTCP(port, site)
    reactor.run()

def serve_rickle_https(rickle, path_to_private_key: str, path_to_certificate: str, port: int = 8080):
    ssl_context = ssl.DefaultOpenSSLContextFactory(
        path_to_private_key,
        path_to_certificate,
    )

    site = server.Site(HttpResource(rickle))

    reactor.listenSSL(port, site, ssl_context)
    reactor.run()
