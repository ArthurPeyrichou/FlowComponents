import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'columnName' not in instance.options:
      return
    
    res = 0
    count = 0
    distinctList = []
    
    if 'pattern' not in instance.options :
      pattern = 'SUM'
    else: 
      pattern = instance.options['pattern']

    for index, row in df.iterrows():
      if instance.options['columnBasedDistinct'] == '' or row[instance.options['columnBasedDistinct']] not in distinctList:
        if type(row[instance.options['columnName']]) is str:
          res = stats(res, float(row[instance.options['columnName']].replace(',','.')), pattern)
          count += 1
        elif pd.notnull(row[instance.options['columnName']]):
          res = stats(res, row[instance.options['columnName']], pattern)
          count += 1
      if instance.options['columnBasedDistinct'] != '':
        distinctList.append(row[instance.options['columnBasedDistinct']])
  
    if pattern == 'MOY':
      res /= count

    instance.send(res)

  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def stats(res, value, pattern):
  if pattern == 'SUM' or pattern == 'MOY':
    res += value
  elif pattern == 'MIN':
    if res > value:
      res = value
  elif pattern == 'MAX':
    if res < value:
      res = value
  return res

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'addcolumnstat',
  'title': 'Add Column Stat',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'chart-bar',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'columnName': '',
    'pattern': 'SUM',
    'columnBasedDistinct':''
  },
  'details': {
    'columnName': {
      'input': 'text',
      'info': 'The name of the column where the stats are processed.',
      'beautifulName': 'Studied column name'
    },
    'pattern': {
      'input': 'select',
      'info': 'The pattern of calcul, you can use SUM, MOY, MAX, MIN',
      'beautifulName': 'Calcul pattern',
      'values': ['SUM', 'MOY', 'MAX', 'MIN'],
      'example': 'SUM',
      'exampleExplain': 'This example will give the sum of all the values in the studied column.'
    },
    'columnBasedDistinct': {
      'input': 'text',
      'info': 'True if in the rows, a column have to be treated as distinct. False otherwise',
      'beautifulName': 'Have a column distinct for studies?'
    }
  },
  'readme': 'This component allow you to make an operation on all the values of a targeted DataFrame\'s column. It will send the result of the calcul.',
  'install': install
}
