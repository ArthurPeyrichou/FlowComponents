from os.path import basename 
from zipfile import ZipFile
import traceback
import os

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

  if 'withParentFolder' in instance.options:
    withParentFolder = instance.options['withParentFolder']
  else:
    withParentFolder = False

  if 'removeFilesAfter' in instance.options:
    removeFilesAfter = instance.options['removeFilesAfter']
  else:
    removeFilesAfter = False
  
  try:
    # create a ZipFile object
    zipObj = ZipFile(instance.options['zipfilename'], 'w')

    # Add multiple files to the zip
    for filename in filesname:
      if withParentFolder:
        zipObj.write(filename)
      else:
        zipObj.write(filename, basename(filename))
      if removeFilesAfter:
        os.remove(filename)

    # close the Zip File
    zipObj.close()
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'zipFiles_createzip',
  'title': 'Create ZipFile',
  'author': 'Arthur Peyrichou',
  'color': '#B0BC00FF',
  'input': True,
  'icon': 'file-archive',
  'version': '1.2.0',
  'group': 'Zip',  
  'options': {
    'zipfilename' : 'my-zipFile.zip',
    'filesname': '',
    'withParentFolder': False,
    'removeFilesAfter': False
  },
  'details': {
    'filesname': {
      'input': 'text',
      'info': 'The list of files (path/name) to compress into zip separates by semicolon.',
      'beautifulName': 'Files list to zip'
    },
    'zipfilename': {
      'input': 'text',
      'info': 'The created zip file (path/name).',
      'beautifulName': 'Zip file name'
    },
    'withParentFolder': {
      'input': 'checkbox',
      'info': 'True if zip parent folders, false otherwise.',
      'beautifulName': 'Zip files with parent folders?'
    },
    'removeFilesAfter': {
      'input': 'checkbox',
      'info': 'True if ziped files have to be remove after, false otherwise.',
      'beautifulName': 'Remove files after zip?'
    }
   },
  'readme': 'This component allow you to compress files into a single zip file.',
  'install': install
}
