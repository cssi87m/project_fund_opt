'''Nhap input'''
num_task, task_constrain_num = map(int, input().split())
task_constrain = [[0]*num_task for _ in range(num_task)]
'''The matrix task_constrain represents the precedence constraints between tasks. 
If task_constrain[i][j] is 1, it means that task j can only start after the completion of task i.'''
for _ in range(task_constrain_num):
    pretask, posttask = tuple(map(int, input().split()))
    task_constrain[posttask-1][pretask-1] = 1
task_duration = list(map(int, input().split()))
num_team = int(input())
team_avalable_time = list(map(int, input().split()))
'''The matrix team_task_constrain stores the time constraints for tasks assigned to teams. 
If team_task_constrain[i][j] is not -1, it represents the cost (time) for team j to perform task i.'''
team_task_constrain = [[-1]*num_team for _ in range(num_task)]
if len(team_avalable_time) == num_team:
    num_pair = int(input())
else:
    num_pair = team_avalable_time.pop()
for _ in range(num_pair):
    task, team, temp_time = tuple(map(int, input().split()))
    team_task_constrain[task-1][team-1] = temp_time
cur_time = min(team_avalable_time)
team_avalable_list = [team for team in range(
    1, num_team+1) if team_avalable_time[team-1] <= cur_time]
# task_avalable_list = [task for task in range(
#     1, num_task+1) if sum(task_constrain[task-1]) == 0]
task_solved_time = [-1]*num_task
not_solved = [x for x in range(1, num_task+1)]
ans = []
min_time = 2**31-1
min_value = 2**31-1
newly_avalable=[]

task_avalable_list=[]
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
            task_avalable_list.append((task,max_time))
print(team_task_constrain)
# def checkout(cur_time):
#     global team_avalable_list, task_avalable_list
#     team_avalable_list = [team for team in range(
#         1, num_team+1) if team_avalable_time[team-1] <= cur_time]
#     task_avalable_list = [task for task in range(1, num_task+1) if sum([task_constrain[task-1][pretask-1]
#                                                                        for pretask in range(1, num_task+1) if pretask in not_solved
#                                                                         or task_solved_time[pretask-1] > cur_time]) == 0 and task in not_solved]
#     # print("list:",team_avalable_list,task_avalable_list,not_solved)
    
def checkout():
    global task_avalable_list
    task_avalable_list=[]
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
                task_avalable_list.append((task,max_time))
    # print("list:",team_avalable_list,task_avalable_list,not_solved)
    
    
def checkout_newly_avalable(new_time):
    global newly_avalable
    newly_avalable=[team for team in range(1,num_team+1) if team_avalable_time[team-1]==new_time]

def solve(cur_time, current_task_order, cur_value, waited):
    # print("time:",cur_time)
    global min_time, min_value, ans
    if len(not_solved) != 0 and (cur_time > min_time or (cur_time == min_time and cur_value < min_value)):
        return
    elif len(not_solved) == 0:
        solve_time = max(task_solved_time)
        if solve_time < min_time or (solve_time == min_time and cur_value < min_value):
            ans = current_task_order[:]
            min_time = solve_time
            min_value = cur_value
        return
    done_something = 0
    if waited==1:
        for team in newly_avalable[:]:
            for task in task_avalable_list[:]:
                if team_task_constrain[task-1][team-1] != -1:
                    # temp = (team_avalable_list[:], task_avalable_list[:])
                    # print(task,team,cur_time)
                    # print("list:",team_avalable_list,task_avalable_list,not_solved)
                    done_something = 1
                    not_solved.remove(task)
                    task_solved_time[task-1] = cur_time+task_duration[task-1]
                    team_avalable_time[team-1] += task_duration[task-1]
                    new_time = min(team_avalable_time)
                    current_task_order.append((task, team, cur_time))
                    checkout(new_time)
                    solve(new_time, current_task_order, cur_value +
                        team_task_constrain[task-1][team-1],0)
                    task_solved_time[task-1] = -1
                    current_task_order.pop()
                    not_solved.append(task)
                    team_avalable_time[team-1] -= task_duration[task-1]
                    checkout(cur_time)
    else:  
        for task in task_avalable_list[:]:
            for team in team_avalable_list[:]:
                if team_task_constrain[task-1][team-1] != -1:
                    # temp = (team_avalable_list[:], task_avalable_list[:])
                    # print(task,team,cur_time)
                    # print("list:",team_avalable_list,task_avalable_list,not_solved)
                    done_something = 1
                    not_solved.remove(task)
                    task_solved_time[task-1] = cur_time+task_duration[task-1]
                    team_avalable_time[team-1] += task_duration[task-1]
                    new_time = min(team_avalable_time)
                    current_task_order.append((task, team, cur_time))
                    checkout(new_time)
                    solve(new_time, current_task_order, cur_value +
                        team_task_constrain[task-1][team-1],0)
                    task_solved_time[task-1] = -1
                    current_task_order.pop()
                    not_solved.append(task)
                    team_avalable_time[team-1] -= task_duration[task-1]
                    checkout(cur_time)
    if len(team_avalable_list)==num_team:
        return
    temp = {}
    for index in range(num_team):
        temp[index] = team_avalable_time[index]
    time_list = [time for time in team_avalable_time if time > cur_time]
    if len(time_list) == 0:
        new_time = max(task_solved_time)
    else:
        new_time = min(time_list)
    checkout_newly_avalable(new_time)
    for index in range(num_team):
        if team_avalable_time[index] < new_time:
            team_avalable_time[index] = new_time

    checkout(new_time)
    solve(new_time, current_task_order, cur_value, 1)
    for index in range(num_team):
        team_avalable_time[index] = temp[index]

    checkout(cur_time)

def solve2(cur_time, current_task_order, cur_value):
    # print("time:",cur_time)
    global min_time, min_value, ans
    if len(not_solved) != 0 and (cur_time > min_time or (cur_time == min_time and cur_value < min_value)):
        return
    elif len(not_solved) == 0:
        solve_time = max(task_solved_time)
        if solve_time < min_time or (solve_time == min_time and cur_value < min_value):
            ans = current_task_order[:]
            min_time = solve_time
            min_value = cur_value
        return
    done_something = 0
    for task in task_avalable_list[:]:
        for team in team_avalable_list[:]:
            if team_task_constrain[task-1][team-1] != -1:
                # temp = (team_avalable_list[:], task_avalable_list[:])
                # print(task,team,cur_time)
                # print("list:",team_avalable_list,task_avalable_list,not_solved)
                done_something = 1
                not_solved.remove(task)
                task_solved_time[task-1] = cur_time+task_duration[task-1]
                team_avalable_time[team-1] += task_duration[task-1]
                new_time = min(team_avalable_time)
                current_task_order.append((task, team, cur_time))
                checkout(new_time)
                solve2(new_time, current_task_order, cur_value +
                    team_task_constrain[task-1][team-1])
                task_solved_time[task-1] = -1
                current_task_order.pop()
                not_solved.append(task)
                team_avalable_time[team-1] -= task_duration[task-1]
                checkout(cur_time)
    if not done_something:
        temp = {}
        for index in range(num_team):
            temp[index] = team_avalable_time[index]
        time_list = [time for time in team_avalable_time if time > cur_time]
        if len(time_list) == 0:
            new_time = max(task_solved_time)
        else:
            new_time = min(time_list)
        for index in range(num_team):
            if team_avalable_time[index] < new_time:
                team_avalable_time[index] = new_time

        checkout(new_time)
        solve2(new_time, current_task_order, cur_value)
        for index in range(num_team):
            team_avalable_time[index] = temp[index]

        checkout(cur_time)

def solve3(current_task_order, cur_value):
    # print("time:",cur_time)
    global min_time, min_value, ans
    if len(not_solved) != 0 and (max(task_solved_time) > min_time or (max(task_solved_time) == min_time and cur_value <= min_value)):
        return
    elif len(not_solved) == 0:
        solve_time = max(task_solved_time)
        if solve_time < min_time or (solve_time == min_time and cur_value < min_value):
            ans = current_task_order[:]
            min_time = solve_time
            min_value = cur_value
        return
    for task,time in task_avalable_list[:]:
        for team in range(1,num_team+1):
            if team_task_constrain[task-1][team-1] != -1:
                # temp = (team_avalable_list[:], task_avalable_list[:])
                # print(task,team,cur_time)
                # print("list:",team_avalable_list,task_avalable_list,not_solved)
                not_solved.remove(task)
                new_time = max(team_avalable_time[team-1],time)
                task_solved_time[task-1] = new_time+task_duration[task-1]
                team_avalable_time[team-1] += task_duration[task-1]
                current_task_order.append((task, team, new_time))
                checkout()
                solve3(current_task_order, cur_value +
                    team_task_constrain[task-1][team-1])
                task_solved_time[task-1] = -1
                current_task_order.pop()
                not_solved.append(task)
                team_avalable_time[team-1] -= task_duration[task-1]
                checkout()

# print(team_avalable_time,"\n",team_task_constrain,"\n",task_duration,"\n",task_constrain,"\n",team_avalable_list,"\n",task_avalable_list)
# solve2(cur_time, [], 0)
# print("done")
# solve(cur_time, [], 0, 0)
solve3([], 0)
answer = ans[:]
answer.sort()
print(num_task)
for task, team, temp_time in answer:
    print(task, team, temp_time)
