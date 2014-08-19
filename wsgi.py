from werkzeug.contrib.fixers import ProxyFix

from dotasalt import app

app.wsgi_app = ProxyFix(app.wsgi_app)
app.run(debug=True, port=7070)