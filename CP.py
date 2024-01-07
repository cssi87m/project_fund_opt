from ortools.sat.python import cp_model
from input import take_input
import time

def main(n):
    task,team,constrain = take_input(n)
    C1=99999999999
    model=cp_model.CpModel()
    check = [[model.NewBoolVar(f"Check variable for task {i+1} and team {j+1}") for j in range(team.num_team)] for i in range(task.num_task)]
    times = [model.NewIntVar(0, C1, f"Time for task {i+1}") for i in range(task.num_task)]
    orders = [[model.NewBoolVar(f"Task order for task {i+1} and task {j+1}") for j in range(task.num_task)] for i in range(task.num_task)]
    for task_var in range(task.num_task):
        model.AddAtMostOne(check[task_var])
        for team_var in range(team.num_team):
            model.Add(check[task_var][team_var]-1-constrain.team_task_constrain[task_var][team_var]<=0)
            model.Add(team.team_available_time[team_var]-times[task_var]<=0).OnlyEnforceIf(check[task_var][team_var])
            for task2_var in range(task.num_task):
                if task2_var != task_var:
                    model.Add(task.duration[task_var]+times[task_var]<=times[task2_var]).OnlyEnforceIf(orders[task_var][task2_var],check[task_var][team_var],check[task2_var][team_var])
    for task1_var in range(task.num_task):
        for task2_var in range(task.num_task):
            model.Add(times[task1_var]<=times[task2_var]).OnlyEnforceIf(orders[task1_var][task2_var])
            model.Add(times[task1_var]>times[task2_var]).OnlyEnforceIf(orders[task1_var][task2_var].Not())
            if constrain.task_constrain[task2_var][task1_var]==1:
                model.Add(times[task1_var]+task.duration[task1_var]<=times[task2_var])
    max_time = model.NewIntVar(0, C1, "Final time for solving all task")
    for task_var,time_var in enumerate(times):
        model.Add(time_var+task.duration[task_var]<=max_time)
    model.Minimize((-100000000*sum(sum(check_var) for check_var in check) + 1000000*max_time + 10000*sum(check[task_var][team_var]*constrain.team_task_constrain[task_var][team_var] for task_var in range(task.num_task) for team_var in range(team.num_team) if constrain.team_task_constrain[task_var][team_var]>=0)+sum(times)))
    solver=cp_model.CpSolver()
    status=solver.Solve(model)
    if status == cp_model.OPTIMAL:
        print("Optimal solution found.")
        sums=0
        task_done=0
        for task_var in range(task.num_task):
            for team_var in range(team.num_team):
                if solver.Value(check[task_var][team_var])==1:
                    print(f"Task {task_var+1} do by team {team_var+1} in {solver.Value(times[task_var])}")   
                    sums+=solver.Value(check[task_var][team_var])*constrain.team_task_constrain[task_var][team_var]
                    task_done+=1
        print(f"Number of task done is {task_done}")
        print(f"Max time is {solver.Value(max_time)}")
        print(f'Total cost is {sums}')
    else:
        print("No solution found.")
hehehe=time.perf_counter()
main("4.txt")
print('Time: ',time.perf_counter()-hehehe)