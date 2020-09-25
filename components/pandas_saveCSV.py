import pandas as pd
import traceback

def onData(instance, args):
  payload = args[0]
  df = payload.data

  if 'filename' not in instance.options:
    instance.throw('No filename specified !')
    return
  
  sep = ';'
  if 'seperator' in instance.options and instance.options['seperator'] != '':
    sep = instance.options['seperator']
  
  try:
    df.to_csv(instance.options['filename'], sep=sep, index=None, header=True)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_savecsv',
  'title': 'Save CSV',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'icon': 'file-csv',
  'version': '1.2.0',
  'group': 'Pandas',  
  'options': {
    'filename': '',
    'separator': ';'
  },
  'details': {
    'separator': {
      'input': 'text',
      'info': 'The separator in the file which allow to determine columns.',
      'beautifulName': 'Columns separator'
    },
    'filename': {
      'input': 'text',
      'info': 'The path that should be used to save the new file.',
      'beautifulName': 'File path/name'
    }
   },
  'readme': 'This component allow you to save a DataFrame into a csv file.',
  'install': install
}
