# https://sagecell.sagemath.org/

N = 7
M = 17005450388330379
WORD_SIZE = 32
state = [1927245640, 871031439, 789877080, 4042398809, 3950816575, 2366948739, 935819524]

def main():
    A = matrix(GF(2), N*WORD_SIZE, N*WORD_SIZE, 0)

    '''
    t = state[0] ^ ((state[0] << 11) & WORD_MASK)
    state[-1] = (state[-1] ^ (state[-1] >> 19)) ^ (t ^ (t >> 8))

    state[-1] = state[0] ^ (state[0] << 11) ^ (state[0] >> 8) ^ ((state[0] << 11) >> 8) ^ state[-1] ^ (state[-1] >> 19) 
    '''

    # left rotate WORD_SIZE bits
    op_matrix_rol(A, WORD_SIZE)

    # state[N-1] ^= state[0] << 11
    op_matrix_move(A, (N-1)*WORD_SIZE+11, 0*WORD_SIZE,        WORD_SIZE-11)

    # state[N-1] ^= state[0] >> 8
    op_matrix_move(A, (N-1)*WORD_SIZE,    0*WORD_SIZE+8,      WORD_SIZE-8)

    # state[N-1] ^= (state[0] << 11) >> 8
    op_matrix_move(A, (N-1)*WORD_SIZE+3,  0*WORD_SIZE,        WORD_SIZE-11)

    # state[N-1] ^= state[N-1]
    op_matrix_move(A, (N-1)*WORD_SIZE,    (N-1)*WORD_SIZE,    WORD_SIZE)

    # state[N-1] ^= state[N-1] >> 19
    op_matrix_move(A, (N-1)*WORD_SIZE,    (N-1)*WORD_SIZE+19, WORD_SIZE-19)

    invA_M = matrix_pow(A.inverse(), M)
    S = intlist_to_bitmatrix(state, WORD_SIZE)

    init_state  = bitmatrix_to_intlist(invA_M * S, WORD_SIZE)

    print(b''.join(list(map(lambda x: int.to_bytes(x, WORD_SIZE//8, 'big'), init_state))))
    # b'FLAG{m47r1x_!n_8inary_w0rld}'

def intlist_to_bitmatrix(vl, bits=32):
    bf = matrix(GF(2), len(vl)*bits, 1)
    for index, value in enumerate(vl):
        for bit_index in range(bits):
            bf[index*bits + bit_index, 0] = (value >> bit_index) & 1
    return bf

def bitmatrix_to_intlist(bf, bits=32):
    vl = []
    for index in range(bf.nrows()//bits):
        value = 0
        for bit_index in range(bits):
            value |= int(bf[index*bits + bit_index, 0]) << bit_index
        vl.append(int(value))
    return vl

def op_matrix_move(a, dst, src, length):
    for i in range(length):
        a[dst + i, src + i] += 1

def op_matrix_shl(a, shift_bits):
    op_matrix_move(a, 0, shift_bits, a.nrows() - shift_bits)

def op_matrix_shr(a, shift_bits):
    op_matrix_move(a, shift_bits, 0, a.nrows() - shift_bits)

def op_matrix_rol(a, rot_bits):
    bits = a.nrows()
    op_matrix_move(a, 0, rot_bits, bits - rot_bits)
    op_matrix_move(a, bits - rot_bits, 0, rot_bits)

def op_matrix_ror(a, rot_bits):
    bits = a.nrows()
    op_matrix_move(a, rot_bits, 0, bits - rot_bits)
    op_matrix_move(a, 0, bits - rot_bits, rot_bits)

def matrix_pow(a, n):
    sz = a.nrows()
    assert sz == a.ncols()

    An = matrix.identity(sz)
    while n:
        if n & 1:
            An *= a
        a *= a
        n >>= 1
    return An 

if __name__ == '__main__':
    main()
