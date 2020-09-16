from zipfile import ZipFile
import traceback

def onData(instance, args):
  payload = args[0]
  df = payload.data

  if 'zipfilename' not in instance.options:
    instance.throw('No zip filename specified !')
    return

  if ';' in instance.options['filesname']:
    filesname = instance.options['filesname'].split(';')
  else:
    filesname = [instance.options['filesname']]

  
  try:
    # create a ZipFile object
    zipObj = ZipFile(instance.options['zipfilename'], 'w')

    # Add multiple files to the zip
    for filename in filesname:
      zipObj.write(filename)

    # close the Zip File
    zipObj.close()
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'zip_zipFiles',
  'title': 'Zip Files',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'icon': 'file-archive',
  'version': '1.0.0',
  'group': 'Zip',  
  'options': {
    'zipfilename' : 'my-zipFile.zip',
    'filesname': ''
  },
  'readme': """# Drop NA

  Zip Files""",
  'html': """<div class="padding">
	<div class="row">
		<div class="col-md-12">
			<div data-jc="textbox" data-jc-path="filename" data-jc-config="placeholder:/public/robots.txt">Filename</div>
			<div class="help m">Filename relative to the application root.</div>
		</div>
	</div>
</div>""",
  'install': install
}
