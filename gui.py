import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from linear_programming_functions import *

# store data throughout program
class Data:
    """ a data entity shared by the forms"""
    def __init__(self):
        self.n_var = tk.IntVar()
        self.n_constraint = tk.IntVar()
        self.func_type = tk.StringVar()
        self.func = []
        self.constraints = []
        self.constraint_signs = []
        self.variable_constraints =  []

    @property
    def n_var(self):
        return self._n_var

    @n_var.setter
    def n_var(self, n_var):
        self._n_var = n_var

    @property
    def n_constraint(self):
        return self._n_constraint

    @n_constraint.setter
    def n_constraint(self, n_constraint):
        self._n_constraint = n_constraint
    
     

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.data = Data()

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(container, self, self.data)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.frames["StartPage"].button.config(command=self.get_and_move)

        self.frames["PageOne"].button.config(command= self.clear_and_move)
        self.frames["PageOne"].button_2.config(command= self.solve_and_move)

        self.frames["PageTwo"].button.config(command= self.back_to_start_page)
        self.show_frame("StartPage")


    # switch between frames
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


    # get input from Start Page and move to Page One
    def get_and_move(self):
        try:
            n_var = int(self.frames["StartPage"].nvar_input_entry.get())
            n_constraint = int(self.frames["StartPage"].nconstrain_input_entry.get())

            if n_var <= 1 or n_constraint < 1:
                messagebox.showerror("INPUT ERROR!", "Number of variables must be  >= 2 and number of constraints must be >= 1.")
            else:
                self.data.n_var.set(n_var) 
                self.data.n_constraint.set(n_constraint) 
                #print(self.data.n_var.get())
                #print(self.data.n_constraint.get())

                self.create_func_widget(self.data.n_var.get())
                self.create_constraint_widget(self.data.n_var.get(),self.data.n_constraint.get())
                self.create_variable_constraints_widget(self.data.n_var.get(),self.data.n_constraint.get())
                self.configure_width()
                self.show_frame("PageOne")

        except:
            messagebox.showerror("INPUT ERROR!", "Inputs must be interger numbers")

    ## create widgets in Page One when clicking "Continue" in StartPage
    def create_func_widget(self, n_var):
        row = 1
        col = 1
        for i in range(n_var):
            var_entry = tk.Entry(self.frames["PageOne"], width= 3)
            var_entry.grid(row= row, column= col)

            var_label = tk.Label(self.frames["PageOne"], text=f'X{i+1} +' if i != (n_var - 1) else f'X{i+1}',  width= 3, font=('Arial', 16))
            var_label.grid(row= row, column= col + 1)


            self.data.func.append(var_entry)
            col += 2

    def create_constraint_widget(self, n_var, n_constraint):
        row = 2

        label = tk.Label(self.frames["PageOne"], text= "Constraints: ", font=('Arial', 16))
        label.grid(row = 2, column=0)

        for i in range(n_constraint):
            col = 1
            ref = []

            for j in range(n_var):
                var_entry = tk.Entry(self.frames["PageOne"],  width= 3)
                var_entry.grid(row= row, column= col)

                var_label = tk.Label(self.frames["PageOne"], text= f'X{j+1} +' if j != (n_var - 1) else f'X{j+1}',  width= 3, font=('Arial', 16))
                var_label.grid(row= row, column= col + 1)

                ref.append(var_entry)
                col += 2
                   
            sign_str = tk.StringVar(value= '<=')
            sign_box = tk.OptionMenu(self.frames["PageOne"], sign_str,*['<=', '>=', '='])
            sign_box.config( fg='#333333', bg='#FFFFFF', font=('Arial', 16))

            sign_box.grid(row = row, column= col)
            self.data.constraint_signs.append(sign_str)

            entry = tk.Entry(self.frames["PageOne"], width= 3)
            entry.grid(row = row, column= col + 1)
            ref.append(entry)
            row += 1

            self.data.constraints.append(ref) 


    def create_variable_constraints_widget(self, n_var, n_constraint):
        row = 2 + n_constraint
        col = 1
        for i in range(n_var):
            var_label = tk.Label(self.frames["PageOne"], text=f'X{i+1}',  width= 3, font=('Arial', 16))
            var_label.grid(row= row, column= col)

            sign_str = tk.StringVar(value= '>= 0')
            sign_box = tk.OptionMenu(self.frames["PageOne"], sign_str, *['<= 0', '>= 0', 'Free'])
            sign_box.config( fg='#333333', bg='#FFFFFF', font=('Arial', 16))
            sign_box.grid(row = row, column= col + 1)

            self.data.variable_constraints.append(sign_str)
            col += 2

        self.frames["PageOne"].button.grid(row = row + 1, column = col, pady = 10)
        self.frames["PageOne"].button_2.grid(row = row + 1, column = col + 1, pady = 10)
    
    # configure window width in Page One
    def configure_width(self):
        obj_label_width = self.frames["PageOne"].obj_label.winfo_reqwidth()
        obj_width = self.frames["PageOne"].objective.winfo_reqwidth()
        
        constraint_width = sum(coef.winfo_reqwidth() for coef in self.data.constraints[0])
        
        new_width = (obj_label_width + obj_width + constraint_width)*2 + int((obj_label_width + obj_width + constraint_width)/4)
        self.geometry(f'{new_width}x440')

    # clear widgets in Page One and move to Start Page when click 'Back'
    def clear_and_move(self):
        # clear widgets
        for row in range(1, 3 + self.data.n_constraint.get()):
            for col in range(1, self.data.n_var.get()*2 + 3):
                for widget in self.frames["PageOne"].grid_slaves(row = row, column= col):
                    widget.destroy()

        self.data.func = []
        self.data.constraints = []
        self.data.constraint_signs = []
        self.data.variable_constraints = []

        self.geometry('740x440')
        # move to Start Page
        self.show_frame("StartPage")

    def back_to_start_page(self):
        for widget in self.frames["PageTwo"].pack_slaves():
            widget.pack_forget()

        self.clear_and_move()

    # solve problem and move to Page Two  
    def solve_and_move(self):
        n_var, n_constraint, func_type, func_coef, constraint_coef, cons_signs, var_con_list = self.get_input()

        if func_type != None and func_coef != None and constraint_coef != None and cons_signs != None and var_con_list != None: 
                
            A, free_var = transfer_to_standard_form(n_var, n_constraint, func_type, func_coef, constraint_coef, cons_signs, var_con_list)

            B, z, solution = solve_linear_programming_problem(n_var, A, free_var)

            if not isinstance(B, np.ndarray):  
                err_label =  tk.Label(self.frames["PageTwo"], text=  "Cannot find the optimal solutions.")
                err_label.pack()
            else:
                self.create_solution_widget(z, solution)

            self.geometry('740x440')
            self.frames["PageTwo"].button.pack()

            # switch to Page Two Frame  
            self.show_frame("PageTwo")
    
    # get input from Page One
    def get_input(self):
        try:
            # get number of variable and consstrains
            n_var = int(self.data.n_var.get())
            n_constraint = int(self.data.n_constraint.get())

            # get the type of objective function
            self.data.func_type.set(self.frames["PageOne"].func_str.get())
            func_type = self.data.func_type.get()

            # get coefficients of objective function
            func_coef = []
            for num in self.data.func:
                func_coef.append(float(num.get()))

            #print(func_coef)

            # get coefficients of constraints
            constraint_coef = []
            for constraint in self.data.constraints:
                l = []
                for i in constraint:
                    l.append(float(i.get()))
                constraint_coef.append(l)

            #print(constraint_coef)

            # get signs of constraints 
            cons_signs = []
            for sign in self.data.constraint_signs:
                cons_signs.append(str(sign.get()))

            #print(cons_signs)

            # get the constraints of variable
            var_con_list = []
            for var_con in self.data.variable_constraints:
                var_con_list.append(str(var_con.get()))

            #print(var_con_list)

            return n_var, n_constraint, func_type, func_coef, constraint_coef, cons_signs, var_con_list
        except:
            messagebox.showerror("INPUT ERROR!", "Inputs must be interger/float numbers not char/text or fractions !")
            return None, None, None, None, None, None, None


    # create widgets in Page Two
    def create_solution_widget(self, z, solution):
        z_label =  tk.Label(self.frames["PageTwo"], text= f'Optimal Value = {z}')
        z_label.pack()

        for i in range(len(solution)):
            solution_label =  tk.Label(self.frames["PageTwo"], text= f'X{i + 1} = {solution[i]}')
            solution_label.pack()
    

class StartPage(ttk.Frame):
    def __init__(self, parent, controller, data):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        title = tk.Label(self, text="WELLCOME TO MY APP", bg='#333333', fg='#FFFFFF', font=('Arial', 30))
        title.grid(row=0, column=1, columnspan=2, sticky='news', pady=40)

        self.nvar_input_label = tk.Label(self, text="Number of variables:", font=('Arial', 16))
        self.nvar_input_label.grid(row=1, column=0)

        self.nvar_input_entry = tk.Entry(self)
        self.nvar_input_entry.grid(row=1, column=1)

        waring_1 = tk.Label(self, text="(Number of variables >= 2)", font=('Arial', 16))
        waring_1.grid(row=2, column=0)

        self.nconstrain_input_label = tk.Label(self, text="Number of constrains:", font=('Arial', 16))
        self.nconstrain_input_label.grid(row=3, column=0)

        self.nconstrain_input_entry = tk.Entry(self)
        self.nconstrain_input_entry.grid(row=3, column=1)

        waring_2 = tk.Label(self, text="(Number of constraints >= 1)", font=('Arial', 16))
        waring_2.grid(row=4, column=0)

        self.button = tk.Button(self, text='Continue', fg='#333333', bg='#FFFFFF', font=('Arial', 16))
        self.button.grid(row=5, column=2,  pady = 30)


    
class PageOne(ttk.Frame):
    def __init__(self, parent, controller, data):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.data = data

        self.obj_label = tk.Label(self, text='Objective function', font=('Arial', 16))
        self.obj_label.grid(row= 0, column= 0, pady= 30)

        self.func_str = tk.StringVar()
        self.func_str.set('Maximize')
        self.objective = tk.OptionMenu(self, self.func_str, *['Maximize', 'Minimize'])
        self.objective.config( fg='#333333', bg='#FFFFFF', font=('Arial', 16))
        self.objective.grid(row= 0, column= 1, pady= 30)

        self.func_label = tk.Label(self, text='Function:', font=('Arial', 16))
        self.func_label.grid(row= 1, column= 0 ,pady=10)
        
        self.button = tk.Button(self, text="Back",  fg='#333333', bg='#FFFFFF', font=('Arial', 16))
        self.button.grid(row = 2, column = 2)

        self.button_2 = tk.Button(self, text="Continue",  fg='#333333', bg='#FFFFFF', font=('Arial', 16))
        self.button_2.grid(row = 2, column = 3)

class PageTwo(ttk.Frame):
    def __init__(self, parent, controller, data):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.button = tk.Button(self, text="Back to Start Page",  fg='#333333', bg='#FFFFFF', font=('Arial', 16))

