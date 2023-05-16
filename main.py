import Grammar

productions = {
            'S': ['bA', 'BC'],
            'A': ['a', 'aS', 'bCaCa'],
            'B': ['A', 'bS', 'bCAa'],
            'C': ['AB', 'aS', 'bCaCa', ''],
            'D': ['AB']
}

grm = Grammar(productions)
grm.print_steps()
grm.to_cnf()