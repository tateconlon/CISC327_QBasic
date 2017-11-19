class Solution(object):
    def maxAreaOfIsland(self, grid):
        #rows and cols
        m, n = len(grid), len(grid[0])
        
        islands = []
    
        def dfs(i,j):         
            if 0<=i<m and 0<=j<n and grid[i][j]:
                # by changing the value in this location to 0 it won't be double counted 
                # when we recurse down this again
                grid[i][j] = 0
                # return 1 and the dfs of every cube of land around this one
                return 1 + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i + 1, j) + dfs(i, j - 1)
            return 0           
            
        for i in range(m):
            for j in range(n):
                islands.append(dfs(i,j))
        
        return max(islands)