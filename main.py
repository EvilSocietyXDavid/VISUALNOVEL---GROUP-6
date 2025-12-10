from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random, json, os
from story import story
from finalmaze import play_maze
import pygame as pygame
pygame.mixer.init()
pygame.mixer.music.load("LEMAO.mp3")
pygame.mixer.music.play(-1)


# === DATA STRUCTURES ===
class SceneStack:
   def __init__(self):
       self.stack = []

   def push(self, scene):
       self.stack.append(scene)

   def pop(self):
       return self.stack.pop() if self.stack else None

   def is_empty(self):
       return len(self.stack) == 0


class StoryLog:
   def __init__(self):
       self.log = []

   def add_entry(self, scene, choice):
       self.log.append(f"{scene}: {choice}")

   def get_log(self):
       return self.log

   def __str__(self):
       return "\n".join(self.log)


class Character:
   def __init__(self, name, affection=50, courage=50, health=100):
       self.name = name
       self.affection = affection
       self.courage = courage

   def __str__(self):
       return f"{self.name} | Affection:{self.affection} | Courage:{self.courage}"


# === RANDOM HORROR QUOTE ===
def get_horror_quote():
   quotes = [
       "Are you sure you can live with that decision?",
       "You can run from fear, but it follows in silence.",
       "The forest was not even the scariest part.",
       "Not all who wander are lost… some are hunted.",
       "Something deep within the forest smiles at you."
   ]
   return random.choice(quotes)


# === MAIN GAME CLASS ===
class StoryGame:
   WINDOW_W = 1200
   WINDOW_H = 1400
   BG_H = 380
   BG_w = 400

   def __init__(self):
       self.window = Tk()
       self.window.iconphoto(False, PhotoImage(file="kakako.png"))
       self.window.title("My Monster Crush")
       self.window.geometry(f"{self.WINDOW_W}x{self.WINDOW_H}")
       self.window.resizable(True, True)
       self.window.configure(bg="#000")

       self.current_scene = "start"
       self.scene_history = SceneStack()
       self.log = StoryLog()
       self.name = ""
       self.player = None

       # === CANVAS ===
       self.canvas = Canvas(
           self.window,
           bg="#000",
           highlightthickness=0,
           width=self.WINDOW_W,
           height=self.BG_H
       )
       self.canvas.place(x=0, y=0)

       # === DIALOGUE FRAME ===
       dialogue_height = self.WINDOW_H - self.BG_H
       self.dialogue_frame = Frame(self.window, bg="#111")
       self.dialogue_frame.place(
           x=0, y=self.BG_H, width=self.WINDOW_W, height=dialogue_height
       )
       self.dialogue_frame.pack_propagate(False)

       # === MENU BAR ===
       self.create_menu()

       self.bg_image = None
       self.char_image = None

       # Start at main menu
       self.show_main_menu()

   # === MENU BAR ===
   def create_menu(self):
       menubar = Menu(self.window)
       file_menu = Menu(menubar, tearoff=0)
       file_menu.add_command(label="Main Menu",command=self.show_main_menu)
       file_menu.add_command(label="Save", command=self.save_game)
       file_menu.add_command(label="Load", command=self.load_game)
       file_menu.add_separator()
       file_menu.add_command(label="Exit", command=self.exit_game)
       menubar.add_cascade(label="Menu", menu=file_menu)
       self.window.config(menu=menubar)

   # === UTILITIES ===
   def clear_dialogue(self):
       for w in self.dialogue_frame.winfo_children():
           w.destroy()

   def show_background(self, filename):
       try:
           img = Image.open(filename).convert('RGBA')
           img = img.resize((self.WINDOW_W, self.BG_H), Image.LANCZOS)
           self.bg_image = ImageTk.PhotoImage(img)
           self.canvas.delete("bg")
           self.canvas.create_image(0, 0, anchor=NW, image=self.bg_image, tags=("bg",))
           self.canvas.tag_lower("bg")
       except Exception as e:
           print(f"Missing background: {filename} ({e})")
           self.canvas.delete("bg")

   def show_character(self, filename):
       try:
           img = Image.open(filename).convert('RGBA')
           max_w, max_h = 420, 470
           w, h = img.size
           scale = min(max_w / w, max_h / h, 1)
           img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
           self.char_image = ImageTk.PhotoImage(img)
           x = self.WINDOW_W - img.width - 20
           y = 10
           self.canvas.delete("char")
           self.canvas.create_image(x, y, anchor=NW, image=self.char_image, tags=("char",))
           self.canvas.tag_raise("char", "bg")
       except Exception as e:
           # remove char if missing
           # print(f"Missing character image: {filename} ({e})")
           self.canvas.delete("char")

   def save_game(self):
       if not self.player:
           messagebox.showwarning("Save Error", "Start the game before saving!")
           return
       data = {
           "name": self.player.name,
           "affection": self.player.affection,
           "courage": self.player.courage,
           "current_scene": self.current_scene,
           "log": self.log.get_log()
       }
       with open("savefile.json", "w") as f:
           json.dump(data, f, indent=4)
       messagebox.showinfo("Saved", "Progress saved successfully!")

   def load_game(self):
       if not os.path.exists("savefile.json"):
           messagebox.showwarning("Load Error", "No save file found.")
           return
       with open("savefile.json", "r") as f:
           data = json.load(f)
       self.player = Character(
           data.get("name", "Player"),
           affection=data.get("affection", 50),
           courage=data.get("courage", 50)
       )
       self.current_scene = data.get("current_scene", "start")
       self.log.log = data.get("log", [])
       self.display_scene()
       messagebox.showinfo("Loaded", "Game loaded successfully!")

   def exit_game(self):
       if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
           self.window.destroy()

   # === MAIN MENU ===
   def show_main_menu(self):
       self.clear_dialogue()
       self.canvas.delete("all")
       self.show_background("background2.png")


       Button(self.dialogue_frame, text="New Game",
              command=self.display_name_entry, bg="#b22222",font=("Arial", 18, "bold"),
              fg="white", width=20).pack(pady=5)

       Button(self.dialogue_frame, text="Load Game",
              command=self.load_game, bg="#444",font=("Arial", 18, "bold"),
              fg="white", width=20).pack(pady=5)

       Button(self.dialogue_frame, text="Exit",
              command=self.exit_game, bg="#222",font=("Arial", 18, "bold"),
              fg="white", width=20).pack(pady=5)

   # === NAME ENTRY ===
   def display_name_entry(self):
       self.clear_dialogue()
       self.canvas.delete("char")
       self.show_background("backgound1.jpeg")

       Label(self.dialogue_frame, text="Enter your name:",
             fg="white", bg="#111",
             font=("Arial", 18, "bold")).pack(pady=5)

       self.name_entry = Entry(self.dialogue_frame,
                               font=("Arial", 18), width=27)
       self.name_entry.pack(pady=5)

       Button(self.dialogue_frame, text="Start Game",
              command=self.start_game,font=("Arial", 18, "bold"),
              bg="#8b0000", fg="white", width=12).pack(pady=5)

       Button(self.dialogue_frame, text="Back",
              command=self.show_main_menu,font=("Arial", 18, "bold"),
              bg="#444", fg="white", width=8).pack(pady=2)

       def clear_dialogue(self):
           for w in self.dialogue_frame.winfo_children():
               w.destroy()

       def start_game(self):
           self.name = self.name_entry.get().strip()
           if not self.name:
               messagebox.showwarning("Missing Name", "⚠️ Please enter your name before starting the game.")
               return

           self.player = Character(self.name)
           for widget in self.window.winfo_children():
               widget.destroy()
           self.display_scene()

   # === START GAME ===
   def start_game(self):
       self.name = self.name_entry.get().strip()

       # VALIDATION: name must contain at least one letter
       if not self.name or not any(ch.isalpha() for ch in self.name):
           messagebox.showwarning(
               "Invalid Name",
               "⚠️ Your name must include at least one letter.\n"
               "Numbers and symbols alone are not allowed."
           )
           return

       self.player = Character(self.name)
       self.current_scene = "start"
       self.display_scene()

   # === DISPLAY SCENE ===
   def display_scene(self):
       # Special case: minigame result scene
       if self.current_scene == "minigame_result":
           result = play_maze(self.window)

           if result.get("won"):
               aff = result.get("affection", 0)
               cour = result.get("courage", 0)

               self.player.affection += aff
               self.player.courage += cour

               messagebox.showinfo(
                   "Maze Result",
                   f"You escaped!\n\n"
                   f"+{aff} Affection\n"
                   f"+{cour} Courage"
               )

               self.current_scene = "event"

           else:
               cour = result.get("courage", 0)

               self.player.courage += cour

               messagebox.showinfo(
                   "Maze Result",
                   f"You were caught!\n\n"
                   f"{cour} Courage"
               )

               self.current_scene = "escape"

           self.display_scene()
           return

       # Normal scenes
       self.clear_dialogue()

       scene = story.get(self.current_scene, None)
       if not scene:
           messagebox.showerror("Scene Error", f"Scene '{self.current_scene}' not found.")
           return

       # If the scene is explicitly an ending, show ending screen
       is_ending_flag = scene.get("is_ending", False)

       # Background + Character
       if scene.get("image"):
           self.show_background(scene["image"])
       else:
           self.show_background("background1.jpg")

       if scene.get("character"):
           self.show_character(scene["character"])
       else:
           self.canvas.delete("char")

       # If scene has no choices (or marked as ending), display ending
       choices = scene.get("choices", None)
       no_choices = (choices is None) or (isinstance(choices, list) and len(choices) == 0)

       # Stats label
       Label(self.dialogue_frame, text=f"{self.player}",
             fg="#ccc", bg="#111",
             font=("Arial", 14, "italic")).pack()

       # Dialogue text
       Label(self.dialogue_frame,
             text=scene.get("text", "").format(name=self.name),
             wraplength=600, justify="left",
             bg="#111", fg="white",
             font=("Arial", 14)).pack(pady=4)

       if is_ending_flag or no_choices:
           # Directly show ending screen for endings
           self.display_ending_screen()
           return

       # Choices
       if choices:
           for choice in choices:

               def make_cmd(ch=choice):
                   req = scene.get("requires_courage") or ch.get("requires_courage")
                   if req and self.player.courage < req:
                       messagebox.showinfo("Can't do that", f"You need at least {req} courage.")
                       return

                   aff = ch.get("affection", 0)
                   cour = ch.get("courage", 0)

                   if aff != 0 or cour != 0:
                       self.player.affection += aff
                       self.player.courage += cour
                       self._show_stat_change(aff, cour)

                   self.scene_history.push(self.current_scene)
                   self.log.add_entry(self.current_scene, ch.get("text", "(choice)"))

                   nxt = ch.get("next_scene")
                   if nxt == "ending_check":
                       self._handle_ending_check()
                   else:
                       self.current_scene = nxt
                       self.display_scene()

               Button(
                   self.dialogue_frame, text=choice["text"],
                   font=("Arial", 14), bg="#b22222", fg="white",
                   activebackground="#8b0000", width=36,
                   command=make_cmd
               ).pack(pady=3)
       else:
           # No choices found -> fallback to ending
           self.display_ending_screen()

   # === FLOATING STAT CHANGE LABEL ===
   def _show_stat_change(self, aff, cour):
       txt = []
       if aff:
           txt.append(f"Affection {'+' if aff > 0 else ''}{aff}")
       if cour:
           txt.append(f"Courage {'+' if cour > 0 else ''}{cour}")

       float_lbl = Label(self.dialogue_frame,
                         text=", ".join(txt),
                         fg="#ffb3b3", bg="#111",
                         font=("Arial", 14, "bold"))
       float_lbl.pack()
       self.window.after(1200, float_lbl.destroy)

   # === ENDING CHECK ===
   def _handle_ending_check(self):
       a = self.player.affection
       c = self.player.courage

       if a >= 80 and c >= 70:
           self.current_scene = "best"
       elif a >= 60 and c >= 40:
           self.current_scene = "good"
       elif c >= 70 and a < 40:
           self.current_scene = "rejection"
       elif a < 30 and c < 30:
           self.current_scene = "death"
       else:
           self.current_scene = "end_hunter"

       self.display_scene()

   # === END SCREEN ===
   def display_ending_screen(self):
       # show ending scene from story if available
       scene = story.get(self.current_scene, {})

       # Use designated ending background if provided
       bg = scene.get("image") or "background1.jpg"
       self.show_background(bg)

       # Optionally show a large ending image (separate key 'ending_image')
       ending_img_path = scene.get("ending_image") or scene.get("character")
       if ending_img_path:
           try:
               img = Image.open(ending_img_path).convert('RGBA')
               # scale image to fit dialogue area height
               dlg_h = self.WINDOW_H - self.BG_H - 40
               max_w = self.WINDOW_W - 40
               w, h = img.size
               scale = min(max_w / w, dlg_h / h, 1)
               img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
               self.end_img_tk = ImageTk.PhotoImage(img)
               # place on canvas centered inside the top BG area
               self.canvas.delete("ending")
               x = (self.WINDOW_W - img.width) // 2
               y = max(10, (self.BG_H - img.height) // 2)
               self.canvas.create_image(x, y, anchor=NW, image=self.end_img_tk, tags=("ending",))
               self.canvas.tag_raise("ending", "bg")
           except Exception as e:
               # print(f"No ending image: {ending_img_path} ({e})")
               self.canvas.delete("ending")
       else:
           self.canvas.delete("ending")

       self.clear_dialogue()

       Label(self.dialogue_frame, text="🎃 The End 🎃",
             font=("Arial", 14, "bold"),
             bg="#111", fg="red").pack(pady=4)

       # Ending description text
       Label(self.dialogue_frame, text=scene.get("text", get_horror_quote()),
             wraplength=600, bg="#111",
             fg="white", font=("Arial", 10)).pack(pady=2)

       # Random horror quote
       quote = get_horror_quote()
       Label(self.dialogue_frame, text=quote,
             wraplength=600, bg="#111",
             fg="#ffcccc", font=("Arial", 8, "italic")).pack(pady=2)

       Label(self.dialogue_frame, text="🕯 Your Choices:",
             font=("Arial", 10, "bold"),
             bg="#111", fg="white").pack(pady=3)

       log_box = Text(self.dialogue_frame,
                      width=72, height=4,
                      wrap=WORD, bg="#222",
                      fg="white", font=("Arial", 8))
       log_box.pack(pady=2)
       log_box.insert(END, str(self.log))
       log_box.config(state=DISABLED)

       Button(self.dialogue_frame, text="Main Menu",
              command=self.show_main_menu,font=("Arial", 18, "bold"),
              bg="#444", fg="white", width=12).pack(pady=4)

       #Button(self.dialogue_frame, text="Exit",
             # command=self.exit_game,
            #  bg="#8b0000", fg="white", width=12).pack(pady=2)

   # === RUN GAME ===
   def run(self):
       self.window.mainloop()


if __name__ == "__main__":
   StoryGame().run()
