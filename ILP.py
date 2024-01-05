from ortools.linear_solver import pywraplp
from input import take_input

def main(n):
    C1=100000000 #Largest constant
    C2=10000000 #Second largest constant
    solver = pywraplp.Solver.CreateSolver("SAT")
    task,team,constrain = take_input(n)
    inf = solver.infinity()
    check_vars = [[solver.IntVar(0, 1, f"Check variable for task {i+1} and team {j+1}") for j in range(team.num_team)] for i in range(task.num_task)]
    time_vars = [solver.IntVar(0, inf, f"Time for task {i+1}") for i in range(task.num_task)]
    task_orders = [[solver.IntVar(0, 1, f"Task order for task {i+1} and task {j+1}") for j in range(task.num_task)] for i in range(task.num_task)]
    for team_var in range(team.num_team):
        for task_var in range(task.num_task):
            solver.Add(check_vars[task_var][team_var]-1-constrain.team_task_constrain[task_var][team_var]<=0)
            solver.Add(team.team_avalable_time[team_var]-time_vars[task_var]-C1*(1-check_vars[task_var][team_var])<=0)
            for task2_var in range(task.num_task):
                if task2_var != task_var:
                    solver.Add(task.duration[task_var]+time_vars[task_var]-time_vars[task2_var]-C2*task_orders[task_var][task2_var]-C1*(1-check_vars[task_var][team_var])-C1*(1-check_vars[task2_var][team_var])<=0)
                    solver.Add(-(task.duration[task_var]+time_vars[task_var]-time_vars[task2_var]+C2*(1-task_orders[task_var][task2_var]))-C1*(1-check_vars[task_var][team_var])-C1*(1-check_vars[task2_var][team_var])<=0)
    for task1_var in range(task.num_task):
        solver.Add(sum(check_vars[task1_var][team_var] for team_var in range(team.num_team))-1<=0)
        for task2_var in range(task.num_task):
            solver.Add(time_vars[task1_var]-time_vars[task2_var]-C2*task_orders[task1_var][task2_var]-0.01<=0)
            solver.Add(-(time_vars[task1_var]-time_vars[task2_var]+C2*(1-task_orders[task1_var][task2_var]))+0.01<=0)
            if constrain.task_constrain[task2_var][task1_var]==1:
                solver.Add(-time_vars[task2_var] + time_vars[task1_var] + task.duration[task1_var] <= 0)
    max_time = solver.IntVar(0, inf, "Final time for solving all task")
    for task_var,time in enumerate(time_vars):
        solver.Add(time+task.duration[task_var]-max_time<=0)
    solver.Minimize(-100000000*sum(sum(check_var) for check_var in check_vars) + 1000000*max_time + 10000*sum(check_vars[task_var][team_var]*constrain.team_task_constrain[task_var][team_var] for task_var in range(task.num_task) for team_var in range(team.num_team) if constrain.team_task_constrain[task_var][team_var]>=0)+sum(time_vars))
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found.")
        print(f"Max time is {max_time.solution_value()}")
        sums=0
        task_done=0
        for task_var in range(task.num_task):
            for team_var in range(team.num_team):
                if check_vars[task_var][team_var].solution_value()==1:
                    print(f"Task {task_var+1} do by team {team_var+1} in {time_vars[task_var].solution_value()}")   
                    sums+=check_vars[task_var][team_var].solution_value()*constrain.team_task_constrain[task_var][team_var]
                    task_done+=1
        print(f"Number of task done is {task_done}")
        print(f'Total cost is {sums}')
    else:
        print("The problem does not have an optimal solution.")      
main("4.txt")
    