import math

EPSILON = 1e-5
DELTA = 1e-3
SEGMENTS = 100

# inverse constant
DEFAULT_INVE_UP_DOM = 2
DEFAULT_INVE_DOWN_DOM = -2
INCREASE_DOM_VAL = 2

def plot_func(graph, f, x0, x1, num_of_segments=SEGMENTS, c='black'):
    """
    plot f between x0 and x1 using num_of_segments straight lines.
    use the plot_line function in the graph object. 
    f will be plotted to the screen with color c.
    """
    STEP = (x1-x0)/num_of_segments
    # first two points in the graph
    point1 = (x0, f(x0))
    point2 = (x0+STEP, f(x0+STEP))
    for segment in range(num_of_segments):
        graph.plot_line(point1,point2,c)
        point1 = point2
        point2 = (point1[0]+STEP, f(point1[0]+STEP))


def const_function(c):
    """return the mathematical function f such that f(x) = c
    >>> const_function(2)(2)
    2
    >>> const_function(4)(2)
    4
    """
    f = lambda x: c
    return f


def identity():
    """return the mathematical function f such that f(x) = x
    >>>identity()(3)
    3
    """
    f = lambda x: x
    return f


def sin_function():
    """return the mathematical function f such that f(x) = sin(x)
    >>> sinF()(math.pi/2)
    1.0
    """
    f = lambda x: math.sin(x)
    return f

def sum_functions(g, h):
    """return f s.t. f(x) = g(x)+h(x)"""
    f = lambda x: g(x)+h(x)
    return f


def sub_functions(g, h):
    """return f s.t. f(x) = g(x)-h(x)"""
    f = lambda x: g(x)-h(x)
    return f


def mul_functions(g, h):
    """return f s.t. f(x) = g(x)*h(x)"""
    f = lambda x: g(x)*h(x)
    return f

def div_functions(g, h):
    """return f s.t. f(x) = g(x)/h(x)"""
    f = lambda x: g(x)/h(x)
    return f

    # The function solve assumes that f is continuous.
    # solve return None in case of no solution
def solve(f, x0=-10000, x1=10000, epsilon=EPSILON):
    """return the solution to f in the range between x0 and x1"""
    UP = False

    if f(x0)*f(x1)>0:
        return None
    # check if the function is monotonically increasing
    if f(x0)<f(x1):
        UP = True

    left = x0
    right = x1

    # version of binary search to find the requested value of 'x'
    while (left <= right):
        middle_x = (left+right)/2
        y_value = f(middle_x)
        if abs(y_value) < epsilon:
            return middle_x
        elif y_value > epsilon:
            if UP:
                right = middle_x
            else:
                left = middle_x
        else:
            if UP:
                left = middle_x
            else:
                right = middle_x
    # x value doesn't exist - return None
    return None



    # inverse assumes that g is continuous and monotonic. 
def inverse(g, epsilon=EPSILON):
    """return f s.t. f(g(x)) = x"""
    def f(x):
        x0 = DEFAULT_INVE_DOWN_DOM
        x1 = DEFAULT_INVE_UP_DOM

        f_help = sub_functions(g,const_function(x))

        # check if the function is monotonically increasing
        if f_help(x0) < f_help(x1):
            UP = True
        else:
            UP = False

        sol = solve(f_help,x0,x1,epsilon)

        while sol == None:
            sol = solve(f_help,x0,x1,epsilon)
            if f_help(x0) > 0:
                if UP:
                    x0 *= INCREASE_DOM_VAL
                else:
                    x1 *= INCREASE_DOM_VAL
            else: # negative value to the function in x0
                if UP:
                    x1 *= INCREASE_DOM_VAL
                else:
                    x0 *= INCREASE_DOM_VAL
        return sol

    return f


def compose(g, h):
    """return the f which is the compose of g and h """
    f = lambda x: g(h(x))
    return f


def derivative(g, delta=DELTA):
    """return f s.t. f(x) = g'(x)"""
    derivative = lambda x: (g(x + delta)- g(x)) / delta
    return derivative


def definite_integral(f, x0, x1, num_of_segments=SEGMENTS):
    """
    return a float - the definite_integral of f between x0 and x1
    >>>definite_integral(const_function(3),-2,3)
    15
    """
    STEP = (x1-x0)/num_of_segments
    integral = 0
    # first two points in the graph
    x_1 = x0
    x_2 = x0+STEP
    for segment in range(num_of_segments):
        # according to the given formula
        integral += f((x_1+x_2)/2)*(x_2 - x_1)
        x_1 = x_2
        x_2 += STEP
    return integral


def integral_function(f, delta=0.01):
    """return F such that F'(x) = f(x)"""
    def integ(x):
        num_of_seg = math.ceil(abs(x)/delta)
        if x == 0:
            return 0
        elif x > 0:
            return definite_integral(f,0,x,num_of_seg)
        else:
            return (definite_integral(f,x,0,num_of_seg))*-1
    return integ




def ex11_func_list():
    """return a list of functions as a solution to q.12"""
    func_list = []
    f0 = const_function(4)
    f1 = sum_functions(sin_function(),f0)
    f2 = compose(sin_function(),sum_functions(identity(),f0))

    def f3():
        f3_help1 = mul_functions(identity(),identity())
        f3_help2 = div_functions(f3_help1,const_function(100))  # x**2/100
        return mul_functions(sin_function(),f3_help2)

    def f4():
        f4_help1 = sum_functions(derivative(sin_function()),const_function(2))
        return div_functions(sin_function(),f4_help1)

    def f5():
        f5_help1 = mul_functions(identity(),identity()) # x**2
        f5_help2 = sub_functions(identity(),const_function(3))  # x-3
        f5_help3 = sum_functions(f5_help1,f5_help2)     # x**2+x-3
        return integral_function(f5_help3)

    def f6():
         f6_help1 = compose(sin_function(),derivative(sin_function()))
         f6_help2 = sub_functions(f6_help1,derivative(sin_function()))
         return mul_functions(const_function(5),f6_help2)

    def f7():
        f6_help1 = mul_functions(identity(),identity()) # x**2
        f6_help2 = mul_functions(f6_help1,identity())   # x**3
        return inverse(f6_help2)

    func_list = []
    func_list.append(f0)
    func_list.append(f1)
    func_list.append(f2)
    func_list.append(f3())
    func_list.append(f4())
    func_list.append(f5())
    func_list.append(f6())
    func_list.append(f7())
    return func_list


# function that genrate the figure in the ex description
def example_func(x):
    # return (x/5)**3
    return math.sin(x)





if __name__ == "__main__":
    import tkinter as tk
    from ex11helper import Graph
    master = tk.Tk()
    graph = Graph(master, -10, -10, 10, 10)
    # un-tag the line below after implementation of plot_func
    # plot_func(graph,f,-10,10,SEGMENTS,'red')
    # plot_func(graph,derivative(sin_function()),-10,10,40,'red')
    # plot_func(graph,const_function(0),-10,10,40,'black')


    color_arr = ['black', 'blue', 'red', 'green', 'brown', 'purple',
                 'dodger blue', 'orange']
    # un-tag the lines below after implementation of ex11_func_list
    for f in ex11_func_list():
        plot_func(graph, f, -10, 10, SEGMENTS)

    master.mainloop()
