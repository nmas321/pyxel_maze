import pyxel
import random

def generateMaze(w, h):
  directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
  grid = [[0 for _ in range(h)] for _ in range(w)]
  
  for x in range(w):
    for y in range(h):
      grid[x][y] = '#'
  
  def is_valid(x, y):
    return 0 <= x < w and 0 <= y < h
      
  def choose_starting_point():
    return random.randint(0, int(w / 2) - 1) * 2 + 1, random.randint(0, int(h / 2) - 1) * 2 + 1

  def walk_path(x, y):
    path = [(x, y)]
    while grid[x][y] == '#':
      direction = random.choice(directions)
      tdirection = (direction[0] * 2, direction[1] * 2)
      nx1, ny1 = x + direction[0], y + direction[1]
      nx, ny = x + tdirection[0], y + tdirection[1]
      if not is_valid(nx, ny):
        continue
      if(nx, ny) in path:
        start = path.index((nx, ny))
        path = path[:start + 1]
      else:
        path.append((nx1, ny1))
        path.append((nx, ny))
      x, y = nx, ny
    return path
  
  grid[1][1] = ' '
  maxlength = -1
  for i in range(w * h - 1):
    x, y = choose_starting_point()
    path = walk_path(x, y)
    for nx, ny in path:
      grid[nx][ny] = ' '
    if maxlength < len(path):
      maxlength = len(path)
      gx, gy = (x, y)
  grid[1][1] = 's'
  grid[gx][gy] = 'g'
  return grid, (1, 1), (gx, gy)

class App:
  def __init__(self):
    pyxel.init(240, 240, title="maze")
    pyxel.load("resource.pyxres")
    self.levelmap = [9, 13, 15, 35, 45, 63]
    self.level = 0
    self.grid, (self.player_x, self.player_y), (self.goal_x, self.goal_y) = generateMaze(self.levelmap[self.level], self.levelmap[self.level])
    self.clear = -1
    self.allclear = False
    self.before = None
    pyxel.playm(0, loop=True)
    pyxel.run(self.update, self.draw)

  def update(self):
    self.update_state()
    self.draw()
    
  def btns(self, keys):
    for k in keys:
      if pyxel.btn(k):
        return True
    return False

  def update_state(self):
    
    if self.before != pyxel.KEY_LEFT and self.btns([pyxel.KEY_LEFT, pyxel.KEY_A]) and self.grid[self.player_x-1][self.player_y] != '#':
      self.player_x -= 1
      self.before = pyxel.KEY_LEFT
    elif self.before != pyxel.KEY_RIGHT and self.btns([pyxel.KEY_RIGHT, pyxel.KEY_D]) and self.grid[self.player_x+1][self.player_y] != '#':
      self.player_x += 1
      self.before = pyxel.KEY_RIGHT
    elif self.before != pyxel.KEY_UP and self.btns([pyxel.KEY_UP, pyxel.KEY_W]) and self.grid[self.player_x][self.player_y-1] != '#':
      self.player_y -= 1
      self.before = pyxel.KEY_UP
    elif self.before != pyxel.KEY_DOWN and self.btns([pyxel.KEY_DOWN, pyxel.KEY_S]) and self.grid[self.player_x][self.player_y+1] != '#':
      self.player_y += 1
      self.before = pyxel.KEY_DOWN
    else:
      self.before = None

    if self.clear == -1 and self.player_x == self.goal_x and self.player_y == self.goal_y:
      self.clear = 90
    if self.clear != -1:
      self.clear -= 1
    if self.clear == 0:
      self.level += 1
      if(self.level < len(self.levelmap)):
        self.grid, (self.player_x, self.player_y), (self.goal_x, self.goal_y) = generateMaze(self.levelmap[self.level], self.levelmap[self.level])
      else:
        self.allclear = True
      self.clear = -1
      
  def draw(self):
    pyxel.cls(0)
    if self.allclear == True:
      cleartext = 'Stage All Clear!'
      pyxel.text(pyxel.width/2 - 25, pyxel.height/2, cleartext, pyxel.frame_count % 16)
      return
      
    if self.clear != -1:
      cleartext = 'Clear stage ' + str(self.level + 1) + "!"
      pyxel.text(pyxel.width/2 - 25, pyxel.height/2, cleartext, pyxel.frame_count % 16)
      return
    
    s = pyxel.width / (self.levelmap[self.level] * 8)
    for i in range(len(self.grid)):
      for j in range(len(self.grid[0])):
        if self.grid[i][j] == '#':
          pyxel.blt(
              i * (8 * s) + 4*s - 4,
              j * (8 * s) + 4*s - 4,
              0, 0, 8, 8, 8, scale=s)

    pyxel.blt(
        self.player_x * (8 * s) + 4*s - 4,
        self.player_y * (8 * s) + 4*s - 4,
        0, 0, 0, 7, 8, scale=s)
    
    pyxel.blt(
        self.goal_x * (8 * s) + 4*s - 4,
        self.goal_y * (8 * s) + 4*s - 4,
        0, 8, 0, 8, 8, scale=s)

App()