from twisted.internet import reactor
from twisted.web import resource
from twisted.web import server

class ResultsResource(resource.Resource):

  def __init__(self, results):
    resource.Resource.__init__(self)
    self.results = results

  def getChild(self, path, request):
    lines = self.results[path]
    return TextResource('\n'.join(lines))

  def render_GET(self, request):
    request.setHeader('content-type', 'text/plain')
    return '%d results available' % len(self.results)

class TextResource(resource.Resource):

  def __init__(self, text):
    self.text = text

  def render_GET(self, request):
    request.setHeader('content-type', 'text/plain')
    return self.text

def get_url(name):
  return 'http://gopher.strangled.net:8000/results/%s' % name

def start_web(results):
  root = resource.Resource()
  root.putChild('results', ResultsResource(results))
  site = server.Site(root)
  reactor.listenTCP(8000, site)