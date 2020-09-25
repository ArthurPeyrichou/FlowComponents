import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'sort' not in instance.options:
      instance.send(df)
      return
    
    if ';' in instance.options['sort']:
      options = instance.options['sort'].split(';')
    else:
      options = [instance.options['sort']]
    sortingColumns = []
    sortingOrder = []
    toRemove = []

    for opt in options:
      if ',' not in opt:
        tmp = [opt, 'asc']
      else:
        tmp = opt.split(',')
      
      sortingColumns.append(tmp[0] + '.Lower')
      if tmp[1].lower() == 'asc':
        sortingOrder.append(True)
      else:
        sortingOrder.append(False)

      df[tmp[0] + '.Lower'] = df[tmp[0]].str.lower()
      toRemove.append(tmp[0] + '.Lower')

    if 'debug' in instance.options and instance.options['debug']:
      instance.debug('%s - %s' % (sortingColumns, sortingOrder))
    df = df.sort_values(by=sortingColumns, ascending=sortingOrder, na_position='first')
    
    for r in toRemove:
      del df[r]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_sort',
  'title': 'Sort Dataframe',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'sort': ''
  },
  'details': {
    'sort': {
      'input': 'text',
      'info': 'The list of columns to sort separate by semicolon (Method asc).',
      'beautifulName': 'Columns list to sort'
    }
   },
  'readme': 'This component allow you to sort a Dataframe',
  'install': install
}
