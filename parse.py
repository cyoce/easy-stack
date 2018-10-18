# parse(str code): transform text into tokens (list)
# execute(list tokens): execute list of tokens

class Program:
    TOKEN_SEPARATORS = '()[]{}'
    TOKEN_WHITESPACE = ' \t\r\n'
    def __init__(self):
        self.stack = []                 # program's runtime stack for calculations
        self.main_block = ['']          # the program as a whole represented by an encompassing block
        self.blocks = [self.main_block] # currently active code blocks.
                                        # when a code block is completed, it is pushed to its containing block


    def push(self, *items):
        for item in items:
            self.stack.append(item)

    def run(self, text):
        text += "\n"
        string = False # are we currently parsing a string literal?
        for i, c in enumerate(text):

            if c == '"':
                self.blocks[-1][-1] += c
                if string:
                    self.blocks[-1].append('')
                    string = False
                else:

                    string = True

            # print(c)
            if c in Program.TOKEN_WHITESPACE:
                self.blocks[-1].append('')

            elif c  == '{':
                self.blocks.append([])
            elif c == '}':
                current = self.blocks.pop()
                self.blocks[-1].append(CodeBlock(current))
                self.blocks[-1].append('')

            elif c in Program.TOKEN_SEPARATORS:
                self.blocks[-1].append(c)
                self.blocks[-1].append('')

            else:
                self.blocks[-1][-1] += c

            # print(c, i, self.blocks[-1])

            if self.blocks[-1] is self.main_block and self.main_block[-1] == '':
                self.execute(*self.main_block)
                self.main_block[:] = [''] # reset main block


    def execute(self, *tokens):
        for command in tokens:
            pass




class CodeBlock: # protect code blocks from being treated as a standard array by the interpreter
    def __init__(self, array):
        self.val = array
