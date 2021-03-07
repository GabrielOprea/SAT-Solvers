import time

#the class for a tree node, which contains an information field,
#the literal used, references to its sons and a boolean satisfiability field
class Node:
    def __init__(self, info):
        self.info = info
        self.literal = None
        self.left = None
        self.right = None
        self.satisfiable = False
        

#auxiliary function for converting an expression to the FNC matrix,
#using a list with all the literals
def expr_to_mat(all_literals, expr):
    result_mat = []

    clauses = expr.split('^')
    for i in range(0, len(clauses)):
        crt_clause = []
        #extract all the literals from each clause
        literals = clauses[i].replace('(', '').replace(')', '').split('V')
        for j in range(0, len(all_literals)):
            #check if each literal is present in the clause, either in direct
            #or negated form
            direct = str(all_literals[j])
            negated = '~' + direct
            if direct in literals:
                crt_clause.append(1)
            elif negated in literals:
                crt_clause.append(-1)
            else:
                crt_clause.append(0)
        result_mat.append(crt_clause)
    return result_mat


#main BDD function
def BDD(expr):
    #extract a list with all the literals present in the expression
    #including duplicates
    all_literals = (expr.replace('V',' ').replace('(','')
    .replace(')','').replace('~', '').replace('^', ' ')
    .split())

    #convert this list of strings to a list of integers, then remove
    #the duplicates, and sort it in ascending order
    all_literals = list(set(map(int, all_literals)))
    all_literals.sort()

    #convert the expression to FNC matrix form
    expr_mat = expr_to_mat(all_literals, expr)

    root = BDD_aux(all_literals, 0, expr_mat)
    return int(root.satisfiable)

#auxiliary function for solving the BDD-SAT problem
def BDD_aux(all_literals, index, expr):
    crt_node = Node(expr)
    
    #if the partial matrix is empty(all the clauses have been satisfied),
    #then set the satisfiable field as true and return the node
    if expr == []:
        crt_node.satisfiable = True
        return crt_node
    
    #stop condition
    if len(expr[0]) == index:
        crt_node.satisfiable = False
        return crt_node
      
    crt_node.literal = all_literals[index]
        
    #partial matrices for left and right children, which contain the clauses
    #that have not yet been satisfied
    left_expr = [l for l in expr if l[index] != 1]
    right_expr = [l for l in expr if l[index] != -1]
    
    index += 1
    crt_node.left = BDD_aux(all_literals, index, left_expr)
    crt_node.right = BDD_aux(all_literals, index, right_expr)
    
    #calculate the satisfiability of the current node
    crt_node.satisfiable = crt_node.left.satisfiable|crt_node.right.satisfiable
        
    return crt_node

#main FNC function
def FNC(expr):
    #extract all the literals from the expression in a list,
    #including duplicates
    all_literals = (expr.replace('V',' ').replace('(','')
    .replace(')','').replace('~', '').replace('^', ' ')
    .split())

    #convert the strings to integers and eliminate the duplicates
    all_literals = list(set(map(int, all_literals)))
    all_literals.sort()

    #convert the expression to its matrix form
    result_mat = expr_to_mat(all_literals, expr)
    
    return int(generate_sol(result_mat))

#check function in the backtracking algorithm
def generate_sol_check(variable_mat, solution):
    #iterate through each clause
    for clause in variable_mat:
        found = False
        #if at least one literal is the same in both the clause
        #and in the generated solution, then the solution is correct
        for (i,j) in zip(clause, solution):
            if i == j:
                found = True
                break

        if not found:
            return False

    return True


def generate_sol_bt(variable_mat, solution, no_literals):

    #check if the solution has the required number of literals
    if no_literals == len(solution):
        return generate_sol_check(variable_mat, solution)

    #generate all lists of 5 elements, with the values 1 or -1
    for literal in [-1, 1]:

        solution.append(literal)

        if generate_sol_bt(variable_mat, solution, no_literals):
            return True
        del solution[-1]

    return False


def generate_sol(variable_mat):
    #the initial solution is empty, and the required size is the number
    #of columns in the matrix representation
    return generate_sol_bt(variable_mat, [], len(variable_mat[0]))

	
def main():
	for i in range(0, 10):
		f = open("checker/input0" + str(i) + ".txt", "r")
		expr = f.read()
		no_var = len(expr.replace('V', ' ').replace('^', ' ').split(' '))
		start = time.time()
		BDD(expr)
		end = time.time()
		print(no_var, sep = " ", end = " ")
		print(end-start)
		
if __name__ == "__main__":
	main()
