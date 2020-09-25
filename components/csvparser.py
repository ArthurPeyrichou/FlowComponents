from io import StringIO
import pandas as pd

def onData(instance, args):
  payload = args[0]
  text = payload.data

  data = StringIO(text)

  sep = ';'
  if 'seperator' in instance.options and instance.options['seperator'] != '':
    sep = instance.options['seperator']

  treatAllAsString = True
  if 'treatAllAsString' in instance.options:
    treatAllAsString = instance.options['treatAllAsString']

  if treatAllAsString:
    df = pd.read_csv(data, sep=sep, dtype = str)
  else:
    df = pd.read_csv(data, sep=sep)

  instance.send(df)

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'csvparser',
  'title': 'CSV Parser',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'separator': ';',
    'treatAllAsString': True
  },
  'details': {
    'separator': {
      'input': 'text',
      'info': 'The separator in the file which allow to determine columns.',
      'beautifulName': 'Columns separator'
    },
    'treatAllAsString': {
      'input': 'checkbox',
      'info': 'True if the values have to be treated as string value, false otherwise',
      'beautifulName': 'Is all values string?'
    }
  },
  'readme': 'This component allow you to parse a string into a DataFrame. You can define the separator and if all values should be treated as string or not.',
  'install': install
}
