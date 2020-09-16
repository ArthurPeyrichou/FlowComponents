import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'columns' not in instance.options:
      instance.send(df)
      return

    if ';' in instance.options['columns']:
      columns = instance.options['columns'].split(';')
    else:
      columns = [instance.options['columns']]

    for column in columns:
      newColumns = column.split(':')
      if len(newColumns) == 1:
        df[newColumns[0]] = None
      elif len(newColumns) == 2:
        if newColumns[1].isnumeric():
          if '.' in newColumns[1]:
            df[newColumns[0]] = float(newColumns[1])
          else:
            df[newColumns[0]] = int(newColumns[1])
        else:
          df[newColumns[0]] = newColumns[1]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_addcolumns',
  'title': 'Add Columns',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'plus',
  'version': '1.0.0',
  'group': 'Pandas',
  'options': {
    'columns': ''
  },
  'readme': """# Add Column

  Add Columns in a DataFrame""",
  'html': """<div class="padding">
  <div class="row">
    <div class="col-md-6">
    </div>
  </div>
</div>""",
  'install': install
}
