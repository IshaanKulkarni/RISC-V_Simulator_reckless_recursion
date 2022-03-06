# CO Project phase 1: Team reckless_recursion
# We are using regex and string formatting to extract and work on instructions using an if else ladder
import re
file=open("test1.asm","r")
lines=file.readlines()
print(lines)
file.close()


global RAM, ram_index, ram_label, instruction_label,i,c
line_counter = 0
RAM=[]
ram_index=0
ram_label={}
instruction_label={}
line_counter=0
c=[]

# Add syntax error class here later
# 32 integer registers of RISC-V. Register x0 is hardwired to 0 and is equivalent to $zero register of MIPS
registers={'x0':0,'x1':0,'x2':0,'x3':0,'x4':0,'x5':0,'x6':0,'x7':0,'x8':0,'x9':0,'x10':0,'x11':0,'x12':0,'x13':0,'x14':0,'x15':0,'x16':0,'x17':0,'x18':0,'x19':0,'x20':0,'x21':0,'x22':0,'x23':0,'x24':0,'x25':0,'x26':0,'x27':0,'x28':0,'x29':0,'x30':0,'x31':0}
BaseAddress="0x1000"
# Below function will remove all comments and white spaces from the given .asm file


def throwError(line):
    print(f"syntax error at line {line}")


def sanitize():
    i=0
    while i<len(lines):
        lines[i]=lines[i].strip()

        if(re.findall(r"^# *",lines[i]) or (re.findall(r"^\n",lines[i]) and len(lines[i])=='\n'.length())):
            lines.remove(lines[i])
            i-=1
        if len(lines[i])==0:
            lines.remove(lines[i])
            i-=1
        i+=1
    print(lines)

def process():
    RAM.clear()
    i=0
    while(i<len(lines)):
        if re.search(r"^\.data", lines[i]):
            while(1>0):
                i+=1

                if(re.findall(r"^\.text", lines[i])):
                    i-=1
                    break

                if lines[i][0]!='.':
                    s=lines[i].split(sep=':',maxsplit=1)
                    lines[i]=s[1].strip()
                    s=s[0].strip()
                    ram_label[s]=ram_index
                

                if re.findall(r"^\.word",lines[i]):
                    line=lines[i][6:]
                    line=line.split(sep=',')
                    for l in line:
                        l=l.strip()
                        RAM.append(int(l))
                        ram_index+=1
                
                elif(re.findall(r"^\.asciiz",lines[i])):
                    line=lines[i][9:len(lines[i])-1]
                    line=re.sub(r"\\n","\n", line)
                    line=re.sub(r"\\t","\t", line)
                    RAM.append(line)
                    ram_index+=1
                else:
                    throwError(i)
                    return
        # once everything is done ==> the next step is to find globl main --> at which the original program will begin
        if(re.findall(r"\.globl",lines[i])):
            i+=1
            break

        i+=1;    

    print("Memory: ", RAM)
    print("-"*100)

    line_counter=i
    print(line_counter)
    
    # Removing all the comments from the instructions
    while(i<len(lines)):
        occ=lines[i].find('#')
        if(occ>=0):
            j=occ
            while(lines[i][j-1]==' '):
                j-=1
            lines[i]=lines[i][:j]

        i+=1
    #Stroring all the labels against their line number so that we can call them back during loops
    i=line_counter
    while(i<len(lines)):
        if re.findall(r"^\w*:",lines[i]):
            label=lines[i].split(token=":",maxsplit=1)[0].strip()
            instruction_label[label]=i 
        i+=1

    return line_counter



# Function to perform add instruction 
def add(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    for i in range(len(instruction_line)):
        instruction_line[i]=str(instruction_line[i].strip()[1:])



    if isinstance(registers[instruction_line[1]],int) and isinstance(registers[instruction_line[2]],int):
        registers[instruction_line[0]]=int(registers[instruction_line[1]])+int(registers[instruction_line[2]])
    else:
        print("Invalid instruction format!")
        return -1
    return line_counter + 1

# Function to perform subtract instruction
def sub(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    for i in range(len(instruction_line)):
        instruction_line[i]=str(instruction_line[i].strip()[1:])
    if isinstance(registers[instruction_line[1]],int) and isinstance(registers[instruction_line[2]],int):
        registers[instruction_line[0]]=int(registers[instruction_line[1]])-int(registers[instruction_line[2]])
    else:
        print("Invalid instruction format!")
        return -1
    return line_counter + 1

def mul(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    for i in range(len(instruction_line)):
        instruction_line[i]=str(instruction_line[i].strip()[1:])
    if isinstance(registers[instruction_line[1]],int) and isinstance(registers[instruction_line[2]],int):
        registers[instruction_line[0]]=int(registers[instruction_line[1]])*int(registers[instruction_line[2]])
    else:
        print("Invalid instruction format!")
        return -1
    return line_counter + 1


# Function to perform bne instruction. Will be used to implement if/else/ loops in assembly
def bne(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    for i in range(len(instruction_line)-1):
        instruction_line[i]=str(instruction_line[i].strip()[1:])

    instruction_line[2]=instruction_line[2].strip()

    if registers[instruction_line[0]]==registers[instruction_line[1]]:
        return line_counter+1
    return int(instruction_label[instruction_line[2]])

# Function to perform beq instruction. Will be used to implement if/else/ loops in assembly
def beq(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    for i in range(len(instruction_line)-1):
        instruction_line[i]=str(instruction_line[i].strip()[1:])
    instruction_line[2]=instruction_line[2].strip()
    if registers[instruction_line[0]]!=registers[instruction_line[1]]:
        return line_counter+1
    return int(instruction_label[instruction_line[2]])

# Function to perform j (jump) instruction. Will be used to implement for loops when required
def j(instruction_line,line_counter):
    return instruction_label[instruction_line]

# Load word instruction function
def lw(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    instruction_line[0]=str(instruction_line[0].strip()[1:])
    instruction_line[1]=instruction_line[1].strip()
    forward=int(instruction_line[1].split(token1="(",maxaplit=1)[0])//4
    registers[instruction_line[0]]=RAM[int(registers[instruction_line[1][2:]])-int(BaseAddress[2:])+forward]
    return line_counter+1


# Save word instruction function
def sw(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    instruction_line[0]=str(instruction_line[0].strip()[1:])
    instruction_line[1]=instruction_line[1].strip()
    forward=int(instruction_line[1].split(token1="(",maxaplit=1)[0])//4
    RAM[int(registers[instruction_line[1][2:]])-int(BaseAddress[2:])+forward]=registers[instruction_line[0]]
    return line_counter+1



def li(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    for i in range(len(instruction_line)-1):
        instruction_line[i]=str(instruction_line[i].strip())
        
    instruction_line[1]=instruction_line[1].strip()
    registers[instruction_line[0]]=int(instruction_line[1])
    return line_counter+1

# Bit manipulation instructions
def sll(instruction_line,line_counter):
    instruction_line=instruction_line.split(",")
    for i in range(len(instruction_line)-1):
        instruction_line[i]=str(instruction_line[i].strip()[1:])
    registers[instruction_line[0]]=int(registers[instruction_line[1]]*pow(2,instruction_line[2]))

    return line_counter+1

# Excetuing the instructions in the file using if else ladder
def execute_instructions(line,line_counter):
    print(line)
    if re.findall(r"^\w*\s*:",line):
        label=line.split(token=":",maxaplit=1)
        line=label[1].strip()
        label=label[0].strip()
        instruction_label[label]=line_counter

        if line=='':
            return line_counter+1
    
    cue=line.split(sep=" ",maxsplit=1)
    try:
        instruction_line=cue[1]
    except:
        pass
    cue=cue[0]

    if cue=="add":
        return add(instruction_line,line_counter)
    if cue=="sub":
        return sub(instruction_line,line_counter)
    if cue=="bne":
        return bne(instruction_line,line_counter)
    if cue=="beq":
        return beq(instruction_line,line_counter)
    if cue=="lw":
        return lw(instruction_line,line_counter)
    if cue=="sw":
        return sw(instruction_line,line_counter)
    if cue=="li":
        return li(instruction_line,line_counter)

    if cue=="sll":
        return sll(instruction_line,line_counter)
    if cue=="j":
        return j(instruction_line,line_counter)
    else:
        print(cue)
        print("Invalid instruction! Please vet your code")
        return -1

def reckless():
    sanitize()
    line_counter = process()
        
    while line_counter< len(lines):
        print(line_counter)
        line_counter = execute_instructions(lines[line_counter],line_counter)
        if(line_counter == -1):
            break

    print("Memory after execution \n",RAM)
    print("-"*100)
    print("State of Registers after execution: ")
    print(registers)


if __name__ == "__main__":
    reckless()

