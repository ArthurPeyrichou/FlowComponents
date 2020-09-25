import pandas as pd
import traceback
import random
import numpy

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data
    keyList = []

    if 'keyName' not in instance.options:
      instance.send(df)
      return

    if instance.options['basedColumn'] in df:
      df[instance.options['keyName']] = df.apply(lambda x: str(x[instance.options['basedColumn']]) + '-' + genKey(keyList, instance.options['keyType'], int(instance.options['keySize'])), axis=1)
    else:
      df[instance.options['keyName']] = df.apply(lambda x: genKey(keyList, instance.options['keyType'], int(instance.options['keySize'])), axis=1)

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def genKey(keyList, keyType, size):
  res = ''
  if keyType == 'alpha':
    res = randomAlphaString(size)
    while res in keyList:
      res = randomAlphaString(size)
  elif keyType == 'alphanum':
    res = (size)
    while res in keyList:
      res = randomAlphaNumString(size)
  else :
    res = randomNumString(size)
    while res in keyList:
      res = randomNumString(size)
  keyList.insert(len(keyList), res)
  return res

def randomAlphaString(size):
  res = ''
  chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
  i = 0
  while (i < size):
      res += chars[random.randint(0, len(chars)-1)]
      i +=1
  return res

def randomAlphaNumString(size):
  res = ''
  chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  i = 0
  while (i < size):
      res += chars[random.randint(0, len(chars)-1)]
      i +=1
  return res

def randomNumString(size):
  res = ''
  i = 0
  while (i < size):
      res += str(random.randint(0,9))
      i +=1
  return res

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_genKey',
  'title': 'Generate Key',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'key',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'keyName': 'id',
    'basedColumn' : '',
    'keyType': 'numerical',
    'keySize': '10'
  },
  'details': {
    'keyName': {
      'input': 'text',
      'info': 'The name of the new column.',
      'beautifulName': 'New column name'
    },
    'basedColumn': {
      'input': 'text',
      'info': 'The column to use to generate the key (can be empty).',
      'beautifulName': 'Based column name'
    },
    'keyType': {
      'input': 'select',
      'info': 'The type of key we want to generate.',
      'beautifulName': 'Key type',
      'value': ['numerical', 'alpha', 'alphanum']
    },
    'keySize': {
      'input': 'number',
      'info': 'The size of the key we want to generate (without counting on the based-column size).',
      'beautifulName': 'Size of the generate key'
    }
  },
  'readme': 'This component allow you to generate a key column in a DataFrame',
  'install': install
}
