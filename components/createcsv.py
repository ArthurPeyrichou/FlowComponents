from io import StringIO
import pandas as pd

def onData(instance, args):
  if 'columns' not in instance.options:
      instance.send(pd.DataFrame())
      return

  if ';' in instance.options['columns']:
    columns = instance.options['columns'].split(';')
  else:
    columns = [instance.options['columns']]
  
  
  df = pd.DataFrame(columns = columns)

  instance.send(df)


def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'csvcreate',
  'title': 'Create CSV',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'columns': ''
  },
  'details': {
    'columns': {
      'input': 'text',
      'info': 'The list of columns in your Dataframe, separates by semicolon.',
      'beautifulName': 'Columns of the DataFrame',
      'example': 'Col1;Col2;Col3',
      'exampleExplain': 'This example will create a Datafram with three columns (Col1, Col2, Col3).'
    }
  },
  'readme': 'This component allow you to create an empty DataFrame with defined columns.',
  'install': install
}
