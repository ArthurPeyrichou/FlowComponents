import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'row' not in instance.options:
      instance.send(df)
      return

    if '\n' in instance.options['row']:
      row = instance.options['row'].split('\n')
      for row in row:
        row = row.plit(';')
    else:
      row = [instance.options['row'].split(';')]

    newRows = pd.DataFrame(row, columns=df.columns)
    df = pd.concat([newRows, df], ignore_index=True)

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_addrowq',
  'title': 'Add Row',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'plus',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'row': ''
  },
  'details': {
    'row': {
      'input': 'text',
      'info': 'Values ordered as their columns in the Dataframes separate by a semicolon',
      'beautifulName': 'Row to add',
      'example': 'aFirstName;aLastName;25',
      'exampleExplain': 'This example will add a new row in the DataFrame (FirstName;LastName,Age) with for values (aFirstName;aLastName;25).'
    }
  },
  'readme': 'This component allow you to add a new row in your DataFrame.',
  'install': install
}
