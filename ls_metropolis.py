import time
import random
#############################

#Change here
n="7.txt"
DEEPNESS1=10
TIMEOUT=300
T=5
#############################

class Node:
    def __init__(self,val):
        self.val=val
        self.rank=0
        self.parent=None
        
    def make_child(self,parent):
        increase=task_duration[self.val-1]
        self.parent=parent
        self.rank+=increase
        cur=self
        looped=[self.val]
        while cur.parent!=None:
            cur=cur.parent
            cur.rank+=increase
            if cur.val in looped:
                break
            looped.append(cur.val)
            

with open(n,"r") as f:
    '''Nhap input'''
    num_task, task_constrain_num = map(int, f.readline().split())
    task_constrain = [[0]*num_task for _ in range(num_task)]
    '''The matrix task_constrain represents the precedence constraints between tasks. 
    If task_constrain[i][j] is 1, it means that task j can only start after the completion of task i.'''
    task_constrain_list=[]
    for _ in range(task_constrain_num):
        pretask, posttask = tuple(map(int, f.readline().split()))
        task_constrain_list.append((posttask,pretask))
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
    team_allowed_for_task=[[] for _ in range(num_task)]
    for _ in range(num_pair):
        task, team, temp_time = tuple(map(int, f.readline().split()))
        team_task_constrain[task-1][team-1] = temp_time
        team_allowed_for_task[task-1].append(team)

node_list=[Node(x) for x in range(1,num_task+1)]

for task1,task2 in task_constrain_list:
    node_list[task1-1].make_child(node_list[task2-1])
    
val_list=sorted(list(range(1,num_task+1)),key=lambda a: node_list[a-1].rank,reverse=True)

def calc_val(cur):
    a=len(cur)
    c=sum(team_task_constrain[task-1][team-1] for task,team in cur.items())
    available_time=team_available_time[:]
    not_solved=list(cur.keys())
    available_task=[]
    task_solved_time={key:0 for key in range(1,num_task+1)}
    for task in cur:
        if sum(task_constrain[task-1])==0:
            available_task.append((task,0))
    available_time=[[[x,99999999]]for x in team_available_time]
    while len(available_task)!=0:
        cur_task,cur_time=min(available_task,key=lambda a: val_list.index(a[0]))
        cur_team=cur[cur_task]
        for num,start_end in enumerate(available_time[cur_team-1]):
            start,end=start_end
            if cur_time + task_duration[cur_task-1]>end:
                continue
            elif cur_time<=start:
                available_time[cur_team-1][num][0]+=task_duration[cur_task-1]
                solve_time=available_time[cur_team-1][num][0]
                break
            else:
                available_time[cur_team-1][num][1]=cur_time
                available_time[cur_team-1].insert(num+1,[cur_time+task_duration[cur_task-1],end])
                solve_time=cur_time+task_duration[cur_task-1]
                break
        task_solved_time[cur_task]=solve_time
        not_solved.remove(cur_task)
        available_task=[]
        for task in cur:
            if task in not_solved:
                task_time = 0
                solvable = 1
                for task2 in range(1,num_task+1):
                    if task_constrain[task-1][task2-1]==1 and task2 in not_solved:
                        solvable=0
                        break
                    elif task_constrain[task-1][task2-1]==1:
                        task_time=max(task_time,task_solved_time[task2])
                if solvable:
                    available_task.append((task,task_time))
    b=max([x for x in available_time],key=lambda x:x[-1][0])[-1][0]
    return(a,b,c)

def print_res(cur):
    printing_list=[]
    a=len(cur)
    c=sum(team_task_constrain[task-1][team-1] for task,team in cur.items())
    available_time=team_available_time[:]
    not_solved=list(cur.keys())
    available_task=[]
    task_solved_time={key:0 for key in range(1,num_task+1)}
    for task in cur:
        if sum(task_constrain[task-1])==0:
            available_task.append((task,0))
    available_time=[[[x,99999999]]for x in team_available_time]
    while len(available_task)!=0:
        cur_task,cur_time=min(available_task,key=lambda a: val_list.index(a[0]))
        cur_team=cur[cur_task]
        for num,start_end in enumerate(available_time[cur_team-1]):
            start,end=start_end
            if cur_time + task_duration[cur_task-1]>end:
                continue
            elif cur_time<=start:
                solve_time=available_time[cur_team-1][num][0]
                available_time[cur_team-1][num][0]+=task_duration[cur_task-1]
                break
            else:
                available_time[cur_team-1][num][1]=cur_time
                available_time[cur_team-1].insert(num+1,[cur_time+task_duration[cur_task-1],end])
                solve_time=cur_time
                break
        task_solved_time[cur_task]=solve_time+task_duration[cur_task-1]
        printing_list.append((cur_task,cur_team,solve_time))
        not_solved.remove(cur_task)
        available_task=[]
        for task in cur:
            if task in not_solved:
                task_time = 0
                solvable = 1
                for task2 in range(1,num_task+1):
                    if task_constrain[task-1][task2-1]==1 and task2 in not_solved:
                        solvable=0
                        break
                    elif task_constrain[task-1][task2-1]==1:
                        task_time=max(task_time,task_solved_time[task2])
                if solvable:
                    available_task.append((task,task_time))
    b=max([x for x in available_time],key=lambda x:x[-1][0])[-1][0]
    printing_list.sort()
    for x1,x2,x3 in printing_list:
        print(x1,x2,x3)
    print(a,b,c)

cur={}
cur_val=(99999,99999,99999)
for h in range(DEEPNESS1):
    new_cur={}
    for task in range(1,num_task+1):
        if not team_allowed_for_task[task-1]:
            continue
        team=random.choice(team_allowed_for_task[task-1])
        new_cur[task]=team
    new_val=calc_val(new_cur)
    if new_val<cur_val:
        changed=1
        cur=new_cur.copy()
        cur_val=new_val
cur_time=time.perf_counter()
while True:
    task=random.randint(1,num_task)
    if not team_allowed_for_task[task-1]:
        continue
    for new_team in team_allowed_for_task[task-1]:
        if cur[task]!=new_team:
            new_cur=cur.copy()
            new_cur[task]=new_team
            new_val=calc_val(new_cur)
            if new_val<cur_val:
                cur[task]=new_team
                cur_val=new_val
            else:
                f=new_val[0]*100 + new_val[1]*10 + new_val[2] - (cur_val[0]*100 + cur_val[1]*10 + cur_val[2])
                c=2.718**((-f)/T)
                a=random.random()
                if a<c:
                    cur[task]=new_team
                    cur_val=new_val
    if time.perf_counter()-cur_time>TIMEOUT:
        break

print_res(cur)

    