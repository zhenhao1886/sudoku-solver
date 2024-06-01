import copy
class Solution:
    def solve_sudoku(self, board: list[list[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        - initialize possibilities
        - eliminate obvious wrong possibilities
        changed = True
        while changed is True:
            change = False
            - run through each empty cell to find any thing that has only 1 possibility
            - put that permanently on the board, set change to True
            - re-initialize possibilities

        if all cells are filled, return board

        stack = []

        look at the first cell with > 1 possibility and for each possibility in the cell,
            stack.append(possibilities with the first cell)
        
        while stack is not []:
            possibility = stack.pop(0)
            changed = True
            
            while changed is True:
                change = False
                - run through each empty cell in possibility; update all possibilities
                - return False immediately if there is a cell with a [] as a possibility, and break. This is a failed guess
                - if updated, set change to True

            if all cells have 1 possibility, then we are done.
            otherwise, 
            look at the first cell with > 1 possibility, and for each possibility in the cell, stack.append(possibilities within the next cell)

        """
        possibilities = self.initialize(board)
        
        changed = True
        while changed is True:
            
            #run through each empty cell to find any thing that has only 1 possibility
            #put that permanently on the board, set change to True
            changed, possibilities, board = self.update_possibilities(possibilities, board)
            
        #if all cells are filled, return board
        if self.check_answer(possibilities):
            self.complete_board(board, possibilities)
            
        else:
        #look at the first cell with > 1 possibility and for each possibility in the cell,
        #    stack.append(possibilities with the first cell)
            stack = self.get_possible_branches(possibilities)
            #print('stacking')
            
            while stack != []:
                possibility = stack.pop(0)
                changed = True
                while changed:
                    changed = False
                    #run through each empty cell in possibility; update all possibilities
                    changed, possibility, board = self.update_possibilities(possibility, board)
                    if possibility == False:
                        break
                if possibility != False:
                #if all cells have 1 possibility, then we are done.
                    if self.check_answer(possibility):
                        #print('checking')
                        self.complete_board(board, possibility)
                #look at the first cell with > 1 possibility, and for each possibility in the cell, stack.append(possibilities within the next cell)
                    else:
                        for branch in self.get_possible_branches(possibility):
                            stack.insert(0,branch)
                
    def initialize(self, board):
        possibilities = [[0 for _ in range(9)] for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                
                if board[i][j] == '.':
                    possibilities[i][j] = [str(k) for k in range(1,10)]
                    
                else:
                    possibilities[i][j] = ['-']
                
        return possibilities


    def update_possibilities(self, possibilities, board):
        #given a board, update the possibilities
        changed = False
        #print(possibilities)
        for i in range(len(board)):
            for j in range(len(board[0])):
                #for each cell, check what numbers are in the subbox, row and column
                ls1, ls2, ls3 = [],[],[]
                if len(possibilities[i][j]) > 1:
                    ls1 = self.get_numbers_in_row(board, possibilities, i)
                    ls2 = self.get_numbers_in_col(board, possibilities, j)
                    ls3 = self.get_numbers_in_subbox(board, possibilities, i,j)
                new = [x for x in possibilities[i][j] if x not in ls1 + ls2 + ls3]
                

                if possibilities[i][j] != new:
                    changed = True
                possibilities[i][j] = new
                if len(new) == 0: #if answer is not valid
                    possibilities = False
                    return changed, possibilities, board

        return changed, possibilities, board

    def check_filled(self,board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    return False
        return True

    def get_possible_branches(self,possibility):
        ls = []
        for i in range(9):
            for j in range(9):
                if len(possibility[i][j]) >= 2:
                    for p in possibility[i][j]:
                        p_prime = copy.deepcopy(possibility)
                        p_prime[i][j] = [p]
                        ls.append(p_prime)
                    return ls    
        

    def check_answer(self, possibility):
        for i in range(9):
            for j in range(9):
                if len(possibility[i][j]) > 1:
                    return False
        return True

    def complete_board(self, board, possibility):
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    board[i][j] = possibility[i][j][0]
        
    #removes from posibilities, the permanent number and the number if the possibility is of length 1
    def get_numbers_in_row(self, board, possibilities, i):
        ls = []
        for idx in range(9):
            if board[i][idx] != '.':
                ls.append(board[i][idx])
            if len(possibilities[i][idx]) == 1 and possibilities[i][idx] != ['-']:
                ls.append(possibilities[i][idx][0])
        return ls
    
    def get_numbers_in_col(self,board, possibilities, j):
        ls = []
        for idx in range(9):
            if board[idx][j] != '.':
                ls.append(board[idx][j])
            if len(possibilities[idx][j]) == 1 and possibilities[idx][j] != ['-']:
                ls.append(possibilities[idx][j][0])
        return ls

    def get_numbers_in_subbox(self, board, possibilities, i, j):
        ls = []
        subbox_range = [(i//3*3, i//3*3 + 3), (j//3*3, j//3*3 + 3)]

        for idx in range(*subbox_range[0]):
            for idx2 in range(*subbox_range[1]):
                if board[idx][idx2] != '.':
                    ls.append(board[idx][idx2])
                if len(possibilities[idx][idx2]) == 1 and possibilities[idx][idx2] != ['-']:
                    ls.append(possibilities[idx][idx2][0])
        return ls

if __name__ == "__main__":
    
    board = [["5","3",".",".","7",".",".",".","."],
             ["6",".",".","1","9","5",".",".","."],
             [".","9","8",".",".",".",".","6","."],
             ["8",".",".",".","6",".",".",".","3"],
             ["4",".",".","8",".","3",".",".","1"],
             ["7",".",".",".","2",".",".",".","6"],
             [".","6",".",".",".",".","2","8","."],
             [".",".",".","4","1","9",".",".","5"],
             [".",".",".",".","8",".",".","7","9"]]
    
    s = Solution()
    s.solve_sudoku(board)

    print(board)