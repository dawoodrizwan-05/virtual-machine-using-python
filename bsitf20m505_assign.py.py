import sys


def push(val):
    global sp, data
    sp -= 1
    data[sp] = val



def pop():
    global sp, data
    val = data[sp]
    sp += 1
    return val



def load_vm_image(filename):
    with open(filename, 'r') as f:
        data_size = int(f.readline().strip(), 16)
        data = [0] * data_size
        image_size = int(f.readline().strip(), 16)
        for i in range(image_size):
            data[i] = int(f.readline().strip(), 16)
    return data


def interpret_instruction(instruction):
    global ip, sp, data
    binop = instruction >> 31
    operation = (instruction >> 24) & 0x7f
    optional_data = instruction & 0xffffff
    

    if binop == 0:
        if operation == 0:
            # pop
            pop()
        elif operation == 1:
            # push <const>
            push(optional_data)
        elif operation == 2:
            # push ip
            push(ip)
        elif operation == 3:
            # push sp
            push(sp)
        elif operation == 4:
            # load
            addr = pop()
            push(data[addr])
        elif operation == 5:
            # store
            st_data = pop()
            addr = pop()
            data[addr] = st_data
        elif operation == 6:
            # jmp
            cond = pop()
            addr = pop()
            if cond != 0:
                ip = addr
        elif operation == 7:
            # not
            val = pop()
            if val == 0:
                push(1)
            else:
                push(0)
        elif operation == 8:
            # putc
            sys.stdout.write(chr(pop() & 0xff))
            sys.stdout.flush()
        elif operation == 9:
            # getc
            x = sys.stdin.read(1)
            if x:
                push(ord(x))
            else:
                push(-1)
        elif operation == 10:
            # halt
            sys.exit()
        else:

            raise ValueError(f"Unknown operation: {operation}")
        
    else:
        # binop == 1
        b = pop()
        a = pop()
        if operation == 0:
            push(a + b)
        elif operation == 1:
            push(a - b)
        elif operation == 2:
            push(a * b)
        elif operation == 3:
            push(a // b)
        elif operation == 4:
            push(a & b)
        elif operation == 5:
            push(a | b)
        elif operation == 6:
            push(a ^ b)
        elif operation == 7:
            push(int(a == b))
        elif operation == 8:
            push(int(a < b))
        else:

            raise ValueError(f"Unknown operation: {operation}")
    


def execute_program(data):
    global ip, sp
    ip = 0
    sp = len(data)
    
    while True:
        instruction = data[ip]
        ip += 1
        interpret_instruction(instruction)


if __name__ == '__main__':
    data = load_vm_image('task1.bin')
    execute_program(data)





    
