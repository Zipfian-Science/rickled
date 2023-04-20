import warnings

try:
    from twisted.web import server, resource
    from twisted.internet import reactor, endpoints
except ImportError as exc:
    warnings.warn('Python package "twisted" required for net op!', ImportWarning)

class HttpResource(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def __init__(self, rickle):
        self.rickle = rickle
        super().__init__()

    def render_GET(self, request):
        request.setHeader(b"content-type", b"text/plain")

        content = u""

        return content.encode("ascii")

def expose_rickle_http(rickle, port: int = 8080):
    site = server.Site(HttpResource(rickle))
    reactor.listenTCP(port, site)
    reactor.run()