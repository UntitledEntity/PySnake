import os, time, threading
import random
import keyboard #pip3 install keyboard

# Each line is 16 spaces long
base_line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
main_matrix = []

# Head location of the snake
snake_head_location = [3,3]

# History of the snake head positions
snake_head_history = []

# Length of snake
snake_len = 3

current_apple_location = [3,6]

time_since_last_move = 3

def clamp(var, a, b):
  ret = var
  if ret < a:
    ret = a
  if ret > b:
    ret = b

  return ret

def clear_env():
  for i in range(0, 16):
    main_matrix.append(list(base_line))

def print_debug():
  for i in range(0, 16):
    print(main_matrix[i])

def change_square_space(line, column, state):
  #print("Changing point (" + str(line) + "," + str(column) + ") to " + str(state))
  line_state = main_matrix[line]
  #print("Old line: " + str(line_state))
  line_state[column] = state
  #print("New line: " + str(line_state))

  main_matrix[line][column] = state

def get_square_space(line,column):
  line_state = main_matrix[line]
  return line_state[column]

def on_death():
  os.system("cls")
  print("You lost haha")
  exit(0)

# Goes through the matrix and prints either a space or a 'W' char depending on the space state.
def render_envornment():
  print("\n\n")
  for i in range(0, 17):
    if i != 0 and i != 17:
      cur_line = main_matrix[i - 1]
    #print(cur_line)
    for n in range(0, 16):
      if i == 0 or i == 17:
        lnend = ""
        if n == 15: 
          lnend = "\n"

        print("-" + lnend, end="")
      else:
        lnend = ""
        if n == 15: 
          lnend = "|\n"
        lnbegin = ""
        if n == 0:
          lnbegin = "|"
        if cur_line[n] == 1:
          print(lnbegin + "+" + lnend, end="")  
        elif cur_line[n] == 2:
          print(lnbegin + "A" + lnend, end="")
        else:
          print(lnbegin + " " + lnend, end="")

def spawn_apple(amount):
  global current_apple_location

  for i in range(0, amount):
    line = random.randint(0, 15)
    column = random.randint(0, 15)

    if get_square_space(line,column) == 0:
      change_square_space(line,column,2)
      current_apple_location = [line, column]
    else:
      spawn_apple(amount)

def check_apple():
  global snake_len, current_apple_location
  print("Current apple location: " + str(current_apple_location))

  if snake_head_location == current_apple_location:
    snake_len += 1
    spawn_apple(1)

def move_snake(direction, vertical):
  global snake_head_location, snake_head_history
  # Set old snake head to current snake head
  snake_head_history.insert(0, snake_head_location)
  old_snake_head_location = snake_head_location
  # Max size of 256
  if len(snake_head_history) > 255:
    snake_head_history.pop()

  #print("Direction: " + str(direction) + ", Vertical:" + str(vertical))

  # Need to loop through length of snake but for now just move head
  
  if len(snake_head_history) > snake_len:
    change_square_space(snake_head_history[snake_len][0], snake_head_history[snake_len][1], 0)

  # Set new snake head location to old + 1
  if vertical:
    snake_head_location = [old_snake_head_location[0] + direction, old_snake_head_location[1]]
  else:
    snake_head_location = [old_snake_head_location[0], old_snake_head_location[1] + direction]

  if snake_head_location[0] > 15:
    #snake_head_location[0] = 0
    on_death()
  if snake_head_location[1] > 15:
    #snake_head_location[1] = 0
    on_death()

  if snake_head_location[0] < 0:
    #snake_head_location[0] = 15
    on_death()
  if snake_head_location[1] < 0:
    #snake_head_location[1] = 15
    on_death()

  # Snake eats itself
  if get_square_space(snake_head_location[0], snake_head_location[1]) == 1:
    on_death()

  change_square_space(snake_head_location[0], snake_head_location[1], 1)   

  for i in range(0,3):
    if len(snake_head_history) > snake_len:
      change_square_space(snake_head_history[i][0], snake_head_history[i][1], 1)    
  
cur_direction = 1
vertical = False
def handle_keys():
  global cur_direction, vertical
  if ( keyboard.is_pressed('A') or keyboard.is_pressed('left') ) and ( cur_direction != 1 or vertical == True ):
    cur_direction = -1
    vertical = False
  elif ( keyboard.is_pressed('D') or keyboard.is_pressed('right') ) and ( cur_direction != -1 or vertical == True ):
    cur_direction = 1
    vertical = False
  elif ( keyboard.is_pressed('W') or keyboard.is_pressed(keyboard.KEY_UP) ) and ( cur_direction != 1 or vertical == False):
    cur_direction = -1
    vertical = True
  elif ( keyboard.is_pressed('S') or keyboard.is_pressed(keyboard.KEY_DOWN) ) and ( cur_direction != -1 or vertical == False):
    cur_direction = 1
    vertical = True

def convert_speed_to_rf(speed: int):
  if (speed == 1): return 0.25
  if (speed == 2): return 0.10
  if (speed == 3): return 0.05
  if (speed == 4): return 0.04
  if (speed == 5): return 0.03
  if (speed == 6): return 0.01
  if (speed > 6): return 0.001
  if (speed < 1): return 1

def __main__():
  # Bring the global snake head location var into the main function
  global snake_head_location, time_since_last_move

  set_speed = False

  while not set_speed: 
    try:
      speed = int(input("Input the speed [1: Slower, 2: Slow, 3: Medium, 4: Fast, 5: Faster, 6: Speedy]: "))
      set_speed = True
    except ValueError:
      print("Speed must be an integer")

  refresh_rate = convert_speed_to_rf(speed)

  clear_env()
  
  # Spawn initial snake and apple
  change_square_space(3, 3, 1)
  change_square_space(3, 6, 2)
    
  # Create a thread for handle_keys function
  keys_thread = threading.Thread(target=handle_keys)

  # Start the thread
  keys_thread.start()

  while True:
    os.system("cls")
    
    time_since_last_move += 1

    print("Current snake length: " + str(snake_len))

    handle_keys()
    check_apple()

    if time_since_last_move > 2:
      move_snake(cur_direction, vertical)
      time_since_last_move = 0
    
    render_envornment()
    time.sleep(refresh_rate)
    


__main__()
