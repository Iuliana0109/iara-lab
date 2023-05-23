# Topic: Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Iuliana Stețenco

----
## Overview
In formal language theory, a context-free grammar, G, is said to be in Chomsky normal form (first described by Noam Chomsky)[1] if all of its production rules are of the form:

A → BC,   or
A → a,   or
S → ε,
where A, B, and C are nonterminal symbols, the letter a is a terminal symbol 

To convert a grammar to Chomsky normal form, a sequence of simple transformations is applied in a certain order:
1. Eliminate the start symbol from right-hand sides. Introduce a new start symbol, and a new rule
2. Eliminate rules with nonsolitary terminals
3. Eliminate right-hand sides with more than 2 nonterminals
Replace each rule
4. Eliminate ε-rules
5. Eliminate unit rules


## Objectives:
1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    a. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    b. The implemented functionality needs executed and tested.
    c. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    d. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation:

In order to transform my grammar into CNF I made severa functions, according to each step from the overview. Firstly, we need to assign a new starter symbol: 

```python
def new_start(self):
    for i in self.P:
        for j in self.P[i]:
            for k in j: 
                if self.start_symbol == k:
                    self.P['0'] = self.start_symbol
                    self.start_symbol = '0'
                    return
```
In order to eliminate the rules wiith nonsolitary terminals (unreachable) will be used a queue that checks if the terminals are reachable and if not, it deletes them. 

```python
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
```
After that, we have to remove all the apsilon transitions. for that, we loop through the dictionary of productons and looks for epsilon productions. After finding one, it loks for a rule that caan replace the epsilon that is associated to the same symbol.
```python
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
```
 After that, we need to remove the unit productions. The function looks for units and merges the productions of nonterminals connected by unit productions. After that iterates through the productions, categorizes them as unit or non-unit, and updates the set of productions accordingly.
```python
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
```

 In order to remove the productions of type A -> aB, we replace them in the following way: A -> aB, X -> a, therefore A -> XB.
```python
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
```
## Output
```
S  ->  bA
S  ->  BC
A  ->  a
A  ->  aS
A  ->  bCaCa
B  ->  A
B  ->  bS
B  ->  bCAa
C  ->  AB
C  ->  aS
C  ->  bCaCa
C  ->  
D  ->  AB
========================================================
If the starting string S is on the right hand side of any production, adds a new starting nonterminal
S  ->  bA
S  ->  BC
A  ->  a
A  ->  aS
A  ->  bCaCa
B  ->  A
B  ->  bS
B  ->  bCAa
C  ->  AB
C  ->  aS
C  ->  bCaCa
C  ->  
D  ->  AB
0  ->  S
========================================================
Removed the unreachable nonterminals
S  ->  bA
S  ->  BC
A  ->  a
A  ->  aS
A  ->  bCaCa
B  ->  A
B  ->  bS
B  ->  bCAa
C  ->  AB
C  ->  aS
C  ->  bCaCa
C  ->  
========================================================
Removed the epsilon producitons
S  ->  bA
S  ->  BC
S  ->  B
A  ->  a
A  ->  aS
A  ->  bCaCa
A  ->  bCa
A  ->  bCa
A  ->  b
A  ->  b
B  ->  A
B  ->  bS
B  ->  bCAa
B  ->  b
C  ->  AB
C  ->  aS
C  ->  bCaCa
C  ->  bCa
C  ->  bCa
C  ->  b
C  ->  b
========================================================
Removed the unit productions
S  ->  bA
S  ->  BC
S  ->  bS
S  ->  bCAa
S  ->  b
A  ->  a
A  ->  aS
A  ->  bCaCa
A  ->  bCa
A  ->  bCa
A  ->  b
A  ->  b
B  ->  bS
B  ->  bCAa
B  ->  b
C  ->  AB
C  ->  aS
C  ->  bCaCa
C  ->  bCa
C  ->  bCa
C  ->  b
C  ->  b

```

## Conclusion
During my lab work, I gained knowledge about Noam Chomsky's normal form and how to convert a Context Free Grammar into Chomsky Normal Form. I applied this knowledge by writing a Python code to perform the transition