import copy
import random

class Grammar:

    
    def __init__(self, P):
        self.P = P
        self.is_cnf = False
        self.start_symbol = 'S'

    def check_string(self, string):
        for i in range (len(string)):
            if string[i] in self.P.keys():
                return "false"
        return "true"
    
    def generate_string(self):
        new_str = self.starter_symbol

        j = len(new_str) - 1
        while (self.check_string(new_str) == "false"):
            if new_str[j] in self.rules.keys():
                new_str = new_str[0:j] + random.choice(self.rules[new_str[j]])
                j = len(new_str) - 1
        return new_str
    
    def new_start(self):
        for i in self.P:
            for j in self.P[i]:
                for k in j: 
                    if self.start_symbol == k:
                        self.P['0'] = self.start_symbol
                        self.start_symbol = '0'
                        return
        

    def remove_nonsolitary(self, nonterminal):
        visited = []  
        queue = []

        queue.append('S')
        visited.append('S')
        
        while queue:
            m = queue.pop(0)
            for neighbour in self.P[m]:
                for letter in neighbour:
                    if letter in nonterminal:
                        if letter not in visited:
                            visited.append(letter)
                            queue.append(letter)

        for i in list(self.P):
            if i not in visited:
                del self.P[i]    

    def remove_epsilon(self):
        nullable = []
        for i in self.P:
            for j in self.P[i]:
                if j == '':
                    nullable.append(i)
                    self.P[i].remove(j)
        
        for i in self.P:
            for j in self.P[i]:
                for k in j:
                    if k in nullable:
                        self.P[i].append(j[:j.rfind(k)])
                        

    def remove_units(self, nonterminal):
        g = {}
        for i in self.P:
            for j in self.P[i]:
                g_keys = []
                guf_keys = []

                if len(j) == 1 and j in nonterminal:
                    g_keys.append(j)
                    self.P[i].remove(j)
                else:
                    guf_keys.append(j)

            if g_keys:
                g[i] = g_keys

        for i in g:
            for j in g[i]:
                temp = self.P[i] + self.P[j]
                self.P[i] = temp

    def remove_other(self, terminal, upper_alphabet):
        new_rules = {}
        for i in terminal:
            new_key = random.choice(upper_alphabet)
            upper_alphabet.remove(new_key)
            self.P[new_key] = [i]
            new_rules[i] = new_key
        remove_dict = {}

        for i in self.P:
            remove_list = []
            for j in self.P[i]:
                if len(j)>1:
                    for k in j:
                        if k in terminal:
                            new_str = j[:j.find(k)] + new_rules[k] +j[j.find(k)+1]
                            self.P[i].append(new_str)
                            remove_dict[i] = []
                            remove_list.append(j)
            remove_dict[i] = remove_list

        for i in remove_dict:
            for j in remove_dict[i]:
                if j in self.P[i]:
                    self.P[i].remove(j)


    def print_steps(self):
        for i in self.P:
            for j in self.P[i]:
                print(i, " -> ", j)
                
    def to_cnf(self):
        self.new_start()
        print("Add a new starting nonterminal")
        self.print_steps()
        nonterminal = []
        for i in self.P:
            nonterminal.append(i)

        self.remove_nonsolitary(nonterminal)
        print("Removed the unreachable nonterminals")
        self.print_steps()
        self.remove_epsilon()
        print("Removed the epsilon producitons")
        self.print_steps()
        # remove unit productions
        self.remove_units(nonterminal)
        print("Removed the unit productions")
        self.print_steps()
        # step3
        terminal = set()
        for i in self.P:
            for j in self.P[i]:
                for k in j:
                    if ord(k) <= ord('z') and ord(k) >= ord('a'):
                        terminal.add(k)

        upper_alphabet = []
        for i in range(ord('A'), ord('Z')):
            upper_alphabet.append(chr(i))

        for i in nonterminal[:]:
            if i in upper_alphabet:
                upper_alphabet.remove(i)

        self.remove_other(terminal, upper_alphabet)