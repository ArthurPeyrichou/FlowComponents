import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'rename' not in instance.options:
      instance.send(df)
      return

    if ';' in instance.options['rename']:
      columns = instance.options['rename'].split(';')
    else:
      columns = [instance.options['rename']]

    for column in columns:
      changes = column.split(':')
      df[changes[1]] = df[changes[0]]
      del df[changes[0]]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_renamecolumns',
  'title': 'Rename Columns',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'edit',
  'version': '1.0.0',
  'group': 'Pandas',
  'options': {
    'rename': ''
  },
  'readme': """# Rename Column

  Rename Columns of a DataFrame""",
  'html': """<div class="padding">
  <div class="row">
    <div class="col-md-6">
    </div>
  </div>
</div>""",
  'install': install
}
