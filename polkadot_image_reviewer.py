import os
import sys
import shutil
import subprocess
from types import SimpleNamespace
from tkinter import *
from tkinter import filedialog, messagebox

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore
    DND_AVAILABLE = True
except Exception:
    # Fallback if tkinterdnd2 is not available
    TkinterDnD = SimpleNamespace(Tk=Tk)
    DND_FILES = None
    DND_AVAILABLE = False

from PIL import Image, ImageTk

try:
    import icu
    collator = icu.Collator.createInstance(icu.Locale('en_US.UTF-8'))
except Exception:
    collator = None


# ---------- Configuration ----------
appName = "PolkaDot Image Reviewer, Ver. 2508130626 (Zoom+)"

SOURCE_FOLDER = os.path.expanduser("~")
SORTED_FOLDER = os.path.abspath(os.path.join(os.getcwd(), "../SELECTED/__SORTING"))
CONFIG_FILE = os.path.abspath(os.path.join(os.getcwd(), "config.txt"))
FAVORITE = "__XXZ_FAVORITE"

APP_DIR = os.path.dirname(os.path.abspath(__file__))
TSV_FILE = os.path.join(APP_DIR, "starred.tsv")

DEFAULT_PRESETS = {
    '1': ('1️⃣ R', '__1A_REVIEW_STEP1_SMALL_TO_1B'),
    '2': ('2️⃣ R', '__1B_REVIEW_STEP2_SMALL_TO_2A'),
    '3': ('🆙 UPSCALE', '__2A_TO_UPSCALE_NEXT_2B'),
    '4': ('🗑️ DEL', '__XXE_TO_DELETE'),

    '5': ('🆙 READY', '__6B_UPSCALED_STEP2_TO_7A_or_7B'),

    '6': ('✅ NSFW', '__7A_FINAL_NSFW_0000'),
    '7': ('✅ SFW',  '__7B_FINAL_SFW_0000'),

    '8': ('📱 SOC', '__XXB_SOCIAL'),
    '9': ('📦 ASIDE', '__XXA_ASIDE'),
    '0': ('🛠 FIX', '__XXC_FIXREQUIRED'),
    '-': ('⛔ BORDER', '__XXC_BORDERLINE'),
    '=': ('❓ TEMP', '__XXD_TEMP'),
}


# ---------- Persistence Helpers ----------
def save_last_folder(path: str) -> None:
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(path)
    except Exception as e:
        print("Could not save config:", e)


def load_last_folder() -> str:
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                path = f.read().strip()
                if os.path.isdir(path):
                    return path
    except Exception as e:
        print("Could not load config:", e)
    return ""


def natural_sort_key(s: str):
    if collator:
        return collator.getSortKey(s)
    return s.lower()


# ---------- Main App ----------
class ImageSorter:
    def __init__(self, root):
        self.root = root
        self.root.title(appName)
        self.root.minsize(1200, 800)

        if DND_AVAILABLE:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.drop_event)

        self.presets = DEFAULT_PRESETS.copy()
        self.preset_paths = {}
        self.images = []
        self.current_index = 0
        self.base_folder = ""
        self.main_review_folder = ""
        self.last_opened_folder = load_last_folder() or ""
        self.sort_root = SORTED_FOLDER
        self.image_hidden = False
        self.undo_stack = []
        self.zoom_level = 1.0  # 1.0 = Fit to window
        self.min_zoom = 0.25
        self.max_zoom = 4.0
        self.zoom_step = 0.1
        self.image_cache = {}
        self.cache_size = 5

        # UI Elements
        self.preset_frame = Frame(root)
        self.preset_frame.pack(pady=10)

        self.img_label = Label(root, bg='white')
        self.img_label.pack(expand=True)
        self.img_label.bind('<Double-Button-1>', lambda e: self.reset_zoom())

        self.file_label = Label(root, text="", font=("Menlo", 10))
        self.file_label.pack(pady=2)

        self.status_bar = Frame(root)
        self.status_bar.pack(side=BOTTOM, fill=X)
        self.status_left = Label(self.status_bar, text="", font=("Menlo", 10), anchor='w')
        self.status_left.pack(side=LEFT, fill=X, expand=True)
        self.status_right = Label(self.status_bar, text="", font=("Menlo", 10), anchor='e')
        self.status_right.pack(side=RIGHT)

        self.bottom_frame = Frame(root)
        self.bottom_frame.pack(side=BOTTOM, fill=X, pady=10)

        self.select_btn = Button(self.bottom_frame, text="📂 Choose Folder", font=("Menlo", 10), command=self.select_folder)
        self.select_btn.pack(side=LEFT, padx=5)

        self.main_review_btn = Button(self.bottom_frame, text="🔙 Main Review Folder", font=("Menlo", 10), command=self.return_to_main)
        self.main_review_btn.pack(side=LEFT, padx=5)

        self.paste_path_btn = Button(self.bottom_frame, text="📋 Paste Path", font=("Menlo", 10), command=self.enable_manual_path_entry)
        self.paste_path_btn.pack(side=LEFT, padx=5)

        self.reveal_in_finder_btn = Button(self.bottom_frame, text="📂 Reveal Finder", font=("Menlo", 10), command=self.reveal_in_finder)
        self.reveal_in_finder_btn.pack(side=LEFT, padx=5)

        self.save_tsv_btn = Button(self.bottom_frame, text="⭐ Save to TSV", font=("Menlo", 10), command=self.save_current_filename_to_tsv)
        self.save_tsv_btn.pack(side=LEFT, padx=5)

        # Zoom controls
        self.zoom_container = Frame(self.bottom_frame)
        self.zoom_container.pack(side=LEFT, padx=10)
        Label(self.zoom_container, text="Zoom", font=("Menlo", 9)).pack(side=TOP, anchor='w')
        self.zoom_scale = Scale(
            self.zoom_container,
            from_=self.min_zoom,
            to=self.max_zoom,
            resolution=0.05,
            orient=HORIZONTAL,
            showvalue=False,
            length=200,
            command=self.on_zoom_slider
        )
        self.zoom_scale.set(self.zoom_level)
        self.zoom_scale.pack(side=LEFT)

        self.path_label = Label(self.bottom_frame, text="", font=("Menlo", 10), anchor='w')
        self.path_label.pack(side=LEFT, expand=True, fill=X)

        self.quick_preset_frame = Frame(root)
        self.quick_preset_frame.pack(side=BOTTOM, pady=5)
        self.setup_quick_presets()

        # No dialog on startup. Just open the last folder if it exists.
        self.open_last_folder_on_start()

        # Key bindings
        root.bind('w', lambda e: self.next_image())
        root.bind('q', lambda e: self.prev_image())
        root.bind('<Right>', lambda e: self.next_image())
        root.bind('<Left>', lambda e: self.prev_image())
        root.bind('<Down>', lambda e: self.next_image())
        root.bind('<Up>', lambda e: self.prev_image())
        root.bind('j', lambda e: self.next_image())
        root.bind('k', lambda e: self.prev_image())
        root.bind('<Configure>', self.on_resize)
        root.bind('<MouseWheel>', self.on_mousewheel)
        root.bind('<Button-4>', self.on_mousewheel)
        root.bind('<Button-5>', self.on_mousewheel)
        root.bind('0', lambda e: self.reveal_in_finder())
        root.bind('<Return>', lambda e: self.reveal_in_finder())
        root.bind('h', lambda e: self.toggle_image_visibility())
        root.bind('H', lambda e: self.toggle_image_visibility())
        root.bind('<space>', lambda e: self.toggle_image_visibility())
        root.bind('<Escape>', lambda e: root.destroy())
        root.bind('r', lambda e: self.refresh_image())
        root.bind('d', lambda e: self.move_image('2'))
        root.bind('p', lambda e: self.enable_manual_path_entry())
        root.bind('u', lambda e: self.undo_move())
        root.bind('m', lambda e: self.toggle_dark_mode())
        root.bind('i', lambda e: self.show_image_info())
        root.bind('s', lambda e: self.save_current_filename_to_tsv())

        # Zoom shortcuts (avoid preset keys '-')
        root.bind('[', lambda e: self.adjust_zoom(-self.zoom_step))
        root.bind(']', lambda e: self.adjust_zoom(self.zoom_step))
        root.bind('Z', lambda e: self.reset_zoom())

        for key in self.presets:
            root.bind(key, self.make_move_handler(key))

    # --- New helpers: toast + button flash ---
    def show_toast(self, text, duration=1500):
        if hasattr(self, "toast_label") and self.toast_label.winfo_exists():
            self.toast_label.destroy()
        self.toast_label = Label(
            self.root, text=text, font=("Menlo", 10),
            bg="#323232", fg="white", padx=10, pady=6
        )
        self.toast_label.place(relx=0.5, rely=0.08, anchor="n")
        self.root.after(duration, lambda: (
            self.toast_label.destroy() if self.toast_label.winfo_exists() else None
        ))

    def flash_button(self, btn, text="Saved ✓", duration=1200):
        original = btn["text"]
        btn.config(text=text)
        self.root.after(duration, lambda: btn.config(text=original))

    # --- Safe copy helper for Favorites ---
    def _safe_copy_to_dir(self, src_path, dst_dir):
        base = os.path.basename(src_path)
        name, ext = os.path.splitext(base)
        candidate = os.path.join(dst_dir, base)
        i = 1
        while os.path.exists(candidate):
            candidate = os.path.join(dst_dir, f"{name}_{i}{ext}")
            i += 1
        shutil.copy2(src_path, candidate)
        return candidate

    def save_current_filename_to_tsv(self):
        if not self.images:
            messagebox.showinfo("Save to TSV", "No image loaded.")
            return

        filename = self.images[self.current_index]
        image_path = os.path.join(self.base_folder, filename)

        try:
            with open(TSV_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{filename}\n")

            if not hasattr(self, "favorites_path"):
                self.favorites_path = os.path.join(self.sort_root, FAVORITE)
                os.makedirs(self.favorites_path, exist_ok=True)

            copied_path = self._safe_copy_to_dir(image_path, self.favorites_path)

            self.status_right.config(text=f"Saved & copied: {os.path.basename(copied_path)} ⭐")
            self.show_toast(f"Saved to TSV & copied to FAVORITES: {os.path.basename(copied_path)} ⭐")
            self.flash_button(self.save_tsv_btn, text="Saved ✓")

        except Exception as e:
            messagebox.showerror("TSV/Favorites Error", f"Could not complete action: {e}")

    # --- Startup folder handling (no dialog) ---
    def open_last_folder_on_start(self):
        folder = self.last_opened_folder
        if folder and os.path.isdir(folder):
            self.base_folder = folder
            self.main_review_folder = folder
            self.path_label.config(text=f"📂 {folder}")
            self.load_images()
            self.setup_presets()
            self.setup_preset_labels()
            self.current_index = 0
            self.show_image()
        else:
            self.status_left.config(text="No folder loaded. Click “📂 Choose Folder”.")
            self.path_label.config(text="")

    def select_folder(self):
        initial_dir = self.last_opened_folder or SOURCE_FOLDER
        folder = filedialog.askdirectory(initialdir=initial_dir, title="Select Folder with Images")
        if folder:
            self.base_folder = folder
            self.main_review_folder = folder
            self.last_opened_folder = folder
            save_last_folder(folder)
            self.path_label.config(text=f"📂 {folder}")
            self.load_images()
            self.setup_presets()
            self.setup_preset_labels()
            self.current_index = 0
            self.show_image()

    def setup_quick_presets(self):
        for widget in self.quick_preset_frame.winfo_children():
            widget.destroy()
        for key, (label, folder_name) in self.presets.items():
            btn = Button(self.quick_preset_frame, text=label, padx=2, pady=2,
                         font=("Menlo", 9), command=lambda f=folder_name: self.switch_to_preset_folder(f))
            btn.pack(side=LEFT, padx=2)

    def switch_to_preset_folder(self, folder_name):
        folder_path = os.path.join(self.sort_root, folder_name)
        if os.path.exists(folder_path):
            self.base_folder = folder_path
            self.path_label.config(text=f"📂 {self.base_folder}")
            self.load_images()
            self.current_index = 0
            self.show_image()
        else:
            messagebox.showerror("Error", f"Folder {folder_path} does not exist.")

    def return_to_main(self):
        if self.main_review_folder and os.path.exists(self.main_review_folder):
            self.base_folder = self.main_review_folder
            self.path_label.config(text=f"📂 {self.base_folder}")
            self.load_images()
            self.current_index = 0
            self.show_image()
        else:
            messagebox.showerror("Error", "Main review folder not set or doesn't exist.")

    def enable_manual_path_entry(self):
        path_window = Toplevel(self.root)
        path_window.title("Enter Folder Path")

        Label(path_window, text="Paste folder path:", font=("Menlo", 10)).pack(padx=10, pady=5)
        path_entry = Entry(path_window, width=60, font=("Menlo", 10))
        path_entry.pack(padx=10, pady=5)

        def load_from_entry():
            folder = path_entry.get().strip()
            if os.path.isdir(folder):
                self.base_folder = folder
                self.main_review_folder = folder
                self.last_opened_folder = folder
                save_last_folder(folder)
                self.path_label.config(text=f"📂 {folder}")
                self.load_images()
                self.setup_presets()
                self.setup_preset_labels()
                self.current_index = 0
                self.show_image()
                path_window.destroy()
            else:
                messagebox.showerror("Error", "Provided path is not a valid directory.")

        Button(path_window, text="Open", command=load_from_entry, font=("Menlo", 10)).pack(pady=5)

    def drop_event(self, event):
        if not DND_AVAILABLE:
            return
        path = event.data.strip().replace('{', '').replace('}', '')
        if os.path.isdir(path):
            self.base_folder = path
            self.main_review_folder = path
            self.last_opened_folder = path
            save_last_folder(path)
            self.path_label.config(text=f"📂 {path}")
            self.load_images()
            self.setup_presets()
            self.setup_preset_labels()
            self.current_index = 0
            self.show_image()
        else:
            messagebox.showerror("Error", f"{path} is not a valid directory.")

    def load_images(self):
        valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        try:
            self.images = sorted([
                f for f in os.listdir(self.base_folder)
                if not f.startswith('.') and f.lower().endswith(valid_exts)
                and not os.path.isdir(os.path.join(self.base_folder, f))
            ], key=natural_sort_key)
        except Exception as e:
            self.images = []
            self.status_left.config(text=f"Error loading images: {e}")

    def setup_presets(self):
        self.preset_paths = {}
        os.makedirs(self.sort_root, exist_ok=True)
        for _, (_, folder_name) in self.presets.items():
            path = os.path.join(self.sort_root, folder_name)
            os.makedirs(path, exist_ok=True)
            self.preset_paths[folder_name] = path

        self.favorites_path = os.path.join(self.sort_root, FAVORITE)
        os.makedirs(self.favorites_path, exist_ok=True)

    def setup_preset_labels(self):
        for widget in self.preset_frame.winfo_children():
            widget.destroy()
        for key, (label, _) in self.presets.items():
            btn = Button(self.preset_frame, text=f"{label} [{key}]", padx=2, pady=2,
                         width=10, font=("Menlo", 10),
                         command=lambda k=key: self.move_image(k))
            btn.pack(side=LEFT, padx=2)

    def _get_platform(self):
        if sys.platform == 'darwin':
            return 'mac'
        if sys.platform.startswith('win'):
            return 'windows'
        return 'linux'

    def _compute_scaled_image(self, img: Image.Image) -> Image.Image:
        orig_w, orig_h = img.size
        view_w = max(50, self.root.winfo_width() - 50)
        view_h = max(50, self.root.winfo_height() - 200)
        fit_scale = min(view_w / orig_w, view_h / orig_h)
        scale = max(self.min_zoom, min(self.max_zoom, self.zoom_level)) * fit_scale
        target_w = max(1, int(orig_w * scale))
        target_h = max(1, int(orig_h * scale))
        resample = Image.LANCZOS if target_w < orig_w or target_h < orig_h else Image.BICUBIC
        return img.resize((target_w, target_h), resample)

    def show_image(self):
        if not self.images:
            self.status_left.config(text="No images found.")
            self.file_label.config(text="")
            self.img_label.config(image='')
            self.img_label.image = None
            return

        if self.image_hidden:
            self.img_label.config(image='')
            self.img_label.image = None
            self.status_left.config(text=f"{self.current_index + 1} of {len(self.images)} (Hidden)")
            return

        image_path = os.path.join(self.base_folder, self.images[self.current_index])
        try:
            if self.images[self.current_index] in self.image_cache:
                base_img = self.image_cache[self.images[self.current_index]]
            else:
                base_img = Image.open(image_path)
                if len(self.image_cache) >= self.cache_size:
                    self.image_cache.pop(next(iter(self.image_cache)))
                self.image_cache[self.images[self.current_index]] = base_img

            display_img = self._compute_scaled_image(base_img)
            self.tk_img = ImageTk.PhotoImage(display_img)
            self.img_label.config(image=self.tk_img)
            self.img_label.image = self.tk_img
            self.file_label.config(text=self.images[self.current_index])
            self.update_status_bar()
        except Exception as e:
            self.status_left.config(text=f"Error loading image: {str(e)}")

    def update_status_bar(self):
        if not self.images:
            return
        image_path = os.path.join(self.base_folder, self.images[self.current_index])
        try:
            img = self.image_cache.get(self.images[self.current_index]) or Image.open(image_path)
            file_size = os.path.getsize(image_path) / (1024 * 1024)
            dimensions = f"{img.width}×{img.height}"
            self.status_left.config(text=f"{self.current_index + 1} of {len(self.images)} | Alphabetical")
            self.status_right.config(text=f"{dimensions} | {file_size:.1f}MB | Zoom: {self.zoom_level:.2f}x")
        except Exception:
            pass

    def rotate_image(self, degrees):
        if not self.images:
            return
        image_path = os.path.join(self.base_folder, self.images[self.current_index])
        try:
            img = Image.open(image_path)
            img = img.rotate(degrees, expand=True)
            img.save(image_path)
            if self.images[self.current_index] in self.image_cache:
                del self.image_cache[self.images[self.current_index]]
            self.show_image()
            messagebox.showinfo("Rotation", f"Image rotated {degrees}° and saved.")
        except Exception as e:
            messagebox.showerror("Rotation Error", f"Could not rotate image: {e}")

    def on_zoom_slider(self, value):
        try:
            self.zoom_level = float(value)
        except Exception:
            return
        self.show_image()

    def adjust_zoom(self, delta):
        self.zoom_level = max(self.min_zoom, min(self.max_zoom, self.zoom_level + delta))
        self.zoom_scale.set(self.zoom_level)
        self.show_image()

    def reset_zoom(self):
        self.zoom_level = 1.0
        self.zoom_scale.set(self.zoom_level)
        self.show_image()

    def toggle_dark_mode(self):
        bg = "#2d2d2d" if self.root.cget('bg') == 'white' else "white"
        fg = "white" if bg == "#2d2d2d" else "black"
        self.root.config(bg=bg)
        for widget in [self.img_label, self.file_label, self.status_left, self.status_right]:
            widget.config(bg=bg, fg=fg)
        self.show_image()

    def show_image_info(self):
        if not self.images:
            return
        info_window = Toplevel(self.root)
        info_window.title("Image Information")
        image_path = os.path.join(self.base_folder, self.images[self.current_index])
        img = Image.open(image_path)
        info = img.info
        text = f"Filename: {self.images[self.current_index]}\n"
        text += f"Size: {os.path.getsize(image_path) / (1024 * 1024):.2f} MB\n"
        text += f"Dimensions: {img.width} × {img.height}\n"
        text += f"Mode: {img.mode}\n"
        text += "Metadata:\n"
        for k, v in info.items():
            text += f"  {k}: {v}\n"
        scroll = Scrollbar(info_window)
        text_area = Text(info_window, wrap=WORD, yscrollcommand=scroll.set,
                        font=("Menlo", 10), padx=10, pady=10)
        scroll.config(command=text_area.yview)
        text_area.insert(END, text)
        text_area.config(state=DISABLED)
        text_area.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)

    def reveal_in_finder(self):
        if not self.images:
            return
        current_image_path = os.path.join(self.base_folder, self.images[self.current_index])
        platform = self._get_platform()
        try:
            if platform == 'mac':
                subprocess.run(['open', '-R', current_image_path], check=False)
            elif platform == 'windows':
                subprocess.run(['explorer', f'/select,{current_image_path}'], check=False)
            else:
                folder = os.path.dirname(current_image_path)
                subprocess.run(['xdg-open', folder], check=False)
        except Exception as e:
            messagebox.showerror("Reveal Error", f"Could not reveal file: {e}")

    def toggle_image_visibility(self):
        self.image_hidden = not self.image_hidden
        self.show_image()

    def on_mousewheel(self, event):
        if event.num == 5 or getattr(event, "delta", 0) < 0:
            self.next_image()
        elif event.num == 4 or getattr(event, "delta", 0) > 0:
            self.prev_image()

    def move_image(self, key):
        if not self.images:
            return
        filename = self.images[self.current_index]
        src = os.path.join(self.base_folder, filename)
        _, folder_name = self.presets[key]
        dest = os.path.join(self.preset_paths[folder_name], filename)
        try:
            shutil.move(src, dest)
            self.undo_stack.append((dest, src))
            del self.images[self.current_index]
            if self.current_index >= len(self.images):
                self.current_index = len(self.images) - 1
            if self.current_index < 0:
                self.current_index = 0
            self.show_image()
        except Exception as e:
            messagebox.showerror("Move Error", f"Could not move file: {e}")

    def undo_move(self):
        if not self.undo_stack:
            messagebox.showinfo("Undo", "No actions to undo.")
            return
        last_dest, original_src = self.undo_stack.pop()
        if os.path.exists(last_dest):
            try:
                shutil.move(last_dest, original_src)
                self.load_images()
                # Keep selection at restored file if possible
                try:
                    self.current_index = self.images.index(os.path.basename(original_src))
                except ValueError:
                    self.current_index = 0
                self.show_image()
                messagebox.showinfo("Undo", f"Moved back: {os.path.basename(original_src)}")
            except Exception as e:
                messagebox.showerror("Undo Error", f"Failed to undo move: {e}")
        else:
            messagebox.showerror("Undo Error", "File no longer exists in the target location.")

    def make_move_handler(self, key):
        return lambda e: self.move_image(key)

    def next_image(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.show_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def on_resize(self, event):
        self.show_image()

    def refresh_image(self):
        if not self.images:
            return
        if self.images[self.current_index] in self.image_cache:
            del self.image_cache[self.images[self.current_index]]
        self.img_label.config(image='')
        self.img_label.image = None
        self.show_image()


# ---------- Run App ----------
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageSorter(root)
    root.mainloop()

