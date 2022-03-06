.data
.text
.globl main
li x1,10
li x2,20
li x3,1
loop:
beq x1,x2,end
add x1,x1,x3
j loop

end:
