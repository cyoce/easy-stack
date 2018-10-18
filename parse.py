# parse(str code): transform text into tokens (list)
# execute(list tokens): execute list of tokens

from collections import namedtuple

class Program:
    TOKEN_SEPARATORS = '()[]{}'
    TOKEN_WHITESPACE = ' \t\r\n'
    def __init__(self, debug=0):
        self.stack = []                 # program's runtime stack for calculations
        self.main_block = ['']          # the program as a whole represented by an encompassing block
        self.blocks = [self.main_block] # currently active code blocks.
                                        # when a code block is completed, it is pushed to its containing block
        self.functions = FunctionIndex()
        self.debug = debug

    def push(self, *items):
        for item in items:
            self.stack.append(item)

    def pop(self, length=None):
        if length is None:
            return self.stack.pop()
        a = []
        for i in range(length):
            a.insert(0, self.pop())
        return a

    def run(self, text):
        text += "\n"
        string = False # is it currently parsing a string literal?
        for i, c in enumerate(text):

            if c == '"':
                self.blocks[-1][-1] += c
                if string:
                    self.blocks[-1].append('')
                    string = False
                else:
                    string = True
                continue
            elif string:
                self.blocks[-1][-1] += c
                continue


            # print(c)
            if c in Program.TOKEN_WHITESPACE:
                self.blocks[-1].append('')

            elif c == '{':
                self.blocks.append([''])
            elif c == '}':
                current = self.blocks.pop()
                self.blocks[-1].append(Block(current))
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
        if self.debug == 1:
            print(self.stack)


    def execute(self, *tokens):
        for command in tokens:
            if command == '': continue
            if type(command) == Block:
                self.push(command)
            elif command[0] == '"':
                self.push(command[1:-1])
            elif command[0] in '0123456789-':
                val = None
                try:
                    val = int(command)
                except ValueError:
                     val = float(command)
                self.push(val)
            else:
                fn = self.functions[command]
                fn(self)


            if self.debug == 2:
                print(self.stack)

class FunctionIndex:
    FunctionTuple = namedtuple('F', 'func arity') # func is the reference to the function, arity is how many arguments it takes. a negative arity means the first argument should be the program
    def __init__(self):

        self.setup_index()


    def __getitem__(self, key):
        f = self.index[key]
        def wrapper(program):
            arity = f.arity
            needs_program = False
            if arity < 0:
                arity = ~arity
                needs_program = True
            args = program.pop(arity)
            if needs_program:
                args.insert(0, program)
            out = f.func(*args)
            if out is not None:
                program.push(out)
        return wrapper

    def setup_index(self):
        F = FunctionIndex.FunctionTuple
        def times(program, block, n):
            for i in range(n):
                program.execute(*block)


        self.index = {
            '+': F(lambda x,y: x+y, 2),
            '-': F(lambda x,y: x-y, 2),
            '*': F(lambda x,y: x*y, 2),
            '/': F(lambda x,y: x/y, 2),
            '//':F(lambda x,y: x//y,2),
            'puts': F(print, 1),
            'times': F(times, ~2)
        }


class Block(tuple):
    def __init__(self, vals):
        self.vals = vals


    def __repr__(self):
        return '{' + ' '.join(filter(len,map(str,self.vals))) + '}'

    __str__ = __repr__
