import random

#1) Escolher posições iniciais de forma aleatória s = (s1,...,st) e formar os segmentos respectivos. 
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

#2) Escolher aleatoriamente uma sequência i
def choose_seq(seqs, pos_i, tam_motif):
    random_index = random.randint(0, len(seqs) - 1)
    chosen_seq = seqs[random_index]
    seqs2 = seqs[:random_index] + seqs[random_index + 1:]
    motif_positions = pos_i[:random_index] + pos_i[random_index + 1:]
    motifs = []
    for i in range(len(seqs2)):
        motifs.append(seqs2[i][motif_positions[i]:motif_positions[i] + tam_motif])
    return chosen_seq, seqs2, motifs, random_index

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

#4) Para cada posição p na sequência i, calcular a probabilidade do segmento iniciado em p com tamanho L, ser gerado por P. 
def prob_p(chosen_seq, tam_motif, pwm_matrix):
    motifs_i = []
    for i in range(len(chosen_seq) - tam_motif + 1):
        motifs_i.append(chosen_seq[i:i+tam_motif])
    
    motif_probs = {}
    for motif in motifs_i:
        prob = 1
        for i, nuc in enumerate(motif):
            prob *= pwm_matrix[nuc][i]
        motif_probs[motif] = prob
    
    return motif_probs


def normalize_probabilities(motif_probs):
    total_prob = sum(motif_probs.values())
    normalized_probs = {}
    for motif, prob in motif_probs.items():
        normalized_probs[motif] = prob / total_prob
    return normalized_probs

#5) Escolher p de modo de forma estocástica, de acordo com as probabilidades calculadas em 4). 
def roulette_wheel(normal_probs):
    motifs = list(normal_probs.keys())
    probabilities = list(normal_probs.values())
    return random.choices(motifs, weights=probabilities, k=1)[0]

#6) Repetir passos 2) a 5) enquanto for possível melhorar
def gibbs_sampler(seqs, tam_motif, num_iterations=1000):
    pos_i = pos_init(seqs, tam_motif)
    
    for iteration in range(num_iterations):
        chosen_seq, seqs2, motifs, random_index = choose_seq(seqs, pos_i, tam_motif)
        ocorrencias = matriz_oc(motifs,pseudocont=0.01)
        pwm_matrix = pwm(ocorrencias)
        motif_probs = prob_p(chosen_seq, tam_motif, pwm_matrix)
        normalized_probs = normalize_probabilities(motif_probs)
        new_motif = roulette_wheel(normalized_probs)
        new_position = [i for i in range(len(chosen_seq) - tam_motif + 1) if chosen_seq[i:i+tam_motif] == new_motif][0]
        pos_i[random_index] = new_position
        
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Current best motifs - {[seqs[i][pos_i[i]:pos_i[i] + tam_motif] for i in range(len(seqs))]}")
    
    final_motifs = [(seqs[i][pos_i[i]:pos_i[i] + tam_motif], pos_i[i]) for i in range(len(seqs))]
    
    print("Final Motifs Found:")
    for i, (motif, position) in enumerate(final_motifs):
        print(f"Sequence {i+1}: {motif} (Start Position: {position})")
    
    return final_motifs

# Exemplo
seqs = ["GTAAACAATATTTATAGC", "AAAATTTACCTCGCAAGG", "CCGTACTGTCAAGCGTGG", "TGAGTAAACGACGTCCCA", "TACTTAACACCCTGTCAA"]
tam_motif = 8
result = gibbs_sampler(seqs, tam_motif, num_iterations=2000)