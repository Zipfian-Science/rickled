import importlib.util
import sys
import traceback
import warnings
import json

import yaml
import tomli_w as tomlw

from rickled import Rickle, toml_null_stripper

try:
    from twisted.web import server, resource
    from twisted.internet import reactor, endpoints, ssl
    from twisted.python import log
    from twisted.internet import ssl
except (ImportError, ModuleNotFoundError):
    warnings.warn('Required Python package not found.', ImportWarning)


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
        except Exception as exc:
            request.setResponseCode(500)
            request.setHeader(b"content-type", b"text/html")
            response = f"<html><h1>Internal Server Error</h1> {str(exc)}</html>"
            return response.encode("utf-8")

        request.setResponseCode(200)
        try:
            if isinstance(content, Rickle):
                if self.output_type == 'yaml':
                    request.setHeader(b"content-type", b"application/yaml")
                    response = content.to_yaml(serialised=self.serialised)
                elif self.output_type == 'toml':
                    request.setHeader(b"content-type", b"application/toml")
                    response = content.to_toml(serialised=self.serialised)
                elif self.output_type == 'xml' and importlib.util.find_spec('xmltodict'):
                    request.setHeader(b"content-type", b"text/xml")
                    response = content.to_xml(serialised=self.serialised)
                else:
                    request.setHeader(b"content-type", b"application/json")
                    response = content.to_json(serialised=self.serialised)
            elif isinstance(content, dict) or isinstance(content, list):
                if self.output_type == 'yaml':
                    request.setHeader(b"content-type", b"application/yaml")
                    response = yaml.safe_dump(content)
                elif self.output_type == 'toml':
                    request.setHeader(b"content-type", b"application/toml")
                    if isinstance(content, dict):
                        content = toml_null_stripper(content)
                    response = tomlw.dumps(content)
                elif self.output_type == 'xml' and importlib.util.find_spec('xmltodict'):
                    import xmltodict
                    request.setHeader(b"content-type", b"text/xml")
                    if isinstance(content, list):
                        raise ValueError("List can not be dumped as XML.")
                    response = xmltodict.unparse(input_dict=content, pretty=True)
                else:
                    request.setHeader(b"content-type", b"application/json")
                    response = json.dumps(content)
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

def serve_rickle_http(rickle,
                       port: int = 8080,
                       interface: str = '',
                       serialised: bool = False,
                       output_type: str = 'json',
                       path_to_private_key: str = None,
                       path_to_certificate: str = None):
    log.startLogging(sys.stdout)
    site = server.Site(HttpResource(rickle, serialised=serialised, output_type=output_type))

    if path_to_private_key and path_to_certificate:
        ssl_context = ssl.DefaultOpenSSLContextFactory(
            path_to_private_key,
            path_to_certificate,
        )
        reactor.listenSSL(port, site, ssl_context, interface=interface)
    else:
        reactor.listenTCP(port, site, interface=interface)

    reactor.run()
