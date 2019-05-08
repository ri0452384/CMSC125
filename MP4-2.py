"""
This code will convert the input string into its postfix equivalent to evaluate its value. returns an integer value only.

references:
http://interactivepython.org/lpomz/courselib/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
https://www.aoprogrammer.com/infix-prefix-and-postfix-notation/
by: Rayven N. Ingles

"""

from pythonds.basic.stack import Stack


def classify(expression):
    tokenList = expression.split()
    if tokenList[0] in "^*/%+-":
        return "prefix"
    elif tokenList[-1] in "^*/%+-":
        return "postfix"
    else:
        return "infix"


def prefixToInfix(prefixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["%"] = 3
    prec["+"] = 2
    prec["-"] = 2
    infixStack = Stack()
    tokenList = prefixexpr[::-1].split()
    for token in tokenList:
        if token.isdigit():
            infixStack.push(token.__str__())
        else:
            operand1 = infixStack.pop()
            operand2 = infixStack.pop()
            infixStack.push(("( " + operand1 + " "+ token + " " + operand2 + " )"))
    output = ""
    output += infixStack.pop()
    if infixStack.isEmpty():
        return output
    else:
        print("Error! Invalid Input!")
        exit(1)

        
def infix_to_postfix(infixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["%"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token.isdigit():
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def postfix_eval(postfixExpr):
    operandStack = Stack()
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token.isdigit():
            operandStack.push(int(token))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = do_math(token,operand1,operand2)
            operandStack.push(result)
    return operandStack.pop()

def do_math(op, op1, op2):
    if op == "^":
        ans = op1 ** op2
        print(op1,op,op2,ans)
        return ans
    elif op == "*":
        ans = op1 * op2
        print(op1,op,op2,ans)
        return ans
    elif op == "/":
        ans = int(float(op1 / op2))
        print(op1,op,op2,ans)
        return ans
    elif op == "+":
        ans = op1 + op2
        print(op1,op,op2,ans)
        return ans
    elif op == "%":
        ans = op1 % op2
        print(op1,op,op2,ans)
        return ans
    else:
        ans = op1 - op2
        print(op1,op,op2,ans)
        return ans


#main starts here
entered_input = input("Enter an expression: ")
classification = classify(entered_input)

if classification == "infix":
    print("Infix detected \n infix:"+entered_input)
    print("\n value: "+postfix_eval(infix_to_postfix(entered_input)).__str__())
elif classification == "postfix":
    print("Postfix detected \n postfix: " + entered_input)
    print("\n value: "+postfix_eval(entered_input).__str__())
else:
    print("Prefix detected \n prefix: " + entered_input)
    a = prefixToInfix(entered_input)
    print("\n infix: "+a)
    print("\n value: "+postfix_eval(infix_to_postfix(a)).__str__())

