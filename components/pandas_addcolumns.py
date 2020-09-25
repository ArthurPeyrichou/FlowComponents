import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'columns' not in instance.options:
      instance.send(df)
      return

    if ';' in instance.options['columns']:
      columns = instance.options['columns'].split(';')
    else:
      columns = [instance.options['columns']]

    for column in columns:
      newColumns = column.split(':')
      if len(newColumns) == 1:
        df[newColumns[0]] = None
      elif len(newColumns) == 2:
        if newColumns[1].isnumeric():
          if '.' in newColumns[1]:
            df[newColumns[0]] = float(newColumns[1])
          else:
            df[newColumns[0]] = int(newColumns[1])
        else:
          df[newColumns[0]] = newColumns[1]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_addcolumns',
  'title': 'Add Columns',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'plus',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'columns': ''
  },
  'details': {
    'columns': {
      'input': 'text',
      'info': 'The list of columns to add separate by semicolon. If the column have a default value, add \':\' and the default value after the column name.',
      'beautifulName': 'New columns list to add',
      'example': 'Col1:3;Col2;Col3:aString',
      'exampleExplain': 'This example will create a 3 new columns, the Col1 with for default value 3. The Col2 with no default value so by default it will be None (null). And the Col3 with for default value \'aString\'.'
    }
  },
  'readme': 'This component allow you to add a new column in your DataFrame. You can add a default value, otherwise it will be None (\'null\').',
  'install': install
}
