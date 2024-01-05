from copy import deepcopy
class Task:
    def __init__(self, num_task, task_duration):
        self.num_task = num_task
        self.duration = task_duration[:]

    def __repr__(self):
        return f"Task(num_task={self.num_task}, duration={self.duration})"

class Team:
    def __init__(self, num_team, team_avalable_time):
        self.num_team = num_team
        self.team_avalable_time = deepcopy(team_avalable_time)

    def __repr__(self):
        return f"Team(num_team={self.num_team}, team_avalable_time={self.team_avalable_time})"

class Constrain:
    def __init__(self, task_constrain, team_task_constrain):
        self.task_constrain = deepcopy(task_constrain)
        self.team_task_constrain = deepcopy(team_task_constrain)

    def __repr__(self):
        return f"Constrain(task_constrain={self.task_constrain}, team_task_constrain={self.team_task_constrain})"
        
def take_input(n):
    with open(n,"r") as f:
        num_task, task_constrain_num = map(int, f.readline().split())
        task_constrain = [[0]*num_task for _ in range(num_task)]
        for _ in range(task_constrain_num):
            pretask, posttask = tuple(map(int, f.readline().split()))
            task_constrain[posttask-1][pretask-1] = 1
        task_duration = list(map(int, f.readline().split()))
        num_team = int(f.readline())
        team_avalable_time = list(map(int, f.readline().split()))
        team_task_constrain = [[-1]*num_team for _ in range(num_task)]
        if len(team_avalable_time) == num_team:
            num_pair = int(f.readline())
        else:
            num_pair = team_avalable_time.pop()
        for _ in range(num_pair):
            task, team, temp_time = tuple(map(int, f.readline().split()))
            team_task_constrain[task-1][team-1] = temp_time
        task,team,constrain=Task(num_task,task_duration),Team(num_team,team_avalable_time),Constrain(task_constrain,team_task_constrain)
        return task,team,constrain
    

