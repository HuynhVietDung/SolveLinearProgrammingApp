import numpy as np

def transfer_to_standard_form(n_var, n_constraint, func_type, func_coef, constraints, constraint_signs, variable_cons):
    '''
        Function transfers form orginal form into stard form of linear programming problem
    Input:
        n_var: number of varialbes
        n_constraint: number of contraints of equality/inequality
        func_type: Type of objective function ("Maximize", "Minimize")
        func_coef: coefficient of equality/inequality constraints
        constraint_signs: sign of equality/inequality constraints ("<=", ">=", "=") 
        variable_cons: constraints of variables ("<= 0", ">= 0", "Free")
    Output:
        A: stardard form
        free_var: list including indeces of free variables  
    '''

    # transfer from maximize to minimize
    if func_type == "Maximize":

        func_type = "Minimize"
        func_coef = [- coef for coef in func_coef]

    # transfer all constraints sign ">=" to "<="
    for i in range(n_constraint):
        if constraint_signs[i] == ">=":
            constraints[i] =  [- coef for coef in constraints[i]]

    # complement slack variables
    for i in range(n_constraint):
        slack_coef = [0.0 for k in range(n_constraint)] 
        if constraint_signs[i] != '=':
            slack_coef[i] = 1.0
        slack_coef.reverse()

        for coef in  slack_coef:
            constraints[i].insert(n_var, coef)

    free_var = []

    for i in range(n_var):
        # transfer negative variable into positive variables
        if variable_cons[i] == "<= 0":
            for constraint in constraints:
                constraint[i] = -1*constraint[i]

        # transfer each free variable into two positives variables   
        elif variable_cons[i] == 'Free':
            for constraint in constraints:
                constraint.insert(i + 1, -constraint[i])
            l = len(free_var)
            free_var.append(i + l)


    for i in range(len(constraints[0]) - n_var):
        func_coef.append(0)

    A = []
    A.append(func_coef)
    for constraint in constraints:
        A.append(constraint)
    
    A = np.array(A, dtype = float)
    return A, free_var

    

def pivot_operation(A):
    '''
        Function finds optimal tableau
    Input:
        A: original tableau
    Output:
        B: optimal tableau
    '''
    while np.any(A[0,:-1] < 0):
        # find pivot column
        pivot_col = np.where(A[0] == min(A[0,:-1]))[0][0]

        # check whether all ai < 0
        if np.all(A[:, pivot_col] < 0):
            #sys.exit("Ham Muc tieu khong gioi noi tren mien chap nhan duoc.\nBai toan Vo nghiem'")
            return None
        
        # find pivot row
        pivot_row = 1
        for i in range(1, A.shape[0]):
            if A[i, pivot_col] < 0:
                continue
            try: 
                frac = A[i, pivot_col]/A[i,-1]
            except ZeroDivisionError:
                frac = 1.00e100

            if frac > A[pivot_row, pivot_col]/A[pivot_row, -1]:
                    pivot_row = i
        # Pivot element
        pivot = A[pivot_row, pivot_col]

        # Pivot Operation
        A[pivot_row, :] = A[pivot_row, :]/pivot

        for i in range(A.shape[0]):
            if i == pivot_row:
                continue
            A[i, :] = A[i, :] - A[i, pivot_col]*A[pivot_row, :]

    return A



def simplex_algorithm(n_var, A,  free_var = [], func_type = 'Minimize'):
    '''
        Function using Simplex algotithm of Danzig finds solution for linear programming problems.
    Input: 
        n_var: number of original variables.
        A: original tableau.
        free_var: python list include indeces of free variables. 
        func_type: type of objective function
    Output:
        A: optimal tableau
        z: optimal value
        solver: optimal soluitons 
    '''

    # check is there any b_i <0 
    if np.any(A[1:,-1] < 0):
        #os.system('cls' if os.name == 'nt' else 'clear')
        #sys.exit("Ton tai b < 0. Khong the thuc hien thuat toan don hinh. Hay dung thuat toan 2 pha de giai")
        return None, None, None


    # pivot operation
    A = pivot_operation(A)
    if not isinstance(A, np.ndarray):
        return None, None, None

    # get solution
    index = np.where(A[0,:-1] == 0)[0]
    solver = [0 for i in range(A.shape[1] - 1)]
    

    for i in index:
        j = np.where(A[:,i] == 1)[0]
        if j.any() != True:
            solver[i] = 1.00e100
        else:
            idx = j[0]
            solver[i] = A[idx, -1]
    

    if len(free_var) != 0:
        for i in free_var:
            solver[i] = solver[i] - solver[i + 1]
        k = 0
        for i in free_var:
            solver.remove(solver[i + 1 - k])
            k += 1
    
    # get optimal value
    if func_type == 'Minimize':
        z = -A[0, -1]
    else:
        z = A[0, -1]
        
    return  A, z, solver[:n_var]


def build_complementary_problem(A):
    '''
        Function builds complementary problem from original problem 
    Input:
        A: original tableau
    Output:
        B: taleau of complementary problem
    '''
    dim = A.shape
    
    z_new = np.zeros(dim[1] + 1)
    z_new[-2] = 1.0
    
    B = A[1:,:].copy()
    B = np.vstack((z_new, np.insert(B, -1, -1, axis = 1)))
    return B


def solve_complementary_problem(B):
    '''
       Function solves complementary problem.
    Input:
        n_var: number of original varialbes
        B: tableau of complementary problem
    Output:
        B: optimal tableau of complementary problem
    '''
    z_new = B[0,:].copy()
    
    # pivot column
    pivot_col = -2 
    
    # pivot row
    pivot_row =  np.where(B[:,-1] == min(B[:,-1]))[0][0]

    
    # pivot element
    pivot = B[pivot_row, pivot_col]

    # Thuc hien phep xoay ban dau
    B[pivot_row, :] = B[pivot_row, :]/pivot

    for i in range(B.shape[0]):
        if i == pivot_row:
            continue
        B[i, :] = B[i, :] - B[i, pivot_col]*B[pivot_row, :]
 
    B = pivot_operation(B)
    if not isinstance(B, np.ndarray):
        return None

    # if only x0 exists on objective function
    if (B[0,:] == z_new).all():
        return B
    else:
        #os.system('cls' if os.name == 'nt' else 'clear')
        #sys.exit("Tu vung toi uu cua bai toan bo tro xuat hien cac bien khac tren ham muc tieu. Bai toan Vo nghiem'")   
        return None 


def simplex_phases_2(B, z):
    '''
        Function makes phase 2 of simplex algorithm
    Input:  
        B: tableau of complementary problem
        z: original objective function
    Output:
        B: new tableau(new objective function and new constraints)
    '''

    # remove column of x0
    B = np.delete(B, -2, 1)
    
    # new objective function
    z_new = B[0]

    index_col = np.where(z != 0)[0]

    for i in index_col:
        if len(np.where(B[1:, i] == 1)[0]) == 0:
            temp = np.zeros(len(B[0]), dtype = float)
            temp[i] = 1.0
            z_new += temp
            continue
        index_row = np.where(B[1:, i] == 1)[0][0] + 1
        
        row = B[index_row, :].copy()
        for j in range(len(B[0])):
            if j == i:
                row[j] = 0.0
                continue
            row[j] *= -1
            
        z_new += row*z[i]
    
    # new tableau
    B[0] = z_new    
    return B


def simplex_2_phases_algorithm(n_var, A, free_var = [], func_type = 'Minimize'):
    '''
        Function using Simplex 2 phase algotithm finds optimal solution for linear programming problems.
    Input: 
        n_var: number of original variables.
        A: original tableau.
        free_var: python list include indeces of free variables. 
        func_type: type of objective function
        solvable: flag using to check problem is solvable or not
        err_name:
    Output:
        A: optimal tableau
        z: optimal value
        solver: optimal solution
    '''
    # get original objective function
    z = A[0].copy()

    # build and solve complementary problem
    B = build_complementary_problem(A)
    
    B = solve_complementary_problem(B)
    
    if not isinstance(B, np.ndarray):
        return None, None, None
    # if complementary problem is solvable => phase 2
    B = simplex_phases_2(B, z)
    if not isinstance(B, np.ndarray):
        return None, None, None

    # using simplex algorithm to find optimal solution
    return simplex_algorithm(n_var, B, free_var, func_type)

def solve_linear_programming_problem(n_var, A, free_var = [], func_type = 'min'):
    '''
        Function summarizing all linear programming algorithm solves any linear programing problem 
    Input:
        n_var: number of original variables.
        A: original tableau.
        free_var: python list include indeces of free variables. 
        func_type: type of objective function
    Output:
        A: optimal tableau
        z: optimal value
        solver: optimal solution
    '''
    
    if not np.any(A[1:,-1] < 0):
        B, z, solver = simplex_algorithm(n_var, A, free_var, func_type) 
    else: 
        B, z, solver = simplex_2_phases_algorithm(n_var, A, free_var, func_type) 

    if not isinstance(B, np.ndarray):
        print("Cannot find the optimal solutions.")
    else: 
        return B, z, solver 
