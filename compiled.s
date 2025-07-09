.section .data
float_0: .float 0.5
.section .text
.globl main
main:
    push %ebp
    mov %esp, %ebp
    sub $12, %esp    # espaço para variáveis locais
    movl $5, %eax
    movl %eax, -4(%ebp)    # x
    movss float_0, %xmm0
    movss %xmm0, -8(%ebp)    # y
    movss -8(%ebp), %xmm0
    push %eax
    movl -4(%ebp), %eax
    pop %ebx
    addl %ebx, %eax
    movss %xmm0, -12(%ebp)    # z
    movl $10, %eax
    movl %eax, -4(%ebp)    # x (int assign)
    mov %ebp, %esp
    pop %ebp
    ret