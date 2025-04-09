def score(seqs, offsets, tam_motif):
    """
    Calcula o score de uma configuração de offsets para encontrar o melhor motif.
    
    O score é determinado somando a contagem da base mais frequente em cada coluna do alinhamento gerado pelos offsets.
    Se a configuração for parcial, o score é calculado apenas para as sequências já definidas.
    
    Parâmetros:
    seqs (list of str): Lista de sequências de DNA.
    offsets (list of int): Lista de deslocamentos atuais para cada sequência.
    tam_motif (int): Tamanho do motif a ser identificado.
    
    Retorna:
    int: Score da configuração atual de offsets.
    """
    if not offsets:
        return 0
    snips = [s[p : p + tam_motif] for p, s in zip(offsets, seqs)]
    return sum(max(col.count(x) for x in set(col)) for col in zip(*snips))


def branch_and_bound(seqs, num_seqs, tam_seq, tam_motif):
    """
    Algoritmo Branch and Bound para encontrar os melhores conjuntos de offsets.
    
    Explora recursivamente diferentes combinações de offsets e usa poda para eliminar ramos que não podem
    superar o melhor score encontrado.
    
    Parâmetros:
    seqs (list of str): Lista de sequências de DNA.
    num_seqs (int): Número de sequências.
    tam_seq (int): Tamanho de cada sequência.
    tam_motif (int): Tamanho do motivo a ser identificado.
    
    Retorna:
    tuple: (
        melhores_offsets (list of list of int): Lista dos melhores conjuntos de offsets encontrados.
        melhor_score (int): Melhor score obtido.
    )
    """
    melhor_score = 0
    melhores_offsets = []

    # Dicionário de bases de DNA válidas
    bases_validas = {'A', 'C', 'G', 'T', 'a', 'c', 'g', 't'}

    # Validação das sequências de entrada
    for seq in seqs:

        if not all(base in bases_validas for base in seq):
            raise ValueError(f'As sequências devem conter apenas A, C, G, T.')

    assert all(len(seq) == len(seqs[0]) for seq in seqs), 'As sequências têm que ter o mesmo tamanho!'

    def rec(offsets):
        nonlocal melhor_score, melhores_offsets
        idx = len(offsets)  # Número de offsets já definidos

        if idx == num_seqs:
            score_atual = score(seqs, offsets, tam_motif)
            if score_atual > melhor_score:
                melhor_score = score_atual
                melhores_offsets = [offsets.copy()]
            elif score_atual == melhor_score:
                melhores_offsets.append(offsets.copy())
            return

        score_parcial = score(seqs, offsets, tam_motif)
        melhor_score_teorico = score_parcial + tam_motif * (num_seqs - idx)

        if melhor_score_teorico < melhor_score:
            return

        limite = tam_seq - tam_motif + 1
        for offset in range(limite):
            offsets.append(offset)
            rec(offsets)
            offsets.pop()

    rec([])
    return melhores_offsets, melhor_score


def mostra_motifs(resultado):
    """
    Exibe os melhores conjuntos de offsets e os motifs correspondentes.
    
    Parâmetros:
    resultado (tuple): Saída da função `branch_and_bound`, contendo os melhores offsets e o score máximo.
    
    Retorna:
    None: Apenas imprime os resultados.
    """
    melhores_offsets, melhor_score = resultado
    if len(melhores_offsets) > 1:
        print('Os melhores conjuntos de offsets são:')
    else:
        print('Os melhores offsets são:')
    
    for offsets in melhores_offsets:
        snips = [s[p : p + tam_motif] for p, s in zip(offsets, seqs)]
        print(offsets, '---->', snips)
    
    print('Com score de:', melhor_score)
