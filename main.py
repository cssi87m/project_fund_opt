from CONSTANT import import_data, Task, Team
'''
Heuristic:
Step 1:
	create a Tree, each Node is a Task
	Tree Depth is based on Q(i, j)
	if Task j can only be started to execute after the completion of task i -> task i is parent of task j and task j is child of task i
Step 2:
	loop through each task, sort workers based on workflow[-1][-1] is start free time of that worker
	loop through each worker, 
	if this task depth is 1, meaning this task does not depend on any task, add the worker has minimum workflow[-1][-1] that can work on this task
	else, calc timeDone of all task.prev (all tasks that this task depends on) and get the max timeDone
		if we have a worker's workflow[-1][-1] less than max timeDone and can work on this task, get the worker that has the minimum cost
		else, add the worker that has the minimum workflow[-1][-1] that can work on this task
'''
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
        teams[i].avail = s[i]
        teams[i].work_flow.append([0, teams[i].avail])
        teams[i].cost = [-1 for _ in range(n)]
    
    if len(s) == m: k = int(input())
    else: k = s[-1]
    
    for _ in range (k):
        a, b, c = map(int, input().split())
        teams[b-1].cost[a-1] = c
        tasks[a-1].costs.append((c, b))

    return tasks, teams

class Solve:
    def __init__(self, tasks, teams):
        self.tasks = tasks
        self.teams = teams 
        self.task_done = []
        
    
    def calc_breadth(self):
        for task in self.tasks[::-1]:
            for t in task.pred_tasks:
                t.breadth += task.breadth

    def solve(self):
        # Build a graph with nodes are tasks, node i is parent of node j if task j must be executed after task i
        del_cycle = Cycle(self.tasks)
        del_cycle.del_cycle()
        # print(del_cycle)
        # initial depth
        for i in range(len(self.tasks)):
             if len(self.tasks[i].pred_tasks) == 0:
                  self.tasks[i].depth = 0
		
		# calc all tasks depth
        for task in self.tasks:
            if task.depth == 0:
                task.calc_depth()

        self.calc_breadth()

        self.tasks.sort(key = lambda x: [x.depth, -x.breadth])
        self.teams.sort(key = lambda x: x.work_flow[-1][-1])

        for task in self.tasks:
            if task.depth == 0:
                for team in self.teams:
                    if team.cost[task.ID - 1] > -1:
                        team.works[task] = [team.work_flow[-1][-1], team.work_flow[-1][-1] + task.duration]
                        task.time_done = team.work_flow[-1][-1] + task.duration
                        team.work_flow.append(team.works[task])
                        task.team = team 
                        self.task_done.append(task)
                        break 
            
            else: 
                max_time = 0
                for t in task.pred_tasks:
                    if max_time < t.time_done: max_time = t.time_done

                best_team = self.teams[0]
                best_cost = float('inf')

                for team in self.teams:
                    if team.work_flow[-1][-1] <= max_time:
                        if team.cost[task.ID - 1] > -1:
                            if team.cost[task.ID - 1] < best_cost:
                                best_team = team
                                best_cost = team.cost[task.ID - 1]

                if best_cost < float('inf'):
                    best_team.works[task] = [max_time, max_time + task.duration]
                    task.time_done = max_time + task.duration
                    best_team.work_flow.append(best_team.works[task])
                    task.team = best_team
                    self.task_done.append(task)
                    
                else:
                    for team in self.teams:
                        if team.cost[task.ID - 1] > -1:
                            team.works[task] = [team.work_flow[-1][-1], team.work_flow[-1][-1] + task.duration]
                            task.time_done = team.work_flow[-1][-1] + task.duration
                            team.work_flow.append(team.works[task])
                            task.team = team 
                            self.task_done.append(task)
                            break 

    def export_sol(self, file):
        with open(file, 'w') as f:
            f.write(str(len(self.tasks)) + "\n")
            f.write(str(len(self.task_done)))
            f.write("\n")

            self.task_done.sort(key = lambda x: x.ID)

            for task in self.task_done:
                f.write(str(task.ID) + " " + str(task.team.ID) + " " + str(task.time_done - task.duration) + " " + str(task.team.cost[task.ID - 1]))
                f.write("\n")
            
    def write(self):
        print(len(self.task_done))
        for task in self.task_done:
            print(task.ID, task.team.ID, task.time_done - task.duration)

def main():
    # tasks, teams = import_data("3_in.txt")
    tasks, teams = inp()
    sol = Solve(tasks, teams)
    sol.solve()
    # sol.export_sol("3_out.txt")
    sol.write()

if __name__ == "__main__":
    main()
