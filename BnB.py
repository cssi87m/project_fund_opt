#############################

#Change here
n="1.txt"

#############################
with open(n,"r") as f:
    '''Nhap input'''
    num_task, task_constrain_num = map(int, f.readline().split())
    task_constrain = [[0]*num_task for _ in range(num_task)]
    '''The matrix task_constrain represents the precedence constraints between tasks. 
    If task_constrain[i][j] is 1, it means that task j can only start after the completion of task i.'''
    for _ in range(task_constrain_num):
        pretask, posttask = tuple(map(int, f.readline().split()))
        task_constrain[posttask-1][pretask-1] = 1
    task_duration = list(map(int, f.readline().split()))
    num_team = int(f.readline())
    team_available_time = list(map(int, f.readline().split()))
    '''The matrix team_task_constrain stores the time constraints for tasks assigned to teams. 
    If team_task_constrain[i][j] is not -1, it represents the cost (time) for team j to perform task i.'''
    team_task_constrain = [[-1]*num_team for _ in range(num_task)]
    if len(team_available_time) == num_team:
        num_pair = int(f.readline())
    else:
        num_pair = team_available_time.pop()
    for _ in range(num_pair):
        task, team, temp_time = tuple(map(int, f.readline().split()))
        team_task_constrain[task-1][team-1] = temp_time
task_solved_time = [-1]*num_task
not_solved = [x for x in range(1, num_task+1)]

ans = []
min_time = 2**31-1
min_value = 2**31-1

task_available_list=[]
for task in range(1,num_task+1):
    if task in not_solved:
        max_time=0
        doable=1
        for pretask in range(1,num_task+1):
            if task_constrain[task-1][pretask-1]==1:
                if pretask in not_solved:
                    doable=0
                    break
                else:
                    max_time=max(max_time,task_solved_time[pretask-1])
        if doable==1:
            task_available_list.append((task,max_time))

def checkout():
    global task_available_list
    task_available_list=[]
    for task in range(1,num_task+1):
        if task in not_solved:
            max_time=0
            doable=1
            for pretask in range(1,num_task+1):
                if task_constrain[task-1][pretask-1]==1:
                    if pretask in not_solved:
                        doable=0
                        break
                    else:
                        max_time=max(max_time,task_solved_time[pretask-1])
            if doable==1:
                task_available_list.append((task,max_time))

def solve3(current_task_order, cur_value, task_constrain_num):
    global min_time, min_value, ans
    if len(not_solved) != 0 and (max(task_solved_time) > min_time or (max(task_solved_time) == min_time and cur_value >= min_value)):
        return
    elif len(not_solved) == 0:
        solve_time = max(task_solved_time)
        if solve_time < min_time or (solve_time == min_time and cur_value < min_value):
            ans = current_task_order[:]
            min_time = solve_time
            min_value = cur_value
        return
    done_something=0
    min_do_time=min(task_available_list,key=lambda a:a[1])[1]
    for task,time in task_available_list[:]:
        if time==min_do_time:
            have_done=0
            not_solved.remove(task)
            new_task_constrain_num=sum(task_constrain[task1][task2] for task1 in range(num_task) for task2 in range(num_task) if task1+1 in not_solved and task2+1 in not_solved)
            for team in range(1,num_team+1):
                if team_task_constrain[task-1][team-1] != -1:
                    new_time = max(team_available_time[team-1],time)
                    task_solved_time[task-1] = new_time + task_duration[task-1]
                    temp_value=team_available_time[team-1]
                    team_available_time[team-1] = new_time + task_duration[task-1]
                    current_task_order.append((task, team, new_time))
                    checkout()
                    if new_task_constrain_num!=task_constrain_num or not done_something:
                        solve3(current_task_order, cur_value +
                            team_task_constrain[task-1][team-1], new_task_constrain_num)
                        have_done=1
                    current_task_order.pop()
                    team_available_time[team-1] = temp_value
            task_solved_time[task-1] = -1
            not_solved.append(task)
            checkout()
            if have_done==1:
                done_something=1

solve3([], 0, task_constrain_num)
answer = ans[:]
answer.sort()
print(num_task)
for task, team, temp_time in answer:
    print(task, team, temp_time)
