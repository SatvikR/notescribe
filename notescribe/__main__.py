from notescribe import app, settings

port = settings['port']
debug = settings['debug']

app.run(port=port, debug=debug)
