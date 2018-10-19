class Program: # 88 LLOC 
    TOKEN_SEPARATORS = '()[]{}'
    TOKEN_WHITESPACE = ' \t\r\n'
    def __init__(self):
        self.stack = []                 # program's runtime stack for calculations
        self.main_block = ['']          # the program as a whole represented by an encompassing block
        self.blocks = [self.main_block] # currently active code blocks. when a code block is completed, it is pushed to its containing block
        self.vars = {}
        self.arrays = []
    def peek(self):
        return self.stack[-1]
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
        for c in text:
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
            if c in Program.TOKEN_WHITESPACE:
                self.blocks[-1].append('')
            elif c == '{':
                self.blocks.append([''])
            elif c == '}':
                current = self.blocks.pop()
                self.blocks[-1].append(tuple(current))
                self.blocks[-1].append('')
            elif c in Program.TOKEN_SEPARATORS:
                self.blocks[-1].append(c)
                self.blocks[-1].append('')
            else:
                self.blocks[-1][-1] += c
            if self.blocks[-1] is self.main_block and self.main_block[-1] == '':
                self.execute(*self.main_block)
                self.main_block[:] = [''] # reset main block
        if self.debug == 1:
            print(self.stack)
    def execute(self, *tokens):
        for command in tokens:
            if command == '': continue
            if type(command) is tuple:
                self.push(command)
            elif command[0] == '"':
                self.push(command[1:-1])
            elif command[0] in '0123456789-':
                if command[0] == '-' and (len(command) == 1 or command[1] not in '0123456789.'):
                    self.exec_cmd(command)
                    break
                val = None
                try:
                    val = int(command)
                except ValueError:
                     val = float(command)
                self.push(val)
            else:
                self.exec_cmd(command)
            if self.debug == 2:
                print(self.stack)
    def exec_cmd(self, c):
        if c.startswith('->'):
            self.vars[c[2:]] = self.pop()
        elif c.startswith('<-'):
            self.push(self.vars[c[2:]])
        elif c == '[':
            self.arrays.append([])
        elif c == ']':
            self.push(self.arrays.pop())
        elif c == ',':
            self.arrays[-1].append(self.pop())
        else:
            self.execute(*self.vars[c])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    