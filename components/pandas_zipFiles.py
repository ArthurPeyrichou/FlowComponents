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
  'version': '1.2.0',
  'group': 'Zip',  
  'options': {
    'zipfilename' : 'my-zipFile.zip',
    'filesname': ''
  },
  'details': {
    'filesname': {
      'input': 'text',
      'info': 'The list of files (path/name) to compress into zip separates by semicolon.',
      'beautifulName': 'Columns list to zip'
    },
    'zipfilename': {
      'input': 'text',
      'info': 'The created zip file (path/name).',
      'beautifulName': 'Zip file name'
    }
   },
  'readme': 'This component allow you to compress files into a single zip file.',
  'install': install
}
