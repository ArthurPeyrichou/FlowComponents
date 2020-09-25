import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'filter' not in instance.options:
      instance.send(df)
      return

    if ';' in instance.options['filter']:
      columns = instance.options['filter'].split(';')
    else:
      columns = [instance.options['filter']]

    df = df[columns]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_filtercolumns',
  'title': 'Filter Columns',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'minus',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'filter': ''
  },
  'details': {
    'filter': {
      'input': 'text',
      'info': 'The list of columns to keep separates by semicolon.',
      'beautifulName': 'Columns list'
    }
  },
  'readme': 'This component allow you to filter columns of a DataFrame.',
  'install': install
}
