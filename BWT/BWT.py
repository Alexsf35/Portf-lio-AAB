class BWT:
    def __init__(self, seq="", buildsufarray=False, encoded=False):
        """
        Initialize the BWT class.
        If encoded is True, sets self.bwt to the given sequence.
        Otherwise, builds the BWT and optionally the suffix array.
        """
        self.seq = seq

        if encoded:
            self.bwt = seq  # The input is already a BWT string
        elif seq:
            self.bwt = self.build_bwt(seq, buildsufarray)
        else:
            self.bwt = ""


    def build_bwt(self, text, buildsufarray=False):
        """
        Constructs the Burrows-Wheeler Transform (BWT) of the given text.
        """
        rotations = [] #Inicializa a lista
        for i in range(len(text)):
            rotation = text[i:] + text[:i] # Criar uma rotação movendo os primeiros i caracteres para o fim
            rotations.append(rotation) # Adicionar a rotação à lista

        rotations.sort() # Ordenar todas as rotações por ordem alfabética
        self.rotations = rotations  # Guardar a matriz de rotações ordenadas

        result = "" #Inicializar a string que irá conter o resultado da transformação BWT
        for row in rotations:
            result += row[-1]  # Adicionar o último caractere de cada linha da matriz à string resultante

        if buildsufarray: # Se for pedido para construir o array de sufixos
            self.sa = [] # Inicializar o array de sufixos
            for row in rotations:
                pos = row.index('$') # Encontrar a posição do símbolo terminal '$' na rotação
                self.sa.append(len(text) - pos - 1) # Calcular e guardar a posição original do sufixo

        return result # Devolver a string transformada pela BWT

    def set_bwt(self, bwt_string):
        """
        Manually sets the BWT (used when starting from an already transformed string).
        """
        self.bwt = bwt_string

    def get_first_col(self):
        """
        Returns the first column.
        """
        first_col = [] # Lista para guardar os caracteres da primeira coluna da matriz BWT
        for c in self.bwt:
            first_col.append(c) # Copiar cada caractere da BWT (última coluna) para a lista
        first_col.sort() # Ordenar a lista de forma lexicográfica para obter a primeira coluna
        return first_col # Devolver a primeira coluna da matriz (ordenada)

    def find_ith_occ(self, l, elem, index):
        """
        Finds the index of the i-th occurrence of elem in list l.
        """
        count = 0 # Contador para mostrar o número de ocorrências encontradas
        for i in range(len(l)):
            if l[i] == elem: # Verifica se o elemento atual corresponde ao procurado
                count += 1 # Aumenta o contador de ocorrências
                if count == index:
                    return i
        return -1

    def inverse_bwt(self):
        """
        Reconstructs the original string from the BWT.
        """
        first_col = self.get_first_col() # Obtemos a primeira coluna da matriz BWT
        result = "" # Inicializamos uma string vazia para reconstruir a sequência original
        c = "$" # Começamos a reconstrução a partir do símbolo terminal '$'
        occ = 1 # Consideramos a primeira ocorrência do símbolo '$'

        for _ in range(len(self.bwt)):
            pos = self.find_ith_occ(self.bwt, c, occ) # Encontramos a posição da ocorrência atual de 'c' na coluna BWT
            c = first_col[pos] # Saltamos para o caractere correspondente na mesma linha da primeira coluna
            occ = 1 # Reiniciamos o número de ocorrência a contar para o próximo símbolo
            k = pos - 1
            while k >= 0 and first_col[k] == c: # Contamos quantas vezes o novo símbolo já apareceu acima, na primeira coluna
                occ += 1
                k -= 1
            result += c # Adicionamos o novo símbolo à sequência reconstruída

        return result

    def last_to_first(self):
        """
        Computes the last-to-first mapping used in backward search.
        """
        first_col = self.get_first_col() # Obtemos a primeira coluna da matriz BWT
        result = [] # Lista onde vamos guardar o mapeamento

        for i in range(len(self.bwt)):
            c = self.bwt[i] # Caractere atual da última coluna
            occ_num = 1 # Vamos contar quantas vezes já vimos este caractere até esta posição
            for j in range(i):
                if self.bwt[j] == c:
                    occ_num += 1 # Incrementamos a contagem de ocorrências anteriores do mesmo caractere
            pos = self.find_ith_occ(first_col, c, occ_num) # Encontramos a posição correspondente na primeira coluna
            result.append(pos) # Adicionamos essa posição à lista de mapeamento

        return result

    def bw_matching(self, pattern):
        """
        Backward search for a pattern using the BWT.
        Returns the list of row indices where the pattern matches.
        """
        lf = self.last_to_first() # Obtemos o mapeamento "last-to-first" da BWT
        top = 0  # Índice inicial do intervalo de pesquisa
        bottom = len(self.bwt) - 1 # Índice final do intervalo de pesquisa


        while top <= bottom: # Continuamos enquanto o intervalo for válido
            if pattern:  # Se ainda houver caracteres no padrão a procurar
                symbol = pattern[-1] # Vamos verificar o último caractere do padrão
                pattern = pattern[:-1] # Removemos o último caractere do padrão
                lmat = [] # Lista com os símbolos da coluna BWT entre top e bottom
                for i in range(top, bottom + 1):
                    lmat.append(self.bwt[i]) # Adicionamos cada caractere da BWT dentro do intervalo ao lmat

                if symbol in lmat: # Se o símbolo procurado estiver presente no intervalo atual
                    top_index = lmat.index(symbol) + top # Primeiro índice onde o símbolo aparece
                    bottom_index = bottom - lmat[::-1].index(symbol) # Último índice onde o símbolo aparece
                    top = lf[top_index] # Atualizamos o top usando o mapeamento LF
                    bottom = lf[bottom_index] # Atualizamos o bottom usando o mapeamento LF
                else:
                    return [] # Se o símbolo não for encontrado, o padrão não ocorre — devolvemos lista vazia
            else:
                matches = [] # Lista para guardar os índices onde o padrão ocorre
                for i in range(top, bottom + 1):
                    matches.append(i) # Adicionamos todos os índices possíveis onde o padrão ocorre
                return matches

        return [] # Caso o ciclo termine sem encontrar, devolvemos lista vazia

    def bw_matching_pos(self, pattern):
        """
        Returns the positions from the suffix array where the pattern occurs.
        """
        if not hasattr(self, 'sa'):
            raise ValueError("Suffix array not built.")

        result = [] #Inicializa a lista
        matches = self.bw_matching(pattern) # Obtemos as linhas da matriz BWT onde o padrão foi encontrado
        for m in matches:
            result.append(self.sa[m]) # Para cada linha correspondente, obtemos a posição original a partir do array de sufixos
        result.sort() # Ordenamos as posições para devolver os resultados por ordem crescente
        return result # Devolvemos a lista de posições onde o padrão ocorre na sequência original

    def show_bwt_matrix(self):
        """
        Prints the full BWT matrix (sorted rotations of the original sequence).
        """
        if hasattr(self, 'rotations'):
            for row in self.rotations:
                print(row)
        else:
            print("BWT matrix not available. Build BWT first.")

# 🧪 Test the implementation
if __name__ == "__main__":
    seq = "TAGACAGAGA$"
    bwt_obj = BWT(seq, buildsufarray=True)

    print("BWT:", bwt_obj.bwt) 
    print("Inverse BWT:", bwt_obj.inverse_bwt())  
    print("Pattern matches for 'AGA':", bwt_obj.bw_matching_pos("AGA")) 
    print("BWT Matrix:")
    bwt_obj.show_bwt_matrix()


encoded = "AGGGTCAAAA$"
bwt_decoded = BWT(encoded, encoded=True)
original = bwt_decoded.inverse_bwt()
print(original) 
