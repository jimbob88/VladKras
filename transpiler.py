from collections import OrderedDict
from re import L
import ete3
import pprint
import itertools

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
 ('FLOAT', 277, 1.0),
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
 ('VARIABLE', 318, 'name$'),
 ('PLUS', 324, '+'),
 ('VARIABLE', 326, 'lastName$'),
 ('ARGUMENTS_END', 335, ')'),
 ('END_LINE', 336, ';'),
 ('STATEMENT', 343, 'var'),
 ('VARIABLE', 347, 'j'),
 ('ASSIGN', 349, '='),
 ('INT', 351, 0),
 ('END_LINE', 352, ';'),
 ('STATEMENT', 358, 'for'),
 ('ARGUMENTS_START', 361, '('),
 ('VARIABLE', 362, 'j'),
 ('ASSIGN', 364, '='),
 ('INT', 366, 0),
 ('ARGUMENTS_SEP', 367, ','),
 ('CONDITION_WRAPPER', 369, '|'),
 ('VARIABLE', 370, 'j'),
 ('LESS_THAN', 372, '<'),
 ('INT', 374, 19),
 ('CONDITION_WRAPPER', 376, '|'),
 ('ARGUMENTS_SEP', 377, ','),
 ('VARIABLE', 379, 'j'),
 ('PLUS_ONE', 380, '++'),
 ('ARGUMENTS_END', 382, ')'),
 ('START_BLOCK', 384, '{'),
 ('FUNCTION', 394, 'Print'),
 ('ARGUMENTS_START', 399, '('),
 ('VARIABLE', 400, 'j'),
 ('ARGUMENTS_END', 401, ')'),
 ('END_LINE', 402, ';'),
 ('END_BLOCK', 408, '}'),
 ('STATEMENT', 415, 'while'),
 ('CONDITION_WRAPPER', 421, '|'),
 ('BOOLEAN', 422, 'true'),
 ('CONDITION_WRAPPER', 426, '|'),
 ('START_BLOCK', 428, '{'),
 ('STATEMENT', 438, 'if'),
 ('CONDITION_WRAPPER', 441, '|'),
 ('VARIABLE', 442, 'i'),
 ('COMPARISON', 444, '=='),
 ('INT', 447, 0),
 ('CONDITION_WRAPPER', 448, '|'),
 ('START_BLOCK', 450, '{'),
 ('FUNCTION', 464, 'Print'),
 ('ARGUMENTS_START', 469, '('),
 ('STRING', 470, 'Hello'),
 ('ARGUMENTS_END', 477, ')'),
 ('END_LINE', 478, ';'),
 ('VARIABLE', 492, 'i'),
 ('PLUS_EQUALS', 494, '+='),
 ('PLUS', 496, '+'),
 ('INT', 497, 1),
 ('END_LINE', 498, ';'),
 ('END_BLOCK', 508, '}'),
 ('VARIABLE', 510, 'else'),
 ('START_BLOCK', 515, '{'),
 ('FUNCTION', 529, 'Print'),
 ('ARGUMENTS_START', 534, '('),
 ('STRING', 535, 'No'),
 ('ARGUMENTS_END', 539, ')'),
 ('END_LINE', 540, ';'),
 ('VARIABLE', 554, 'i'),
 ('MINUS_EQUALS', 556, '-='),
 ('MINUS', 558, '-'),
 ('INT', 559, 1),
 ('END_LINE', 560, ';'),
 ('END_BLOCK', 570, '}'),
 ('VARIABLE', 580, 'break'),
 ('END_LINE', 585, ';'),
 ('END_BLOCK', 591, '}'),
 ('STATEMENT', 597, 'call'),
 ('VARIABLE', 602, 'other'),
 ('END_LINE', 607, ';'),
 ('END_BLOCK', 609, '}')]



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

def tokenify(tokens: list) -> list:
    classed_tokens = []
    for token in tokens:
        classed_tokens.append(tokenType(token))
    return classed_tokens

def treeify(tokens: list) -> Tree:
    # Tree based off subroutines
    classed_tokens = tokenify(tokens)

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



def transpileFlat(flatTokenList: list) -> list:
    code = ['']
    # context = 'NA'
    currentVar = ''
    for token in flatTokenList:
        if token.tokenType in ['INT', 'FLOAT', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'LESS_THAN', 'GREATER_THAN', 'LESS_OR_EQUAL', 'GREATER_OR_EQUAL', 'ASSIGN', 'NOT_EQUAL']:
            code[-1] += str(token.tokenVal)
        elif token.tokenType == 'VARIABLE':
            code[-1] += token.tokenVal
            currentVar = token.tokenVal
        elif token.tokenType == 'END_LINE':
            code.append('')
        elif token.tokenType == 'COMPARISON':
            code[-1] += '='
        elif token.tokenType == 'PLUS_ONE':
            code[-1] += f'= {currentVar} + 1'
        elif token.tokenType == 'MINUS_ONE':
            code[-1] += f'= {currentVar} - 1'
        elif token.tokenType == 'MINUS_EQUALS':
            code[-1] += f'= {currentVar} - '
        elif token.tokenType == 'PLUS_EQUALS':
            code[-1] += f'= {currentVar} + '
        elif token.tokenVal == 'Print':
            code[-1] += 'PRINT '
        elif token.tokenVal == 'while':
            code[-1] += 'WHILE '
        elif token.tokenType == 'STRING':
            code[-1] += f'"{token.tokenVal}"'
        # elif token.tokenVal == 'askInput':


    return code

def cleanInputs(tokenList: list) -> list:
    # print("Inputs:", inputs)
    noInputs = 0
    # for noInputs, idx in enumerate(inputs):
    while True:
        inputs = [idx for idx, token in enumerate(tokenList) if token.tokenVal == 'askInput']
        if len(inputs) == 0:
            break
        idx = inputs[0]
        noInputs += 1
        depth = 1
        tokenIdx = idx + 1
        while True:
            tokenIdx += 1
            if tokenList[tokenIdx].tokenType == 'ARGUMENTS_END':
                depth -= 1
            elif tokenList[tokenIdx].tokenType == 'ARGUMENTS_START':
                depth += 1
            if depth == 0:
                break
        
        inputString = tokenList[idx+2:tokenIdx]
        print("inputString", inputString)
        tokenList[idx:tokenIdx] = [
           tokenType(('VARIABLE', -1, f"reservedInputValue{noInputs}$"))
        ]
        lastLineSearch = [
            idx for idx, token in enumerate(tokenList[:idx]) 
            if token.tokenType in ['START_BLOCK', 'END_LINE']
        ][-1]
        tokenList[lastLineSearch:lastLineSearch] = [
            tokenType(('END_LINE', -1, ';')),
            tokenType(("STATEMENT", -1, "INPUT")),
            tokenType(('ARGUMENTS_START', -1, '(')),
        ] + inputString + [
            tokenType(('ARGUMENTS_SEP', -1, ',')),
            tokenType(('VARIABLE', -1, f"reservedInputValue{noInputs}$")),
            tokenType(('ARGUMENTS_END', -1, ')')),
            tokenType(('END_LINE', -1, ';'))
        ]
        pprint.pprint([token.tokenVal for token in tokenList])
        
        

    return tokenList
        


def transpile(tokenList: list) -> str:
    tokenIdx = 0
    context = 'null'
    subName = 'NA'
    code = ['GOSUB main',
    'escape$=CHR$(27)',
    'clear$=escape$+"E"',
    'home$=escape$+"H"',
    'move$=escape$+"Y"',
    'con$=e$+"e"',
    'coff$=e$+"f"',
    'REM other',
    "'",
    '']
    subroutines = OrderedDict()
    noIfStatements = 0
    endLineStatementPos = [n for n, t in enumerate(tokenList) if t.tokenType == 'END_LINE']
    finishedLines = 0
    while True:
        if tokenList[tokenIdx].tokenVal == 'sub':
            context = 'subroutine'
            subName = tokenList[tokenIdx+1].tokenVal
            subroutines[subName] = []
            tokenIdx += 2
        elif tokenList[tokenIdx].tokenVal == 'printAt':
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+2:endLineStatementPos[finishedLines]-1], lambda x: x.tokenType not in ['ARGUMENTS_SEP']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]
            lineNo = ' '.join(temp[0])
            columnNo = ' '.join(temp[1])
            string = ' '.join(temp[2])
            subroutines[subName].append(
                f"PRINT move$;CHR$({lineNo}+32);CHR$({columnNo}+32);"
            )
            subroutines[subName].append(
                f"PRINT {string};"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'Print':
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+2:endLineStatementPos[finishedLines]-1], lambda x: x.tokenType not in ['ARGUMENTS_SEP']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]
            string = ' '.join(temp[0])
            subroutines[subName].append(
                f"PRINT {string}"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'clearScreen':
            subroutines[subName].append(
                f"PRINT clear$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'enableCursor':
            subroutines[subName].append(
                f"PRINT con$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'disableCursor':
            subroutines[subName].append(
                f"PRINT coff$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'resetCursor':
            subroutines[subName].append(
                f"PRINT home$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx

        elif tokenList[tokenIdx].tokenVal == 'var':
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+1:endLineStatementPos[finishedLines]], lambda x: x.tokenType not in ['ASSIGN']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]
            # for t in [token for tokenList in temp for token in tokenList if token.tokenVal == 'askInput']:
            #     subroutines[subName].append(
            #         "INPUT "
            #     )
            # print(temp)
            varName = ' '.join(temp[0])
            varValue = ' '.join(temp[1])
            subroutines[subName].append(
                f"{varName} = {varValue}"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        
        elif tokenList[tokenIdx].tokenVal == 'INPUT':
            print("i have an input here", tokenIdx)
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+2:endLineStatementPos[finishedLines]-1], lambda x: x.tokenType not in ['ARGUMENTS_SEP']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]
            inputString = ' '.join(temp[0])
            variableName = ' '.join(temp[1])
            subroutines[subName].append(
                f"INPUT {inputString}, {variableName}"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        
        elif tokenList[tokenIdx].tokenType == 'END_LINE':
            finishedLines += 1
            tokenIdx += 1
        else:
            tokenIdx += 1
        print(tokenIdx)
        if tokenIdx >= len(tokenList):
            break
        print(subroutines)

    return "\n".join([f'REM {key}\n' + "\n".join(text) for key, text in subroutines.items()])


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
    
    class_tokens = tokenify(input_tokens)
    class_tokens = cleanInputs(class_tokens)
    print(transpile(class_tokens))