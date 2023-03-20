import itertools
import random


class Minesweeper():
  """
  Minesweeper game representation
  """

  def __init__(self, height=8, width=8, mines=8):
    # Set initial width, height, and number of mines
    self.height = height
    self.width = width
    self.mines = set()

    # Initialize an empty field with no mines
    self.board = []
    for i in range(self.height):
      row = []
      for j in range(self.width):
        row.append(False)
      self.board.append(row)

    # Add mines randomly
    while len(self.mines) != mines:
      i = random.randrange(height)
      j = random.randrange(width)
      if not self.board[i][j]:
        self.mines.add((i, j))
        self.board[i][j] = True

    # At first, player has found no mines
    self.mines_found = set()

  def print(self):
    """
    Prints a text-based representation
    of where mines are located.
    """
    for i in range(self.height):
      print("--" * self.width + "-")
      for j in range(self.width):
        if self.board[i][j]:
          print("|X", end="")
        else:
          print("| ", end="")
      print("|")
    print("--" * self.width + "-")

  def is_mine(self, cell):
    i, j = cell
    return self.board[i][j]

  def nearby_mines(self, cell):
    """
    Returns the number of mines that are
    within one row and column of a given cell,
    not including the cell itself.
    """

    # Keep count of nearby mines
    count = 0

    # Loop over all cells within one row and column
    for i in range(cell[0] - 1, cell[0] + 2):
      for j in range(cell[1] - 1, cell[1] + 2):
        # Ignore the cell itself
        if (i, j) == cell:
          continue

        # Update count if cell in bounds and is mine
        if 0 <= i < self.height and 0 <= j < self.width:
          if self.board[i][j]:
            count += 1

    return count

  def won(self):
    """
    Checks if all mines have been flagged.
    """
    return self.mines_found == self.mines


class Sentence():
  """
  Logical statement about a Minesweeper game
  A sentence consists of a set of board cells,
  and a count of the number of those cells which are mines.
  """

  def __init__(self, cells, count):
    self.cells = set(cells)
    self.count = count

  def __eq__(self, other):
    return self.cells == other.cells and self.count == other.count

  def __str__(self):
    return f"{self.cells} = {self.count}"

  def known_mines(self):
    """
    Returns the set of all cells in self.cells known to be mines.
    """
    if len(self.cells) == self.count:
      return self.cells
    return None

  def known_safes(self):
    """
    Returns the set of all cells in self.cells known to be safe.
    """
    if self.count == 0:
      return self.cells
    return None

  def mark_mine(self, cell):
    """
    Updates internal knowledge representation given the fact that a cell is known to be a mine.
    """
    if cell in self.cells:
      self.cells.remove(cell)
      self.count -= 1

  def mark_safe(self, cell):
    """
    Updates internal knowledge representation given the fact that a cell is known to be safe.
    """
    if cell in self.cells:
      self.cells.remove(cell)


class MinesweeperAI():
  """
  Minesweeper game player
  """

  def __init__(self, height=8, width=8):
    # Set initial height and width
    self.height = height
    self.width = width

    # Keep track of which cells have been clicked on
    self.moves_made = set()

    # Keep track of cells known to be safe or mines
    self.mines = set()
    self.safes = set()

    # List of sentences about the game known to be true
    self.knowledge = []

  def mark_mine(self, cell):
    """
    Marks a cell as a mine, and updates all knowledge
    to mark that cell as a mine as well.
    """
    self.mines.add(cell)
    for sentence in self.knowledge:
        sentence.mark_mine(cell)

  def mark_safe(self, cell):
    """
    Marks a cell as safe, and updates all knowledge
    to mark that cell as safe as well.
    """
    self.safes.add(cell)
    for sentence in self.knowledge:
      sentence.mark_safe(cell)
        

  def get_neighbors(self, cell):
    """
    Gets all the neighbors of a cell and return a set for us
    """
    i, j = cell
    neighbors = set()
    for row in range(i-1, i+2):
        for col in range(j-1, j+2):
            if (row >= 0 and col >= 0) and (row < self.height and col < self.width) and (row, col) != (i, j):
                neighbors.add((row, col))
    return neighbors

  
  def add_knowledge(self, cell, count):
    """
    Called when the Minesweeper board tells us, for a given
    safe cell, how many neighboring cells have mines in them.
    
    This function should:
        1) mark the cell as a move that has been made
        2) mark the cell as safe
        3) add a new sentence to the AI's knowledge base
           based on the value of `cell` and `count`
        4) mark any additional cells as safe or as mines
           if it can be concluded based on the AI's knowledge base
        5) add any new sentences to the AI's knowledge base
           if they can be inferred from existing knowledge
    """
    self.moves_made.add(cell) #mark the move as made
    self.mark_safe(cell) #mark the move as safe

   #generate sentence
    neighbors = self.get_neighbors(cell)
    for neigh in neighbors:
      if neigh in self.safes and neigh in self.mines:
        neighbors.remove(neigh)
        
    sentence = Sentence(neighbors, count)

    #add the new sentence to the knowledge db
    self.knowledge.append(sentence)

    #finds new safes and mines
    #!this snippet is inneficient and can break easily
    #!after marking the cells as safe in the sentence we can find new safe sentences
    #!this should be something like:
    #!  get all known safes from the sentences
    #!  mark all the known safes in the sentences (we can make this better by not marking cells that are move_made)
    #!  remove empty knowledge
    #!  somehow loop this shit until there's no new safe cells
    #!    when starting the loop we can count the number of safes and mines, if it doesn't change we can stop the loop
    for knowledge in self.knowledge:
      if knowledge.known_safes() is not None:
        for cell in knowledge.known_safes():
          self.safes.add(cell)
      if knowledge.known_mines() is not None:
        for cell in knowledge.known_mines():
          self.mines.add(cell)

    for sentence in self.knowledge:
      for cell in self.safes:
        sentence.mark_safe(cell)
      for cell in self.mines:
        sentence.mark_mine(cell)
      #!end of snippet to fix

    #new inferences
    while True:
      empty_know = []
      for knowledge in self.knowledge:
        if len(knowledge.cells) == 0:
          empty_know.append(knowledge)
      for empty in empty_know:
        self.knowledge.remove(empty)
      
      inference = None
      have_new_inference = False

      print(f"Knowledge ({len(self.knowledge)})")
      for know in self.knowledge:
        print(f"{know}")
      for knowledge in self.knowledge:
        if knowledge is sentence:
          continue

        print(f"Sentence: {sentence} | Knowledge: {knowledge}")
            
        if knowledge.cells < sentence.cells:
          new_set = sentence.cells - knowledge.cells
          inference = Sentence(new_set, sentence.count - knowledge.count)
          if inference not in self.knowledge:
            print(f"Inference: {inference}")
            have_new_inference = True
          break
        elif sentence.cells < knowledge.cells:
          new_set = knowledge.cells - sentence.cells
          inference = Sentence(new_set, knowledge.count - sentence.count)
          if inference not in self.knowledge:
            print(f"Inference: {inference}")
            have_new_inference = True
          break
          
      #print("Looping")
      if not have_new_inference:
        break
      
      self.knowledge.append(inference)

    #finds new safes and mines
    #!same problems as before (same snippet)
    #!  i should create a function to find safes and mines
    for knowledge in self.knowledge:
      if knowledge.known_safes() is not None:
        for cell in knowledge.known_safes():
          self.safes.add(cell)
      if knowledge.known_mines() is not None:
        for cell in knowledge.known_mines():
          self.mines.add(cell)

    for sentence in self.knowledge:
      for cell in self.safes:
        sentence.mark_safe(cell)
      for cell in self.mines:
        sentence.mark_mine(cell)

    print(f"\n\nMines: ({len(self.mines)})")
    for mine in self.mines:
      print(f"{mine}")

    print(f"Safes: ({len(self.safes) - len(self.moves_made)})")
    for safe in self.safes:
      if safe not in self.moves_made:
        print(f"{safe}")

    print(f"Knowledge ({len(self.knowledge)})")
    for know in self.knowledge:
      print(f"{know}")

  def make_safe_move(self):
    """
    Returns a safe cell to choose on the Minesweeper board.
    The move must be known to be safe, and not already a move
    that has been made.

    This function may use the knowledge in self.mines, self.safes
    and self.moves_made, but should not modify any of those values.
    """
    for cell in self.safes:
      if cell not in self.moves_made:
        return cell
    return None

  def make_random_move(self):
    """
    Returns a move to make on the Minesweeper board.
    Should choose randomly among cells that:
        1) have not already been chosen, and
        2) are not known to be mines
    """
    if len(self.moves_made) + len(self.mines) == self.width * self.height:
      return None

    i = random.randrange(self.height)
    j = random.randrange(self.width)
    move = (i, j)
    while move in self.moves_made or move in self.mines:
      i = random.randrange(self.height)
      j = random.randrange(self.width)
      move = (i, j)

    return move
