import traceback
import time

def onData(instance, args):
  try:
    payload = args[0]
    data = payload.data
    start = time.process_time()

    if data is None or not isinstance(data, dict) or 'path' not in data:
      # No correct input
      if not 'filename' in instance.options:
        return

      path = instance.options['filename']
      enc = instance.options['encoding'] if 'encoding' in instance.options else 'UTF-8'
      type = instance.options['type'] if 'type' in instance.options else 'buffer'
    else:
      if instance.options['debug']:
        instance.debug('Incoming data: %s' % (data,))
      path = data['path']
      enc = data['encoding'] if 'encoding' in data else (instance.options['encoding'] if 'encoding' in instance.options else 'UTF-8')
      type = data['type'] if 'type' in data else (instance.options['type'] if 'type' in instance.options else 'buffer')

    if type == 'buffer':
      file = open(path, 'rb')
    else:
      file = open(path, 'r', encoding=enc)

    toSend = file.read()
    file.close()

    end = time.process_time()
    delta = (end - start) * 1000.0 # In ms
    instance.flow.updateTraffic(instance.id, 'duration', delta)
    
    instance.send(toSend)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'filereader',
  'title': 'File Reader',
  'author': 'Arthur Chevalier',
  'color': '#989D78',
  'output': 1,
  'input': 1,
  'icon': 'file-alt',
  'version': '1.2.0',
  'group': 'Inputs',
  'options': {
    'filename': '',
    'encoding': 'UTF-8',
    'type': 'text',
    'delimiter': '\\n'
  },
  'details': {
    'filename': {
      'input': 'text',
      'info': 'The path that should be used to access file.',
      'beautifulName': 'File path/name'
    },
    'type': {
      'input': 'text',
      'info': 'The encoding that should be used to read the file.',
      'beautifulName': 'File encoding',
      'example': 'buffer'
    },
    'encoding': {
      'input': 'text',
      'info': 'The encoding that we want in output.',
      'beautifulName': 'Output encoding',
      'example': 'buffer'
    },
    'delimiter': {
      'input': 'text',
      'info': 'The file reading delimiter.',
      'beautifulName': 'Delimiter'
    }
  },
  'readme': 'This component allow you to read a file then convert the encoding.',
  'install': install
}
