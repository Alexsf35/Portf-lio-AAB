import random

#1) Escolher posições iniciais de forma aleatória s = (s1,...,st) e formar os segmentos respectivos. 

seqs = ["ATGGTCGC","ATGTCTGA","CCGTAGTA","ATGCATGCATCGATC"]

def pos_init(seqs: list,tam_motif: int):
    tam_seqs = []
    for i in seqs:
        tam_seqs.append(len(i))
    pos=[]
    motif=[]
    for i, seqs in enumerate(seqs):
        ni = random.randint(0, tam_seqs[i] - tam_motif)
        pos.append(ni)
        motif.append(seqs[ni:ni+tam_motif])
    
    return pos, motif
pos_i,motifs= pos_init(seqs,4)
print(pos_i,motifs)

#2) Escolher aleatoriamente uma sequência i

def choose_seq(seqs):
    
    return seqs[random.randint(0,len(seqs)-1)]

chosen_seq = choose_seq(seqs)
print(chosen_seq)


#3) Criar matriz_oc P das outras sequências a partir de s

def matriz_oc(seqs: list, pseudocont: float = 0):

    alfabeto = "ACGT"
    tam_seq = len(seqs[0])
    mat = {}
    for nuc in alfabeto:
        mat[nuc] = []
        for _ in range(tam_seq):
            mat[nuc].append(pseudocont)

    for i in seqs:
        for k, nuc in enumerate(i):
            index = alfabeto.index(nuc)
            mat[nuc][k] += 1
    
    return mat

ocorrencias = matriz_oc(motifs)
print(ocorrencias)



def pwm(ocorrencias: dict):
    pwm = {}

    for nuc in ocorrencias:
        pwm[nuc] = []

    col_sums = []
    for j in range(len(ocorrencias["A"])):
        soma = 0
        for nuc in ocorrencias:
            soma += ocorrencias[nuc][j]
        col_sums.append(soma)

    for nuc in ocorrencias:
        for k in range(len(ocorrencias[nuc])):
            if col_sums[k] > 0:
                pwm[nuc].append(ocorrencias[nuc][k] / col_sums[k])
            else:
                pwm[nuc].append(0)

    return pwm

def consenso(pwm:dict):
    columns = []
    for i in range(0,len(pwm["A"])):
        column = {}
    
        for k in pwm.keys():
            column[k] = pwm[k][i]

        nuc_consenso = max(column, key = column.get)
        columns.append(nuc_consenso)

    seq_consenso = "".join(columns)
    return seq_consenso



pwm_matrix = pwm(ocorrencias)
for nuc, values in pwm_matrix.items():
    formatted_values = [f"{value:.3f}" for value in values]
    print(f"{nuc}: {'  '.join(formatted_values)}")


seq_consensos = consenso(pwm_matrix)
print(seq_consensos)

#4) Para cada posição p na sequência i, calcular a probabilidade do segmento iniciado em p com tamanho L, ser gerado por P. 
