class Task:
    def __init__(self, ID):
        self.ID = ID
        self.pred_tasks = []
        self.after_tasks = []
        self.team  = None
        self.duration = 0
        self.depth = 0
        self.breadth = 1
        self.costs  = []
        self.time_done = 0
    
    def calc_depth(self):
        for task in self.after_tasks:
            task.depth = max(task.pred_tasks, key = lambda x: x.depth).depth + 1
            task.calc_depth()
    

class Team:
    def __init__(self, ID):
        self.ID = ID
        self.avail = 0
        self.cost = []
        self.works = {}
        self.work_flow  = []
        


def import_data(file):

    with open(file, 'r') as f:
        n, q = map(int, f.readline().split())
        tasks = [Task(i+1) for i in range(n)]
        
        for i in range(q):
            a, b = map(int, f.readline().split())
            tasks[a-1].after_tasks.append(tasks[b-1])
            tasks[b-1].pred_tasks.append(tasks[a-1])

        
        d = list(map(int, f.readline().split()))
        
        for i in range(n):
            tasks[i].duration = d[i]
        m = int(f.readline())
        s = list(map(int, f.readline().split()))
        
        teams = [Team(i+1) for i in range(m)]
        for i in range(m):
            teams[i].avail = s[i]
            teams[i].work_flow.append([0, teams[i].avail])
            teams[i].cost = [-1 for _ in range(n)]
        
        if len(s) == m: k = int(input())
        else: k = s[-1]
        
        for _ in range(k):
            a, b, c = map(int, f.readline().split())
            teams[b-1].cost[a-1] = c
            tasks[a-1].costs.append((c, b))
    
    return tasks, teams