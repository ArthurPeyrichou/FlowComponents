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
  'version': '1.0.0',
  'group': 'Pandas',
  'options': {
    'columns': ''
  },
  'readme': """# Create CSV

  Create CSV dataframe (pandas)""",
  'html': """<div class="padding">
    <div class="row">
    </div>
  </div>""",
  'install': install
}
