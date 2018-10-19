# run with python3 -i
from interp import Program
p = Program(1)
try:
    while True:
        p.run(input('-' * ~-len(p.blocks) + '>> '))
except EOFError:
    print()