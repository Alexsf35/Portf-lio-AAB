import random

#1) Escolher posições iniciais de forma aleatória s = (s1,...,st) e formar os segmentos respectivos. 
def pos_init(seqs: list,tam_motif: int) -> list:

    """
    Esta função escolhe aleatóriamente a posição inicial dos motifs em cada sequência.

    Parameters:
    seqs : list
        Uma lista com as sequencias.
    tam_motif: int
        O tamanho do motif

    Returns:
    list
        Uma lista com a posição inicial dos motifs em cada sequência.
    """

    tam_seqs = [] 
    for i in seqs: #Armazena o tamanho das sequências
        tam_seqs.append(len(i))
    pos=[] #Inicializa a lista que vai contêr as posições iniciais.
    for i, seqs in enumerate(seqs): #Para cada sequência escolhe de forma aleatória a posição inicial do motif.
        ni = random.randint(0, tam_seqs[i] - tam_motif)
        pos.append(ni)
    
    return pos

#2) Escolher aleatoriamente uma sequência i
def choose_seq(seqs, pos_i, tam_motif):

    """
    Esta função retira uma sequência aleatória da lista de sequências e devolve a sequência escolhida, a nova lista de sequências e os seus motifs e o index da sequência retirada.
    Parameters:
    seqs : list
        Uma lista com as sequencias.
    pos_i: list
        Uma lista com as posições iniciais dos motifs
    tam_motif: int
        O tamanho do motif

    Returns:
    chosen_seq: str
        A sequência que foi escolhida para ser retirada da lista.
    seqs2: list
        A nova lista de sequências em que foi retirada a sequência escolhida.
    motifs: list
        Uma lista com os motifs selecionados.
    random_index: int
        O index da sequência escolhida.
    """
    random_index = random.randint(0, len(seqs) - 1) #Escholhe aleatóriamente uma das sequências da lista seqs.
    chosen_seq = seqs[random_index] #Armazena a sequência escolhida numa variável.
    seqs2 = seqs[:random_index] + seqs[random_index + 1:] #Cria uma nova lista de sequências sem a sequ~encia escolhida.
    motif_positions = pos_i[:random_index] + pos_i[random_index + 1:] #Cria uma lista das posições iniciais dos motifs sem a sequência escolhida.
    motifs = []
    for i in range(len(seqs2)): #Percorre a lista de sequências e extrai os motifs de cada.
        motifs.append(seqs2[i][motif_positions[i]:motif_positions[i] + tam_motif])
    return chosen_seq, seqs2, motifs, random_index

#3) Criar matriz_oc P das outras sequências a partir de s
def matriz_oc(seqs: list, pseudocont: float = 0):

    """
    Esta função retira uma sequência aleatória da lista de sequências e devolve a sequência escolhida, a nova lista de sequências e os seus motifs e o index da sequência retirada.
    Parameters:
    seqs : list
        Uma lista com as sequencias dos motifs.
    pseudocont: float
        Adiciona um valor a todas as posições da matriz de ocorrências para impedir que tenha posições com 0.

    Returns:
    mat: dict
        Um dicionário com a matriz de contagem das sequências.
    """

    alfabeto = "ACGT"
    tam_seq = len(seqs[0]) #Tamanho dos motifs.
    mat = {}
    for nuc in alfabeto: # Cria a estrutura da matriz.
        mat[nuc] = []
        for _ in range(tam_seq): # Adiciona a pseudocontagem.
            mat[nuc].append(pseudocont)

    for i in seqs: #Preenche a matriz de contagens.
        for k, nuc in enumerate(i):
            mat[nuc][k] += 1
    
    return mat


def pwm(ocorrencias: dict):

    """
    Calcula a matriz de probabilidades(PWM) a partir da matriz de contagem.
    
    Parameters:
    ocorrencias : dict
        Dicionário com a matriz de contagem das sequências.

    Returns:
    dict
        Dicionário representando a matriz de probabilidades (PWM).
    """

    pwm = {}

    for nuc in ocorrencias: #Cria a matriz para a pwm.
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

    """
    Obtém a sequência consenso a partir da matriz PWM.
    
    Parameters:
    pwm : dict
        Matriz de probabilidades dos motifs.

    Returns:
    str
        Sequência consenso.
    """

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

    """
    Calcula a probabilidade de cada possível motif dentro da sequência escolhida.
    
    Parameters:
    chosen_seq : str
        Sequência retirada.
    tam_motif : int
        Tamanho do motif.
    pwm_matrix : dict
        Matriz PWM calculada a partir das sequências restantes.

    Returns:
    dict
        Dicionário contendo motifs possíveis e suas probabilidades.
    """
    
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

    """
    Normaliza as probabilidades dos motifs.
    
    Parameters:
    motif_probs : dict
        Dicionário de probabilidades não normalizadas.

    Returns:
    dict
        Dicionário com probabilidades normalizadas.
    """

    total_prob = sum(motif_probs.values())

    if total_prob == 0: # Se todas as probabilidades forem 0, distribui uniformemente
        num_motifs = len(motif_probs)
        return {motif: 1 / num_motifs for motif in motif_probs}
    
    normalized_probs = {}
    for motif, prob in motif_probs.items():
        normalized_probs[motif] = prob / total_prob
    return normalized_probs

#5) Escolher p de modo de forma estocástica, de acordo com as probabilidades calculadas em 4). 
def roulette_wheel(normal_probs):

    """
    Escolhe um motif com base nas probabilidades normalizadas.
    
    Parameters:
    normal_probs : dict
        Dicionário de probabilidades normalizadas.

    Returns:
    str
        Motif escolhido.
    """

    motifs = list(normal_probs.keys())
    probabilities = list(normal_probs.values())
    return random.choices(motifs, weights=probabilities, k=1)[0]

#6) Repetir passos 2) a 5) enquanto for possível melhorar
def gibbs_sampler(seqs, tam_motif, num_iterations=1000):

    """
    Implementa o algoritmo de Gibbs para encontrar motifs.
    
    Parameters:
    seqs : list
        Lista de sequências.
    tam_motif : int
        Tamanho do motif.
    num_iterations : int
        Número de iterações do algoritmo.

    Returns:
    list
        Lista de motifs encontrados e suas posições.
    """

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
