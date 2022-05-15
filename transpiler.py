from collections import OrderedDict
import ete3

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
 ('VARIABLE', 189, 'name'),
 ('ASSIGN', 194, '='),
 ('STRING', 196, 'James'),
 ('END_LINE', 203, ';'),
 ('STATEMENT', 209, 'var'),
 ('VARIABLE', 213, 'lastName'),
 ('ASSIGN', 222, '='),
 ('FUNCTION', 224, 'askInput'),
 ('ARGUMENTS_START', 232, '('),
 ('STRING', 233, 'What is your last name? '),
 ('ARGUMENTS_END', 259, ')'),
 ('END_LINE', 260, ';'),
 ('STATEMENT', 266, 'var'),
 ('VARIABLE', 270, 'fl'),
 ('ASSIGN', 273, '='),
 ('INT', 275, 1),
 ('INT', 277, 0),
 ('END_LINE', 278, ';'),
 ('STATEMENT', 284, 'var'),
 ('VARIABLE', 288, 'i'),
 ('ASSIGN', 290, '='),
 ('INT', 292, 0),
 ('END_LINE', 293, ';'),
 ('FUNCTION', 299, 'Print'),
 ('ARGUMENTS_START', 304, '('),
 ('STRING', 305, 'Hello '),
 ('PLUS', 314, '+'),
 ('VARIABLE', 316, 'name'),
 ('PLUS', 321, '+'),
 ('VARIABLE', 323, 'lastName'),
 ('ARGUMENTS_END', 331, ')'),
 ('END_LINE', 332, ';'),
 ('STATEMENT', 339, 'var'),
 ('VARIABLE', 343, 'j'),
 ('ASSIGN', 345, '='),
 ('INT', 347, 0),
 ('END_LINE', 348, ';'),
 ('STATEMENT', 354, 'for'),
 ('ARGUMENTS_START', 357, '('),
 ('VARIABLE', 358, 'j'),
 ('ASSIGN', 360, '='),
 ('INT', 362, 0),
 ('ARGUMENTS_SEP', 363, ','),
 ('CONDITION_WRAPPER', 365, '|'),
 ('VARIABLE', 366, 'j'),
 ('INT', 370, 1),
 ('INT', 371, 9),
 ('CONDITION_WRAPPER', 372, '|'),
 ('ARGUMENTS_SEP', 373, ','),
 ('VARIABLE', 375, 'j'),
 ('PLUS_ONE', 376, '++'),
 ('ARGUMENTS_END', 378, ')'),
 ('START_BLOCK', 380, '{'),
 ('FUNCTION', 390, 'Print'),
 ('ARGUMENTS_START', 395, '('),
 ('VARIABLE', 396, 'j'),
 ('ARGUMENTS_END', 397, ')'),
 ('END_LINE', 398, ';'),
 ('END_BLOCK', 404, '}'),
 ('STATEMENT', 411, 'while'),
 ('CONDITION_WRAPPER', 417, '|'),
 ('BOOLEAN', 418, 'true'),
 ('CONDITION_WRAPPER', 422, '|'),
 ('START_BLOCK', 424, '{'),
 ('STATEMENT', 434, 'if'),
 ('CONDITION_WRAPPER', 437, '|'),
 ('VARIABLE', 438, 'i'),
 ('COMPARISON', 440, '=='),
 ('INT', 443, 0),
 ('CONDITION_WRAPPER', 444, '|'),
 ('START_BLOCK', 446, '{'),
 ('FUNCTION', 460, 'Print'),
 ('ARGUMENTS_START', 465, '('),
 ('STRING', 466, 'Hello'),
 ('ARGUMENTS_END', 473, ')'),
 ('END_LINE', 474, ';'),
 ('VARIABLE', 488, 'i'),
 ('PLUS_EQUALS', 490, '+='),
 ('PLUS', 492, '+'),
 ('INT', 493, 1),
 ('END_LINE', 494, ';'),
 ('END_BLOCK', 504, '}'),
 ('VARIABLE', 506, 'else'),
 ('START_BLOCK', 511, '{'),
 ('FUNCTION', 525, 'Print'),
 ('ARGUMENTS_START', 530, '('),
 ('STRING', 531, 'No'),
 ('ARGUMENTS_END', 535, ')'),
 ('END_LINE', 536, ';'),
 ('VARIABLE', 550, 'i'),
 ('MINUS_EQUALS', 552, '-='),
 ('MINUS', 554, '-'),
 ('INT', 555, 1),
 ('END_LINE', 556, ';'),
 ('END_BLOCK', 566, '}'),
 ('VARIABLE', 576, 'break'),
 ('END_LINE', 581, ';'),
 ('END_BLOCK', 587, '}'),
 ('STATEMENT', 593, 'call'),
 ('VARIABLE', 598, 'other'),
 ('END_LINE', 603, ';'),
 ('END_BLOCK', 605, '}')]


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


def treeify(tokens):
    # Tree based off subroutines
    classed_tokens = []
    for token in tokens:
        classed_tokens.append(tokenType(token))

    # tree = OrderedDict()
    tree = Tree()
    token_idx = 0
    current_sub = 'NA'
    depth = 0
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
        
        print(token_idx, depth, tree)

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

