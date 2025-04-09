from prettytable import PrettyTable

class Automata:

    def __init__(self, pattern,sequence):

        if not pattern or len(pattern) < 2:
            raise ValueError("O padrão deve conter pelo menos dois caracteres.")
        
        self.pattern = pattern
        self.sequence = sequence
        self.alphabet = sorted(set(pattern))
        self.m = len(pattern)
        self.states = list(range(self.m + 1))
        self.transition_table = self.build_transition_table()
        self.matches = self.find_matches()
        self.table = self.print_table()

    def max_overlap(self, s1, s2):
        """
        Função auxiliar da build_transition_table
        Retorna o tamanho máximo de overlap entre o sufixo de s1 e o prefixo de s2

        """
        max_len = min(len(s1), len(s2)) #Calcula o comprimento máximo possível de sobreposição entre o sufixo da string s1 e o prefixo da string s2.
        for i in range(max_len, 0, -1): #Verifica, do maior para o menor, o tamanho possível de sobreposição entre s1 e s2.
            if s1[-i:] == s2[:i]:
                return i #Retorna o tamanho da sobreposição.
        return 0 #Caso não haja sobreposição retorna 0.

    def build_transition_table(self):
        """
        Constrói a table de transições

        """
        table = {} #Inicializa o dicionário
        for q in self.states: #Itera sobre todos os estados possíveis do autómato.
            for a in self.alphabet: #Para cada símbolo no alfabeto, calcula a próxima transição.
                prefix = self.pattern[:q] + a #Pega nos elementos do padrão até o estado q e adiciona o elemento a.
                next_state = self.max_overlap(prefix, self.pattern) #Calcula o próximo estado com base na maior sobreposição entre o prefixo e o padrão.
                table[(q, a)] = next_state # Registra a transição na table.
        return table #retorna a table completa das transições.

    def process_sequence(self):
        """
        Aplica o AF a uma sequência e retorna a lista de estados

        """
        current_state = 0 #Define o estado inicial, 0.
        state_list = [current_state] # Inicializa a lista já com o estado inicial, 0.
        for symbol in self.sequence: #Itera sobre cada símbolo da sequência de entrada.
            current_state = self.transition_table.get((current_state, symbol), 0) #Verifica na table de transições para saber qual estado ir a partir da posição e simbolo atual. Se o sibolo não estiver no alfabeto volta para o estado 0.
            state_list.append(current_state) #Adiciona o novo estado à lista de estados.
        return state_list #Retorna a lista completa de estados

    def find_matches(self):
        """
        Retorna a lista de posições onde o padrão foi encontrado na sequência

        """
        states = self.process_sequence( ) #Executa o autómato sobre a sequência, obtendo a lista de estados.
        match_positions = [] #Inicializa a lista de matches.
        for i, state in enumerate(states): #Percorre a lista de estados com os respectivos índices.
            if state == self.m:
                match_positions.append(i - self.m) #Calcula a posição inicial da ocorrência do padrão.
        return match_positions #Retorna a lista de posições onde o padrão ocorre na sequência.

    def print_table(self): #Não precisas testar esta função, é só para imprimir a tabela de maneira melhor

        states = self.process_sequence()
        occurrences = self.find_matches()

        table = PrettyTable()
        table.field_names = ["Index"] + list(range(len(self.sequence)))

        seq_lines = ["Sequence"] + list(self.sequence)
        table.add_row(seq_lines)

        state_lines = ["State"] + states[1:]
        table.add_row(state_lines)

        occurrence_lines = ["Occurrence"]
        for i in range(len(self.sequence)):
            if i in occurrences:
                occurrence_lines.append(str(i))
            else:
                occurrence_lines.append("")
        table.add_row(occurrence_lines)

        return table

#Exemplo
teste = Automata("ACA", "CACAACAAACA")
print(teste.alphabet)
print(teste.matches)
print(teste.transition_table)
print(teste.table)
