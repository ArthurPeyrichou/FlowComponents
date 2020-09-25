import pandas as pd
import traceback
import random
import numpy

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data
    keyList = []

    if 'columnName' not in instance.options or 'basedColumns' not in instance.options:
      instance.send(df)
      return

    columns = instance.options['basedColumns'].split(';')
    df[instance.options['columnName']] = df.apply(lambda x: columnsfusioner(x, columns, instance.options['separator']), axis=1)
    

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def columnsfusioner(x, basedColumns, separator):
  res = ''
  for column in basedColumns:
    if res != '':
      res += ''.join([res, str(separator), str(x[column])]) 
    else :
      res = ''.join([res, str(x[column])]) 
  return res

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_columnsfusioner',
  'title': 'Columns fusioner',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'columnName': '',
    'basedColumns' : '',
    'separator': '-'
  },
  'details': {
    'columnName': {
      'input': 'text',
      'info': 'The name of the new column.',
      'beautifulName': 'New column name'
    },
    'basedColumns': {
      'input': 'text',
      'info': 'The list of columns to fusion separates by semicolon.',
      'beautifulName': 'Column to fusion'
    },
    'separator': {
      'input': 'text',
      'info': 'The separator string between each column fusionned (can be empty).',
      'beautifulName': 'Columns separator'
    }
  },
  'readme': 'This component allow you to fusionning columns in one new columns (keeping the fusionned columns).',
  'install': install
}
