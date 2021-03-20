from notescribe import app, settings

port = settings['port']
debug = settings['debug']
host = settings['host']

app.run(port=port, host=host, debug=debug)
