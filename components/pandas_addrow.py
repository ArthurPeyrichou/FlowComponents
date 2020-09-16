import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'rows' not in instance.options:
      instance.send(df)
      return

    if '\n' in instance.options['rows']:
      rows = instance.options['rows'].split('\n')
      for row in rows:
        row = row.plit(';')
    else:
      rows = [instance.options['rows'].split(';')]

    newRows = pd.DataFrame(rows, columns=df.columns)
    df = pd.concat([newRows, df], ignore_index=True)

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_addrowq',
  'title': 'Add Row',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'plus',
  'version': '1.0.0',
  'group': 'Pandas',
  'options': {
    'rows': ''
  },
  'readme': """# Add Rowq

  Add Rowq in a DataFrame""",
  'html': """<div class="padding">
  <div class="row">
    <div class="col-md-6">
    </div>
  </div>
</div>""",
  'install': install
}
