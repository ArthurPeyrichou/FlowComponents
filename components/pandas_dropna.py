import pandas as pd
import traceback

def onData(instance, args):
  payload = args[0]
  df = payload.data

  if 'columns' not in instance.options:
    instance.throw('No columns specified !')
    return
  
  try:
    columns = instance.options['columns'].split(';')

    df = df.dropna(subset=columns)

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_dropna',
  'title': 'Drop NA',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.2.0',
  'group': 'Pandas',
  'readme': 'This component allow you to drop all rows containing NaN in a specified column.',
  'install': install
}
