import pandas as pd
import traceback
import logging

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    index = payload.toIdx

    if 'dataframes' not in instance.custom:
      instance.custom['dataframes'] = {}

    if index not in instance.custom['dataframes']:
      instance.custom['dataframes'][index] = None
    instance.custom['dataframes'][index] = df

    nbReceived = len([y for y in instance.custom['dataframes'].values() if y is not None])
    instance.status('%d/2 received' % (nbReceived,))

    if nbReceived == 2:
      instance.status('Merging')
      # keysMap = {}
      # for table in instance.custom['dataframes'].values():
      #   for keys in table.keys():
      #     if keys in keysMap: 
      #       keysMap[keys] += 1
      #     else : 
      #       keysMap.setdefault(keys,  1)
      
      # keyKeepedMap = []
      # for key, value in keysMap.items():
      #   if value > 1:
      #       keyKeepedMap.append(key)

      if 'method' in instance.options:
        method = instance.options['method']
      else :
        method = 'inner'

      df = pd.merge(instance.custom['dataframes'][0], instance.custom['dataframes'][1], how=method)
      instance.send(df)

      instance.status('Resetting')
      instance.custom['dataframes'] = {}
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

  instance.status('0/2 received')

EXPORTS = {
  'id': 'pandas_joincsv',
  'title': 'Merge CSV',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': 2,
  'output': True,
  'icon': 'file-csv',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'method': 'inner',
  },
  'details': {
    'method': {
      'input': 'select',
      'info': 'The type merge we want to do.',
      'beautifulName': 'Merge type',
      'values': ['left', 'right', 'inner', 'outer']
    }
  },
  'readme': 'This component allow you to merge two dataframes to a unique one.',
  'install': install
}
