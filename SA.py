'''
Improve greedy algorithm using simulated annealing (SA)
- Define each state as a topological order of tasks
- At each state, calculate a solution using greedy algorithm. Based on that solution calculate temperature of the state.
- Based on SA schema, update the state.
'''
import random
import math 
from copy import deepcopy
class Cycle:
    def __init__(self, tasks):
        self.tasks = tasks
        # self.flags = [-1 for _ in range(len(self.tasks))]
        self.cycle = []
    def __str__(self):
        result = str(len(self.tasks))
        return result
    def detect_cycle(self):
        visited = {}
        backtrack = {}
        for task in self.tasks:
            visited[task] = False
            backtrack[task] = False
        
        for task in self.tasks:
            if visited[task] == False:
                if self.cycle_util(task, visited, backtrack):
                    return True 
        
        return False
    
    def cycle_util(self, task, visited, backtrack):
        # if backtrack[task] is True,  the current task is in the traversal path and we encounter it again during the same path.
        # it means task is a vertice of a cycle 
        if backtrack[task]:
            self.cycle.append(task)
            return True
        if visited[task]:
            return False

        backtrack[task] = True 
        visited[task] = True 
        for t in task.after_tasks:
            if self.cycle_util(t, visited, backtrack):
                self.cycle.append(t)
                return True
        
        backtrack[task] = False
        return False

    def remove_node(self, node):
        self.tasks.remove(node)
        # remove the task in list of all after_tasks in all pred_tasks of node 
        for task in node.pred_tasks:
            task.after_tasks.remove(node)
        # remove the task in list of all predr_tasks in all after_tasks of node    
        for task in node.after_tasks:
            task.pred_tasks.remove(node)
    
    
    def del_cycle(self):
        # import queue
        self.tasks.sort(key = lambda x: len(x.pred_tasks))

        # detect if there is a cycle in graph 
        if self.detect_cycle():
            # remove all node in cycle list
            for task in self.cycle:
                if task in self.tasks:
                    self.remove_node(task)
                if task.after_tasks is not None:
                    for child in task.after_tasks:
                        if child in self.tasks:
                            self.remove_node(child)
class Task:
    def __init__(self, ID):
        self.ID = ID
        self.pred_tasks = []
        self.after_tasks = []
        self.duration = 0
        self.costs = []
        self.time_done = 0
        self.visited = False
        self.length = 1
    def calc_length(self):
        if self.after_tasks:
            self.length = max(after_task.calc_length() for after_task in self.after_tasks) 
            self.length += 1
        return self.length

class Team:
    def __init__(self, ID):
        self.ID = ID
        self.avail = 0
        self.last_work = 0
        self.task_done = 0

def inp():
    n, q = map(int, input().split())
    tasks = [Task(i+1) for i in range(n)]
    graph = [[0 for _ in range(n)] for _ in range(n)]

    for _ in range(q):
        a, b = map(int, input().split())
        tasks[a-1].after_tasks.append(tasks[b-1])
        tasks[b-1].pred_tasks.append(tasks[a-1])
        graph[a-1][b-1] = 1

    d = list(map(int, input().split()))

    for i in range(n):
        tasks[i].duration = d[i]
    m = int(input())
    s = list(map(int, input().split()))

    teams = [Team(i+1) for i in range(m)]
    for i in range(m):
        teams[i].avail = s[i]
        teams[i].last_work = s[i]
        teams[i].cost = [-1 for _ in range(n)]

    if len(s) == m:
        k = int(input())
    else:
        k = s[-1]

    for _ in range(k):
        a, b, c = map(int, input().split())
        teams[b-1].cost[a-1] = c

    task_team = [[-1 for _ in range(len(teams))] for _ in range(len(tasks))]
    for i in tasks:
        for j in teams:
            task_team[i.ID - 1][j.ID - 1] = j.cost[i.ID - 1]
    return tasks, teams, task_team, graph

'''
Denote a state = permutation of tasks. a valid permutation must be in topological order, 
indeed, there is no cycle in the tasks graph.
If the solution is not feasible, its fitness score will be 0.
'''
class state: 
    def __init__(self, teams, task_team, state, graph): 
        self.teams = teams
        self.task_team = task_team 
        self.state = state
        self.n = len(self.state)
        self.m = len(self.teams)
        # if chromosome is None, generate random solution 
        self.team_state = [0] * self.n
        self.obj = 0
        self.graph = graph 
        self.neighbour = []
        self.task_done = 0
        self.visited = False

    def __str__(self):
        res = [str(self.state[i].ID) for i in range(self.n)]
        return ', '.join(res)


    def calc_obj(self):
        ''' calculate team order base on state. the team is chosen by greedy algorithm '''
        self.res = []
        teams = deepcopy(self.teams)
        for i in range(self.n):
            max_time = -1
            # print(task.ID, end=' ')
            if len(self.state[i].pred_tasks) > 0:
                for t in self.state[i].pred_tasks:
                    if max_time < t.time_done:
                        max_time = t.time_done

            avail_teams = [j for j in teams if j.cost[self.state[i].ID - 1] > -1]
            if len(avail_teams) > 0:
                best_team = min(avail_teams, key=lambda x: [
                                max(max_time, x.last_work), x.cost[self.state[i].ID - 1], x.task_done])
                time = max(max_time, best_team.last_work)
                self.state[i].time_done = time + self.state[i].duration
                best_team.last_work = self.state[i].time_done
                best_team.task_done += 1
                self.team_state[i] = best_team.ID
                self.res.append([self.state[i].ID, best_team.ID, time]) 
            
        '''calculate the temperature'''
        # calculate number of tasks done 
        task_done = sum([(self.team_state[i] > 0) for i in range(self.n)])
        self.task_done = task_done
        # calculate the completion time of all tasks
        time_done = max(self.state, key = lambda x: x.time_done).time_done
        # calculate total cost for task assignment 
        total_cost = 0
        for i in range(self.n): 
            if self.team_state[i] > 0:
                total_cost += self.task_team[self.state[i].ID - 1][self.team_state[i] - 1]
        self.obj = [task_done, time_done, total_cost]
    
    def swap(self):
        '''Swap 2 consecutive tasks that still preserve topological order '''
        for i in range(self.n - 1):
            if not self.graph[self.state[i].ID - 1][self.state[i+1].ID - 1]:
                new_state = state(self.teams, self.task_team, self.state.copy(), self.graph)
                new_state.state[i], new_state.state[i+1] = new_state.state[i+1], new_state.state[i]
                if new_state not in self.neighbour:
                    self.neighbour.append(new_state)

        '''Swap 2 consecutive tasks that still preserve topological order '''
        for i in range(self.n - 1, 0, -1):
            if not self.graph[self.state[i-1].ID - 1][self.state[i].ID - 1]:
                new_state = state(self.teams, self.task_team, self.state.copy(), self.graph)
                new_state.state[i], new_state.state[i-1] = new_state.state[i-1], new_state.state[i]
                if new_state not in self.neighbour:
                    self.neighbour.append(new_state)

def is_better(obj1, obj2): 
    return (obj1[0] > obj2[0] or (obj1[0] == obj2[0] and obj1[1] < obj2[1]) or 
            (obj1[0] == obj2[0] and obj1[1] == obj2[1] and obj1[2] < obj2[2]))

def e_power(obj1, obj2, temperature):
    return math.exp(((obj1[0] - obj2[0]) - 0.8*(obj1[1] - obj2[1]) - 0.001*(obj1[2] - obj2[2]))/temperature)

class SA:
    LIM = 100
    def __init__(self, temperature, state: state, cooling_factor, num_iterations):
        self.temperature = temperature
        self.state = state
        self.num_iterations = num_iterations
        self.cooling_factor = cooling_factor
        self.res = state
        self.visited = {}
 
    def solve(self):
        # a variable to store best candidate after 1 iteration
        self.state.calc_obj()
        best_cand = state(self.state.teams, self.state.task_team, self.state.state.copy(), self.state.graph)
        obj = self.state.obj.copy()
        best_obj = self.state.obj.copy()
        # SA procedure
        for _ in range(self.num_iterations):
            '''SA procedure will stop either after self.num_iterations, or best_cand is not changed after an iteration'''
            cand_state = tuple(best_cand.state)
            i = 0 # count variable 
            while (i < self.LIM):
                if self.visited.get(cand_state, 0) == 0:
                    best_cand.swap()
                    best_cand = random.choice(best_cand.neighbour)
                    cand_state = tuple(best_cand.state)
                i += 1
            # print(i)
            if self.visited.get(cand_state, 1) == 1:
                # print(len(best_cand.neighbour))
                best_cand.swap()
                self.visited[cand_state] = 0
                neighbour = best_cand.neighbour
                '''Randomly choose 10 neighbour of current best_cand'''
                for i in range(len(neighbour)//10):
                    # print(f"Checking neighbour at index {i}, length: {len(best_cand.neighbour)}")
                    candidate = random.choice(neighbour)
                    cand_state = tuple(candidate.state)
                    if self.visited.get(cand_state, 0) == 0:
                        candidate.calc_obj()
                        self.visited[cand_state] = candidate.obj

                    '''candidate.obj is better than current obj'''
                    if is_better(self.visited[cand_state], obj):
                        obj = self.visited[cand_state]
                        '''if obj is better than best_obj, changing the current best candidate'''
                        if is_better(obj, best_obj):
                            best_obj = obj 
                            best_cand = candidate

                        '''if candidate.obj is not better than current obj, calculate p as the probability of going downward.
                        if p < epsilon, update obj.'''
                    else: 
                        p = min(e_power(obj, self.visited[cand_state], self.temperature), 1)
                        eps = random.random()
                        if eps > p: # downward movement
                            obj = self.visited[cand_state]
                            # best_cand = cand_state
                        
                        else: 
                            self.cooling_factor *= 1.25
                    # print(best_obj)
                self.temperature *= self.cooling_factor
                # print(best_obj)
            # else: 
            #     break
        
        # calculate res
        if best_cand.obj == 0: best_cand.calc_obj()
        self.res = best_cand

def topo(tasks):
    del_cycle = Cycle(tasks)
    del_cycle.del_cycle()

    '''topo sort'''
    N = len(tasks)
    topo_list = [None] * N
    i = N - 1

    def dfs(task, visited_nodes):
        task.visited = True
        # visited_nodes.append(task)
        for child in task.after_tasks:
            if child.visited == False:
                dfs(child, visited_nodes)

        visited_nodes.append(task)

    for j in tasks:
        if j.visited == False:
            visited_nodes = []
            dfs(j, visited_nodes)
            for task in visited_nodes:
                topo_list[i] = task
                i -= 1
    return topo_list

def import_data(file):
    with open(file, 'r') as f:
        n, q = map(int, f.readline().split())
        tasks = [Task(i+1) for i in range(n)]
        graph = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(q):
            a, b = map(int, f.readline().split())
            tasks[a-1].after_tasks.append(tasks[b-1])
            tasks[b-1].pred_tasks.append(tasks[a-1])
            graph[a-1][b-1] = 1

        d = list(map(int, f.readline().split()))
        
        for i in range(n):
            tasks[i].duration = d[i]
        m = int(f.readline())
        s = list(map(int, f.readline().split()))
        
        teams = [Team(i+1) for i in range(m)]
        for i in range(m):
            teams[i].avail = s[i]
            teams[i].last_work = s[i]
            teams[i].cost = [-1 for _ in range(n)]
        
        if len(s) == m: k = int(f.readline())
        else: k = s[-1]
        
        for _ in range(k):
            a, b, c = map(int, f.readline().split())
            teams[b-1].cost[a-1] = c
            tasks[a-1].costs.append((c, b))
        
        task_team = [[-1 for _ in range(len(teams))] for _ in range(len(tasks))]
        for i in tasks:
            for j in teams:
                task_team[i.ID - 1][j.ID - 1] = j.cost[i.ID - 1]
    
    return tasks, teams, task_team, graph

def export_data(file, solver):
    with open(file, 'w') as f:
        f.write(str(solver.res.task_done) + "\n")
        for ress in solver.res.res: 
            for i in ress: f.write(str(i)+ " ")
            f.write("\n")
        # f.write(str(solver.res.obj))

def main(input, out, is_print): 
    # tasks, teams, task_team, graph = inp()
    if input:
        tasks, teams, task_team, graph = import_data(input)
    else: 
        tasks, teams, task_team, graph = inp()
    # initiate a topo list 
    topo_list = topo(tasks)
    for task in topo_list:
        task.length = task.calc_length()
    topo_list.sort(key = lambda x: -x.length)  
    # initiate params 
    num_iterations = 50
    temperature = 10
    cooling_factor = 0.6
    first_state = state(teams, task_team, topo_list, graph)
    solver = SA(temperature, first_state, cooling_factor, num_iterations)
    solver.solve()

    if is_print:
        print(solver.res.task_done)
        for res in solver.res.res:
            for i in res: print(i, end = ' ')
            print()
    else: 
        export_data(out, solver)
    print(solver.res.obj)
    # export_data("output.txt", solver)

local = True
if local:
    import os
    import timeit
    test_case = -1 

    if test_case == -1: 
        for t in sorted(os.listdir('input'), key = lambda x: int(x.split(".")[0])):
            start_time = timeit.default_timer()
            input = f'input//{t}'
            out = f'SA//{t}'
            main(input, out, False)
            print(f'test case {t}: runtime = {timeit.default_timer() - start_time}')

    else: 
        start_time = timeit.default_timer()
        input = f'input//{test_case}.txt'
        out = f'SA//{test_case}.txt'
        main(input, out, False)
        print(f'test case {test_case}: runtime = {timeit.default_timer() - start_time}')

else: 
    main(False, False, True)
