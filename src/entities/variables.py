FPS = 15
SCREENWIDTH  = 288.0
SCREENHEIGHT = 512.0
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

load_saved_pool = 0
save_current_pool = 1
current_pool = []
fitness = []
total_models = 10

next_pipe_x = -1
next_pipe_hole_y = -1
generation = 1