"""
# Employee info
class Employee(object):
    def __init__(self, id, importance, subordinates):
        # It's the unique id of each node.
        # unique id of this employee
        self.id = id
        # the importance value of this employee
        self.importance = importance
        # the id of direct subordinates
        self.subordinates = subordinates
"""
class Solution(object):
    def getImportance(self, employees, id):
        
        if not employees: return
        
        empImportance = {}
        for employee in employees:
            empImportance[employee.id] = (employee.importance, employee.subordinates)
            
        #DFS
        total = empImportance[id][0]
        # Stack s Contains employee ID's to visit
        s = [x for x in empImportance[id][1]]
        seen = set()
        while s:
            nxt = s.pop()
            if nxt not in seen:
                total += empImportance[nxt][0]
                for subordinate in empImportance[nxt][1]:
                    if subordinate not in seen:
                        s.append(subordinate)
                seen.add(nxt)
        
        return total
            
            
            
            

        
        
        