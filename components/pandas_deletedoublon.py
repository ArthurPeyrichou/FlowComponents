import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'columns' in instance.options and instance.options['columns'] != '':
      if ';' in instance.options['columns']:
        df = df.drop_duplicates(subset=instance.options['columns'].split(';'), keep='last') 
      else:
        df = df.drop_duplicates(subset=[instance.options['columns']], keep='last') 
    else:
      df = df.drop_duplicates(keep='last') 

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_deletedoublon',
  'title': 'Delete doublon',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'delete',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'columns': ''
  },
  'details': {
    'columns': {
      'input': 'text',
      'info': 'The list of columns to delete doublon separates by semicolon (if empty treat all columns).',
      'beautifulName': 'Columns list'
    }
  },
  'readme': 'This component allow you to delete doublon values in a DataFrame.',
  'install': install
}
