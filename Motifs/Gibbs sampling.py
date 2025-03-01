import random

#1) Escolher posições iniciais de forma aleatória s = (s1,...,st) e formar os segmentos respectivos. 

seqs = ["GTAAACAATATTTATAGC","AAAATTTACCTCGCAAGG","CCGTACTGTCAAGCGTGG","TGAGTAAACGACGTCCCA","TACTTAACACCCTGTCAA"]
tam_motif = 8
def pos_init(seqs: list,tam_motif: int):
    tam_seqs = []
    for i in seqs:
        tam_seqs.append(len(i))
    pos=[]
    motif=[]
    for i, seqs in enumerate(seqs):
        ni = random.randint(0, tam_seqs[i] - tam_motif)
        pos.append(ni)
    
    return pos
pos_i= pos_init(seqs,tam_motif)
print(pos_i)

#2) Escolher aleatoriamente uma sequência i

def choose_seq(seqs,pos_i, tam_motif):
    motif = [[],[]]
    random_seq = random.choice(seqs)
    seqs2 = seqs[:]
    index = seqs2.index(random_seq)

    for seq,pos in zip(seqs2,pos_i):
        motif[0].append(pos)
        motif[1].append(seq[pos:pos+tam_motif])

    seqs2.pop(index)
    motif[0].pop(index)
    motif[1].pop(index)
    return random_seq, seqs2,motif

chosen_seq, seqs2, motifs = choose_seq(seqs,pos_i,tam_motif)
print(chosen_seq)
print(seqs2)
print(motifs)

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

ocorrencias = matriz_oc(motifs[1],pseudocont=0.5)
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

def prob_p(chosen_seq,tam_motif,pwm_matrix):
    #Creating the motifs
    motifs_i = []
    for i in range(len(chosen_seq)-tam_motif+1):
        motifs_i.append(chosen_seq[i:i+tam_motif])
    
    #Calculating probabilities
    motif_probs={}
    for motif in motifs_i:
        probs = 1

        for k,nuc in enumerate(motif):
            probs *= pwm_matrix[nuc][k]

        motif_probs[motif] = probs

    return motif_probs


results = prob_p(chosen_seq,tam_motif,pwm_matrix)
print(results)

#5) Escolher p de modo de forma estocástica, de acordo com as probabilidades calculadas em 4). 

def normalize_probabilities(motif_probs):
    normalized_probs = {}
    sum = 0
    for value in motif_probs.values():
        sum += value
    print(sum)
    for (motif, prob) in motif_probs.items():
        normalized_probs[motif] = (prob/sum)

    return normalized_probs
normalize_probabilities(results)



