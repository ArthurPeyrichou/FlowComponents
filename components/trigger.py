import logging
import json

def onClick(instance, *args):
  instance.send(instance.custom['value'])

def onOptions(instance, *args):
  if 'datatype' not in instance.options:
    instance.custom['value'] == ''
  elif instance.options['datatype'] == 'integer':
    instance.custom['value'] = int(instance.options['data'])
  elif instance.options['datatype'] == 'float':
    instance.custom['value'] == float(instance.options['data'])
  elif instance.options['datatype'] == 'boolean':
    instance.custom['value'] == bool(instance.options['data'])
  elif instance.options['datatype'] == 'object':
    try:
      instance.custom['value'] = json.loads(instance.options['data'])
    except Exception as e:
      instance.error(str(e))
      return
  elif instance.options['datatype'] == 'string':
    instance.custom['value'] = instance.options['data']
  else:
    instance.custom['value'] = ''

def install(instance):
  instance.custom['value'] = None

  instance.on('click', onClick)
  instance.on('options', onOptions)

  onOptions(instance)

EXPORTS = {
  'id': 'trigger',
  'title': 'Trigger',
  'author': 'Arthur Chevalier',
  'color': '#F6BB42',
  'click': True,
  'output': 1,
  'icon': 'play',
  'version': '1.2.0',
  'readme': 'Clicking on the component starts the chain.',
  'install': install
}
