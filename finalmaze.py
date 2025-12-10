from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import random
import pygame as pygame
pygame.mixer.init()
pygame.mixer.music.load("boss.mp3")
pygame.mixer.music.play(-1)

TILE_SIZE = 90
ROWS, COLS = 8, 10

WIN_REWARD = {"won": True, "affection": 25, "courage": 20}
LOSE_REWARD = {"won": False, "courage": -20}

def load_gif_frames(path):
    img = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("RGBA").resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))
    return frames


def play_maze(parent=None):
    result = {"won": False}
    lives = 3   # ---------------- NEW ----------------

    def run_level(level_number):
        nonlocal result, lives

        maze_root = Toplevel(parent) if parent else Tk()
        maze_root.title(f"Maze Level {level_number}")

        if parent:
            maze_root.transient(parent)
            maze_root.grab_set()

        maze_root.focus_force()

        def load_tile(path):
            try:
                img = Image.open(path).convert("RGBA").resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except:
                blank = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (60, 120, 60))
                return ImageTk.PhotoImage(blank)

        grass = load_tile("grass.jpg")
        tree = load_tile("tree.jpg")
        door = load_tile("church.png")
        patrol_img = load_tile("aswang.png")
        aswang_frames = [load_tile("aswang.png")]

        player_frames = load_gif_frames("Player1.png")
        PLAYER_FRAME_SPEED = 80

        # ------------------------ LEVEL MAPS INCLUDING LEVEL 3 ------------------------
        LEVEL_MAPS = {
            1: [
                [0, 0, 0, 1, 0, 0, 0, 0, 1, 2],
                [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 0, 1, 1, 0]
            ],
            2: [
                [0, 0, 1, 0, 0, 0, 1, 0, 0, 2],
                [0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                [0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 1, 1, 1, 0]
            ],
            3: [   # ---------------- NEW LEVEL ----------------
                [0, 1, 0, 0, 1, 0, 0, 1, 0, 2],
                [0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }

        maze_map = LEVEL_MAPS[level_number]

        # -------------------------------------------------------------------
        # NOTES DISPLAY (Controls + Lives + Goal)
        # -------------------------------------------------------------------
        info_label = Label(
            maze_root,
            text=f"Controls: W A S D or Arrow Keys | Goal: Reach the Church | Lives: {lives}",
            font=("Arial", 14),
            fg="white",
            bg="black"
        )
        info_label.grid(row=0, column=0, columnspan=8, sticky="we")

        canvas = Canvas(maze_root, width=COLS * TILE_SIZE, height=ROWS * TILE_SIZE)
        canvas.grid(row=1, column=0, columnspan=8)

        # Draw tiles
        for r in range(ROWS):
            for c in range(COLS):
                tile = maze_map[r][c]
                img = grass if tile == 0 else tree if tile == 1 else door
                canvas.create_image(c * TILE_SIZE, r * TILE_SIZE, image=img, anchor=NW)

        # POSITIONS
        player_pos = [0, 0]

        # Aswang spawn changes per level
        if level_number == 1:
            aswang_pos = [7, 9]
            patrollers = []
        elif level_number == 2:
            aswang_pos = [7, 1]
            patrollers = [
                {"type": "horizontal", "row": 6, "col": 1,
                 "col_min": 1, "col_max": 8, "dir": 1, "speed": 350,
                 "sprite_pos": (6, 1), "sprite": None},
                {"type": "vertical", "col": 4, "row": 1,
                 "row_min": 1, "row_max": 6, "dir": 1, "speed": 350,
                 "sprite_pos": (1, 4), "sprite": None}
            ]
        else:  # LEVEL 3
            aswang_pos = [7, 5]
            patrollers = [
                {"type": "horizontal", "row": 4, "col": 1, "col_min": 1, "col_max": 8,
                 "dir": 1, "speed": 280, "sprite_pos": (4, 1), "sprite": None},
                {"type": "vertical", "col": 3, "row": 0, "row_min": 0, "row_max": 6,
                 "dir": 1, "speed": 280, "sprite_pos": (0, 3), "sprite": None},
                {"type": "horizontal", "row": 6, "col": 2, "col_min": 2, "col_max": 7,
                 "dir": -1, "speed": 260, "sprite_pos": (6, 2), "sprite": None}
            ]

        player = canvas.create_image(0, 0, image=player_frames[0], anchor=NW)
        aswang = canvas.create_image(aswang_pos[1] * TILE_SIZE, aswang_pos[0] * TILE_SIZE,
                                     image=aswang_frames[0], anchor=NW)

        player_anim_index = 0
        walking = False

        def animate_player():
            nonlocal player_anim_index
            if walking:
                player_anim_index = (player_anim_index + 1) % len(player_frames)
                canvas.itemconfig(player, image=player_frames[player_anim_index])
            maze_root.after(80, animate_player)

        animate_player()

        for p in patrollers:
            r, c = p["sprite_pos"]
            p["sprite"] = canvas.create_image(c * TILE_SIZE, r * TILE_SIZE, image=patrol_img, anchor=NW)

        game_over = False

        # ------------------------ COLLISION HANDLING WITH LIVES ------------------------
        # ------------------------ HIT + RESET PLAYER ------------------------
        def take_hit():
            nonlocal lives, game_over, player_pos

            lives -= 1
            info_label.config(text=f"Controls: W A S D / Arrows | Goal: Reach the Church | Lives: {lives}")

            if lives <= 0:
                game_over = True
                result.update(LOSE_REWARD)
                maze_root.destroy()
                return

            # RESET PLAYER TO START POSITION
            player_pos = [0, 0]
            canvas.coords(player, 0, 0)

            return

        def check_collision():
            r, c = player_pos

            # Hit main aswang
            if [r, c] == aswang_pos:
                take_hit()
                return

            # Hit patrollers
            for p in patrollers:
                if (r, c) == p["sprite_pos"]:
                    take_hit()
                    return

        # --------------------- ASWANG MOVEMENT ----------------------
        def move_aswang():
            nonlocal aswang_pos
            if game_over:
                return

            r, c = aswang_pos
            pr, pc = player_pos

            nr, nc = r, c
            if pr < r:
                nr -= 1
            elif pr > r:
                nr += 1
            elif pc < c:
                nc -= 1
            elif pc > c:
                nc += 1

            if 0 <= nr < ROWS and 0 <= nc < COLS and maze_map[nr][nc] != 1:
                aswang_pos = [nr, nc]
                canvas.coords(aswang, nc * TILE_SIZE, nr * TILE_SIZE)

            check_collision()
            speed = 550 - (level_number * 80)
            maze_root.after(max(150, speed), move_aswang)

        move_aswang()

        # --------------------- PATROLLER MOVEMENT ----------------------
        def move_patroller(p):
            if game_over:
                return

            if p["type"] == "horizontal":
                r = p["row"]
                c = p["col"] + p["dir"]
                if c > p["col_max"] or c < p["col_min"]:
                    p["dir"] *= -1
                    c += p["dir"]
                p["col"] = c

            else:  # vertical
                c = p["col"]
                r = p["row"] + p["dir"]
                if r > p["row_max"] or r < p["row_min"]:
                    p["dir"] *= -1
                    r += p["dir"]
                p["row"] = r

            p["sprite_pos"] = (p["row"], p["col"])
            rr, cc = p["sprite_pos"]
            canvas.coords(p["sprite"], cc * TILE_SIZE, rr * TILE_SIZE)

            check_collision()
            maze_root.after(p["speed"], lambda: move_patroller(p))

        for p in patrollers:
            move_patroller(p)

        # --------------------- PLAYER MOVEMENT ----------------------
        def move_player(dr, dc):
            nonlocal walking, player_pos

            r, c = player_pos
            nr, nc = r + dr, c + dc

            walking = True

            if 0 <= nr < ROWS and 0 <= nc < COLS and maze_map[nr][nc] != 1:
                player_pos = [nr, nc]
                canvas.coords(player, nc * TILE_SIZE, nr * TILE_SIZE)

                if maze_map[nr][nc] == 2:
                    maze_root.destroy()
                    return

                check_collision()

            walking = False

        def on_key(event):
            k = event.keysym.lower()
            if k in ("w", "up"): move_player(-1, 0)
            elif k in ("s", "down"): move_player(1, 0)
            elif k in ("a", "left"): move_player(0, -1)
            elif k in ("d", "right"): move_player(0, 1)

        maze_root.bind("<KeyPress>", on_key)
        maze_root.wait_window()
        return not game_over

    if run_level(1):
        if run_level(2):
            if run_level(3):
                result.update(WIN_REWARD)

    return result
