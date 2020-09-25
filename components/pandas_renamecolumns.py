import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'rename' not in instance.options:
      instance.send(df)
      return

    if ';' in instance.options['rename']:
      columns = instance.options['rename'].split(';')
    else:
      columns = [instance.options['rename']]

    for column in columns:
      changes = column.split(':')
      df[changes[1]] = df[changes[0]]
      del df[changes[0]]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_renamecolumns',
  'title': 'Rename Columns',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'edit',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'rename': ''
  },
  'details': {
    'rename': {
      'input': 'text',
      'info': 'The list of <columnName:newColumnName> separates by semicolon.',
      'beautifulName': 'Columns list to rename',
      'example': 'Col1:FirstName;Col2:LastName;Col3:Age',
      'exampleExplain': 'This example will create rename the colmuns (Col1, Col2, Col3) into (FirstName, LastName, Age).'
    }
  },
  'readme': 'This component allow you to rename columns of a DataFrame',
  'install': install
}
