import pandas as pd
import traceback
import math

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

    for column in columns:
      filterPattern = column.split(':') #0 for the column name and 1 for the pattern
      if len(filterPattern) == 1:
        df = df[pd.isnull(df[filterPattern[0]])]
      elif filterPattern[1] == '!':
        df = df[pd.notnull(df[filterPattern[0]])]
      else:
        if filterPattern[1][0] == '!':
          df = df[df[filterPattern[0]]!=filterPattern[1]]
        else:
          df = df[df[filterPattern[0]]==filterPattern[1]]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_filterrows',
  'title': 'Filter Rows',
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
      'info': 'The list of <column:value> separates by semicolon.',
      'beautifulName': 'Columns list',
      'example': 'Col1:3;Col2:!5;Col3;Col4:!',
      'exampleExplain': 'This example will filter rows on 4 conditions: the Col1\'s value have to be equal to 3, the Col2\'s value have to be not equal to 5, the Col3\'s value have to be None (null), and finally the Col4\'s value have to be not None (not null).'
    }
  },
  'readme': 'This component allow you to filter rows of a DataFrame.',
  'install': install
}
