import pandas as pd
import traceback

class Node:
  def __init__(self, leftNode, rightNode, operator):
    self.left = leftNode
    self.right = rightNode
    self.operator = operator

  def setLeft(self, leftNode):
    self.left = leftNode

  def setLeft(self, rightNode):
    self.right = rightNode
  
  def setOperator(self, operator):
    self.operator = operator

  def compute(self, x):
    left = 0
    right = 0
    if type(self.left) is Node:
      left = self.left.compute(x)
    elif self.left in x:
      left = x[self.left]
    else:
      left = self.left
    if type(self.right) is Node:
      right = self.right.compute(x)
    elif self.right in x:
      right = x[self.right]
    else:
      right = self.right

    if type(left) is str:
      left = float(left.replace(',','.'))
    if type(right) is str:
      right = float(right.replace(',','.'))
    if self.operator == 'PLUS':
      return left + right
    elif self.operator == 'MINUS':
      return left - right
    elif self.operator == 'MULT':
      return left * right
    elif self.operator == 'DIV' and right != 0:
      return left / right
    else:
      return 0

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'columnName' not in instance.options or 'calculatedValue' not in instance.options:
      instance.send(df)
      return
    myTree = stringToTree(instance.options['calculatedValue'])
    df[instance.options['columnName']] = df.apply(lambda x: myTree.compute(x), axis=1)
    
    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def stringToTree(pattern):
  parenthese = 0
  operator = ''
  start = -1
  separator = -1
  end = -1
  i = 0
  while i < len(pattern):
    if pattern[i] == '(':
      parenthese += 1
      if start == -1:
        start = i
    
    if pattern[i] == ',' and parenthese == 1:
      if separator == -1:
        separator = i

    elif pattern[i] == ')':
      parenthese -= 1

    if parenthese == 0:
      if start != -1 and end == -1:
        end = i
        break
      operator+= pattern[i]
    i += 1
    
  if operator != 'PLUS' and operator != 'MINUS' and operator != 'MULT' and operator != 'DIV':
    raise Exception('Operator unknonw (Should be PLUS, MINUS, MULT or DIV). Got: ' + operator + '. In pattern :' + pattern[start:end])

  left = pattern[(start+1):separator]
  right = pattern[(separator+1):end]

  if '(' in left:
    left = stringToTree(pattern[start:separator])
  
  if '(' in right:
    right = stringToTree(pattern[(separator+1):end])

  return Node(left, right, operator)


def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'addcalculatecolumn',
  'title': 'Add Calculate Column',
  'author': 'Arthur Peyrichou',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'chart-bar',
  'version': '1.2.0',
  'group': 'Pandas',
  'options': {
    'columnName': '',
    'calculatedValue': ''
  },
  'details': {
    'columnName': {
      'input': 'text',
      'info': 'The name of the new column.',
      'beautifulName': 'New column name'
    },
    'calculatedValue': {
      'input': 'text',
      'info': 'The operation to execute in order to calculate the new column value.',
      'beautifulName': 'Calculated value',
      'example': 'MULT(PLUS(Col1,Col2),Col3)',
      'exampleExplain': 'This example will create a new column, his value will be (Col1 + Col2) * Col3. You can use PLUS(), MINUS(), MULT() and DIV().'
    }
  },
  'readme': 'This component allow you to add a new column in your DataFrame, the value is calculated with existing columns values.',
  'install': install
}
