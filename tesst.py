'''
Heuristic:
Build a directed forest satisfies: Node i is parent of node j if and only if task i must be executed before task j
Step 1: Detect cycle in graph and delete it, since if node i, j, k contains a cycle then task i, j, k could not be completed.
Step 2: Sort the tasks in topological order.
Step 3: Calculate length of each node. Length of a node is length of the longest path from that node to a leaf. Sort the topo list 
in descending order of length.
Step 4: Assign task with team (heuristics). For each task in topo list, find available team that can do this task(cost of task done
by that team is greater than -1). The best team is chosen with minimum time done, minimum cost, and minimum number of tasks done 
by one team.
'''
class Task:
    def __init__(self, ID):
        self.ID = ID
        self.pred_tasks = []
        self.after_tasks = []
        self.team  = None
        self.duration = 0
        self.costs  = []
        self.time_done = 0
        self.visited = False 
        self.depth = -1
        self.length = 1

    def calc_depth(self):
        if self.depth != -1:
            return self.depth

        if not self.pred_tasks:
            self.depth = 1
        else:
            max_depth = max(pred_task.calc_depth() for pred_task in self.pred_tasks)
            self.depth = max_depth + 1

        # print(self.ID, self.depth)
        return self.depth
    
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

    for _ in range(q):
        a, b = map(int, input().split())
        tasks[a-1].after_tasks.append(tasks[b-1])
        tasks[b-1].pred_tasks.append(tasks[a-1])

    d =list(map(int, input().split()))

    for i in range(n):
        tasks[i].duration = d[i]
    m = int(input())
    s = list(map(int, input().split()))

    teams = [Team(i+1) for i in range(m)]
    for i in range(m):
        # teams[i].avail = s[i]
        teams[i].last_work = s[i]
        teams[i].cost = [-1 for _ in range(n)]
    
    if len(s) == m: k = int(input())
    else: k = s[-1]
    
    for _ in range (k):
        a, b, c = map(int, input().split())
        teams[b-1].cost[a-1] = c

    return tasks, teams

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
            # self.remove_node(task)
            task.pred_tasks.remove(node)
        if node.after_tasks is not None:
            for task in node.after_tasks:
                self.remove_node(task)
    
    def del_cycle(self):
        # import queue
        self.tasks.sort(key = lambda x: len(x.pred_tasks))

        # detect if there is a cycle in graph 
        if self.detect_cycle():
            # remove all node in cycle list
            for task in self.cycle:
                if task in self.tasks:
                    self.remove_node(task)

class Solve:
    def __init__(self, tasks, teams):
        self.tasks = tasks
        self.teams = teams 
        
    def solve(self):
        del_cycle = Cycle(self.tasks)
        del_cycle.del_cycle()

        for task in self.tasks:
            # task.depth = task.calc_depth()
            task.length = task.calc_length()

        '''topo sort'''
        N = len(self.tasks)
        topo_list = [None] * N
        i = N - 1
        
        def dfs(task, visited_nodes):
            task.visited = True
            # visited_nodes.append(task)
            for child in task.after_tasks:
                if child.visited == False:
                    dfs(child, visited_nodes)
            
            visited_nodes.append(task)
        
        for j in self.tasks:
            if j.visited  == False:
                visited_nodes = []
                dfs(j, visited_nodes)
                for task in visited_nodes:
                     topo_list[i] = task 
                     i -= 1
            
        '''heuristic'''
        self.res = []  
        topo_list.sort(key = lambda x: -x.length)  
        for task in topo_list:        
            max_time = -1
            # print(task.ID, task.depth, task.length)
            if len(task.pred_tasks) > 0:
                for t in task.pred_tasks:
                    if max_time < t.time_done: max_time = t.time_done

            avail_teams = [j for j in self.teams if j.cost[task.ID - 1] > -1]
            if len(avail_teams) > 0: 
                best_team = min(avail_teams, key = lambda x: [max(max_time, x.last_work), x.cost[task.ID - 1], x.task_done])
                time = max(max_time, best_team.last_work)
                task.time_done = time + task.duration 
                best_team.last_work = task.time_done
                best_team.task_done += 1 
                self.res.append([task.ID, best_team.ID, time])

        self.res.sort()
        # print(len(topo_list))
        # '''print for debugging'''
        # total_cost = 0
        # for ress in self.res: 
        #     total_cost += self.teams[ress[1] - 1].cost[ress[0] - 1]
        # eval = (len(self.res), max(topo_list, key = lambda x: x.time_done).time_done, total_cost)
        # print(eval)
        # for i in topo_list:
        #     print(i.ID, end = ' ')
        # print()
            # for task in i.after_tasks:
            #     print(task.ID, end = ' ')
            # print()

    # def export_sol(self, file):
    #     with open(file, 'w') as f:
    #         f.write(str(len(self.res)))
    #         f.write("\n")
    #         for res in self.res:
    #            ress = str()
    #            for i in res:
    #                ress = ress + str(i) + ' '
    #            f.write(ress)
    #            f.write('\n')

    def write(self):
        print(len(self.res))
        for res in self.res:
            print(*res)

def main():
    # tasks, teams = import_data("1.txt")
    tasks, teams = inp()
    sol = Solve(tasks, teams)
    sol.solve()
    # sol.export_sol("3_out.txt")
    sol.write()

if __name__ == "__main__":
    main()