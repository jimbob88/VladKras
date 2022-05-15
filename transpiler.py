from collections import OrderedDict
import ete3
import pprint

input_tokens = [('STATEMENT', 0, 'sub'),
 ('VARIABLE', 4, 'other'),
 ('START_BLOCK', 10, '{'),
 ('FUNCTION', 17, 'printAt'),
 ('ARGUMENTS_START', 24, '('),
 ('INT', 25, 6),
 ('ARGUMENTS_SEP', 26, ','),
 ('INT', 28, 1),
 ('ARGUMENTS_SEP', 29, ','),
 ('STRING', 31, 'I love programming'),
 ('ARGUMENTS_END', 51, ')'),
 ('END_LINE', 52, ';'),
 ('END_BLOCK', 54, '}'),
 ('STATEMENT', 57, 'sub'),
 ('VARIABLE', 61, 'main'),
 ('START_BLOCK', 66, '{'),
 ('FUNCTION', 72, 'clearScreen'),
 ('ARGUMENTS_START', 83, '('),
 ('ARGUMENTS_END', 84, ')'),
 ('END_LINE', 85, ';'),
 ('FUNCTION', 91, 'enableCursor'),
 ('ARGUMENTS_START', 103, '('),
 ('ARGUMENTS_END', 104, ')'),
 ('END_LINE', 105, ';'),
 ('FUNCTION', 111, 'disableCursor'),
 ('ARGUMENTS_START', 124, '('),
 ('ARGUMENTS_END', 125, ')'),
 ('END_LINE', 126, ';'),
 ('FUNCTION', 132, 'printAt'),
 ('ARGUMENTS_START', 139, '('),
 ('INT', 140, 1),
 ('ARGUMENTS_SEP', 141, ','),
 ('INT', 143, 2),
 ('ARGUMENTS_SEP', 144, ','),
 ('STRING', 146, 'Hello World'),
 ('ARGUMENTS_END', 159, ')'),
 ('END_LINE', 160, ';'),
 ('FUNCTION', 166, 'resetCursor'),
 ('ARGUMENTS_START', 177, '('),
 ('ARGUMENTS_END', 178, ')'),
 ('END_LINE', 179, ';'),
 ('STATEMENT', 185, 'var'),
 ('VARIABLE', 189, 'name$'),
 ('ASSIGN', 195, '='),
 ('STRING', 197, 'James'),
 ('END_LINE', 204, ';'),
 ('STATEMENT', 210, 'var'),
 ('VARIABLE', 214, 'lastName$'),
 ('ASSIGN', 224, '='),
 ('FUNCTION', 226, 'askInput'),
 ('ARGUMENTS_START', 234, '('),
 ('STRING', 235, 'What is your last name? '),
 ('ARGUMENTS_END', 261, ')'),
 ('END_LINE', 262, ';'),
 ('STATEMENT', 268, 'var'),
 ('VARIABLE', 272, 'fl'),
 ('ASSIGN', 275, '='),
 ('INT', 277, 1),
 ('INT', 279, 0),
 ('END_LINE', 280, ';'),
 ('STATEMENT', 286, 'var'),
 ('VARIABLE', 290, 'i'),
 ('ASSIGN', 292, '='),
 ('INT', 294, 0),
 ('END_LINE', 295, ';'),
 ('FUNCTION', 301, 'Print'),
 ('ARGUMENTS_START', 306, '('),
 ('STRING', 307, 'Hello '),
 ('PLUS', 316, '+'),
 ('VARIABLE', 318, 'name'),
 ('PLUS', 323, '+'),
 ('VARIABLE', 325, 'lastName$'),
 ('ARGUMENTS_END', 334, ')'),
 ('END_LINE', 335, ';'),
 ('STATEMENT', 342, 'var'),
 ('VARIABLE', 346, 'j'),
 ('ASSIGN', 348, '='),
 ('INT', 350, 0),
 ('END_LINE', 351, ';'),
 ('STATEMENT', 357, 'for'),
 ('ARGUMENTS_START', 360, '('),
 ('VARIABLE', 361, 'j'),
 ('ASSIGN', 363, '='),
 ('INT', 365, 0),
 ('ARGUMENTS_SEP', 366, ','),
 ('CONDITION_WRAPPER', 368, '|'),
 ('VARIABLE', 369, 'j'),
 ('INT', 373, 1),
 ('INT', 374, 9),
 ('CONDITION_WRAPPER', 375, '|'),
 ('ARGUMENTS_SEP', 376, ','),
 ('VARIABLE', 378, 'j'),
 ('PLUS_ONE', 379, '++'),
 ('ARGUMENTS_END', 381, ')'),
 ('START_BLOCK', 383, '{'),
 ('FUNCTION', 393, 'Print'),
 ('ARGUMENTS_START', 398, '('),
 ('VARIABLE', 399, 'j'),
 ('ARGUMENTS_END', 400, ')'),
 ('END_LINE', 401, ';'),
 ('END_BLOCK', 407, '}'),
 ('STATEMENT', 414, 'while'),
 ('CONDITION_WRAPPER', 420, '|'),
 ('BOOLEAN', 421, 'true'),
 ('CONDITION_WRAPPER', 425, '|'),
 ('START_BLOCK', 427, '{'),
 ('STATEMENT', 437, 'if'),
 ('CONDITION_WRAPPER', 440, '|'),
 ('VARIABLE', 441, 'i'),
 ('COMPARISON', 443, '=='),
 ('INT', 446, 0),
 ('CONDITION_WRAPPER', 447, '|'),
 ('START_BLOCK', 449, '{'),
 ('FUNCTION', 463, 'Print'),
 ('ARGUMENTS_START', 468, '('),
 ('STRING', 469, 'Hello'),
 ('ARGUMENTS_END', 476, ')'),
 ('END_LINE', 477, ';'),
 ('VARIABLE', 491, 'i'),
 ('PLUS_EQUALS', 493, '+='),
 ('PLUS', 495, '+'),
 ('INT', 496, 1),
 ('END_LINE', 497, ';'),
 ('END_BLOCK', 507, '}'),
 ('VARIABLE', 509, 'else'),
 ('START_BLOCK', 514, '{'),
 ('FUNCTION', 528, 'Print'),
 ('ARGUMENTS_START', 533, '('),
 ('STRING', 534, 'No'),
 ('ARGUMENTS_END', 538, ')'),
 ('END_LINE', 539, ';'),
 ('VARIABLE', 553, 'i'),
 ('MINUS_EQUALS', 555, '-='),
 ('MINUS', 557, '-'),
 ('INT', 558, 1),
 ('END_LINE', 559, ';'),
 ('END_BLOCK', 569, '}'),
 ('VARIABLE', 579, 'break'),
 ('END_LINE', 584, ';'),
 ('END_BLOCK', 590, '}'),
 ('STATEMENT', 596, 'call'),
 ('VARIABLE', 601, 'other'),
 ('END_LINE', 606, ';'),
 ('END_BLOCK', 608, '}')]


class tokenType:
    def __init__(self, tupe):
        self.tupe = tupe
        self.tokenType = tupe[0]
        self.tokenPos = tupe[1]
        self.tokenVal = tupe[2]

class Node:
    def __init__(self, uNode=None, t: tokenType=None) -> None:
        self.connectedLowerNodes = []
        self.connectedUpperNode = uNode
        self.tokenDetails = t

    def connectNode(self, n) -> None:
        self.connectedLowerNodes.append(n)

class Tree:
    def __init__(self) -> None:
        self.nullNode = Node()
        self.currentNode = self.nullNode

    def addNode(self, n) -> None:
        self.currentNode.connectNode(n)
        self.currentNode = n

    def connectToken(self, t) -> None:
        tempNode = Node(uNode=self.currentNode, t=t)
        self.currentNode.connectNode(tempNode)
        self.currentNode = tempNode

    def decreaseDepth(self):
        if self.currentNode.connectedUpperNode is not None:
            self.currentNode = self.currentNode.connectedUpperNode
        else:
            raise SyntaxError("It looks like there is an indentation issue")


def treeify(tokens: list) -> Tree:
    # Tree based off subroutines
    classed_tokens = []
    for token in tokens:
        classed_tokens.append(tokenType(token))

    # tree = OrderedDict()
    tree = Tree()
    token_idx = 0
    current_sub = 'NA'
    while True:
        if classed_tokens[token_idx].tokenVal == 'sub':
            if classed_tokens[token_idx+1].tokenType != 'VARIABLE':
                raise ValueError("Subroutine has no name")
            else:
                subName = classed_tokens[token_idx+1].tokenVal
                tree.connectToken(t=tokenType(("DEF_SUB", token_idx, subName)))
                token_idx += 2
        elif classed_tokens[token_idx].tokenType == 'START_BLOCK':
            token_idx += 1
        elif classed_tokens[token_idx].tokenType == 'END_BLOCK':
            tree.decreaseDepth()
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'while':
            if classed_tokens[token_idx+1].tokenType == 'CONDITION_WRAPPER':
                tree.connectToken(t=classed_tokens[token_idx])
            else:
                raise SyntaxError("While loop is not followed by condition wrapper '|'")
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'if':
            if classed_tokens[token_idx+1].tokenType == 'CONDITION_WRAPPER':
                tree.connectToken(t=classed_tokens[token_idx])
            else:
                raise SyntaxError("If statement is not followed by condition wrapper '|'")
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'else':
            tree.connectToken(t=classed_tokens[token_idx])
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'for':
            if classed_tokens[token_idx+1].tokenType == 'ARGUMENTS_START':
                tree.connectToken(t=classed_tokens[token_idx])
            else:
                raise SyntaxError("For loop has no parameters")
            token_idx += 1
        elif classed_tokens[token_idx].tokenType == 'CONDITION_WRAPPER':
            if tree.currentNode.tokenDetails.tokenType == 'CONDITION_WRAPPER':
                # If it is the terminating position
                tree.decreaseDepth()
            else:
                tree.connectToken(t=classed_tokens[token_idx])
            token_idx += 1
        else:
            tree.connectToken(t=classed_tokens[token_idx])
            tree.decreaseDepth()
            token_idx += 1
        
        print(token_idx, tree)

        if token_idx >= len(tokens):
            break

    return tree

def toNewick(l):
  t_tuple = []
  for idx, node in enumerate(l):
    if len(node.connectedLowerNodes) > 0:
      t_tuple.append([node.tokenDetails.tokenType, toNewick(node.connectedLowerNodes)])
    else:
      t_tuple.append(node.tokenDetails.tokenType)
  return str(t_tuple).replace('[', '(').replace(']', ')').replace("'", "").replace(' ', '') #tuple(tuple(sub) for sub in t_tuple)

def toList(l):
  tList = []
  for idx, node in enumerate(l):
    if len(node.connectedLowerNodes) > 0:
      tList.append([node.tokenDetails, toList(node.connectedLowerNodes)])
    else:
      tList.append(node.tokenDetails)
  return tList

def transpile(tree: Tree):
    print(tree)
    code = [
        "GOSUB main",
        "escape$=CHR$(27)",
        'clear$=escape$+"E"',
        'home$=escape$+"H"',
        'move$=escape$+"Y"'
    ]
    treeList = toList(tree.currentNode.connectedLowerNodes)
    for subroutine in treeList:
        print(subroutine[0].tokenVal)
        code.append("REM " + subroutine[0].tokenVal)
        code.append("'")
        # for token in subroutine[1]:
        tokenIdx = 0
        while True:
            token = subroutine[1][tokenIdx]
            print(token, token.tokenType, token.tokenVal)
            if type(token) != list:
                if code[-1] == "'":
                    code.append('')
                if token.tokenVal == 'printAt':
                    print("PRINTAT")
                    endLine = [i for i, n in enumerate(subroutine[1][tokenIdx:]) if n.tokenType == 'END_LINE'][0]
                    for i in range(tokenIdx, endLine):
                        print(subroutine[1][i].tokenVal)
                    break    
        break
    pprint.pprint(code)






if __name__ == '__main__':
    # Create tree from tokens
    t = treeify(tokens=input_tokens)

    # Print tree
    newickString = toNewick(t.currentNode.connectedLowerNodes) + ";"
    newickTree = ete3.Tree(newickString)
    print(newickTree)

    # Create png of tree
    ts = ete3.TreeStyle()
    ts.show_leaf_name = True
    ts.scale = 20
    ts.rotation = 90
    newickTree.render("Tree.png", w=1830, units="mm", tree_style=ts)

    transpile(t)