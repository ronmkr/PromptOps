import curses
import curses.textpad
import os
import sys
import re
# Try importing promptops_core
try:
    import promptops_core
except ImportError:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.join(BASE_DIR, "scripts"))
    import promptops_core
class PromptOpsTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.prompts = promptops_core.get_prompts()
        # Build Categories
        all_tags = set()
        for p in self.prompts:
            all_tags.update(p['tags'])
        self.categories = ["All"] + sorted(list(all_tags))
        self.filtered_prompts = self.prompts
        # State
        self.active_pane = "categories" # 'categories', 'prompts', 'input'
        self.cat_row = 0
        self.prompt_row = 0
        self.search_term = ""
        # Final result
        self.final_hydrated_prompt = None
        # Setup colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Selected row
        curses.init_pair(2, curses.COLOR_CYAN, -1)                  # Header
        curses.init_pair(3, curses.COLOR_YELLOW, -1)                # Tags
        curses.init_pair(4, curses.COLOR_GREEN, -1)                 # Instructions
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)               # Active Pane border
    def safe_addstr(self, window, y, x, text, attr=0):
        """Safely print to the screen, truncating to prevent wrapping/crashing."""
        try:
            height, width = window.getmaxyx()
            if y >= height or y < 0 or x >= width or x < 0:
                return
            max_len = width - x - 1
            if max_len <= 0:
                return
            safe_text = text[:max_len]
            window.addstr(y, x, safe_text, attr)
        except curses.error:
            pass
    def update_prompts_for_category(self):
        cat = self.categories[self.cat_row]
        if cat == "All":
            self.filtered_prompts = self.prompts
        else:
            self.filtered_prompts = [p for p in self.prompts if cat in p['tags']]
        self.prompt_row = 0
    def draw(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        if height < 15 or width < 60:
            self.safe_addstr(self.stdscr, 0, 0, "Terminal too small. Please resize.")
            self.stdscr.refresh()
            return
        # Pane Layout (Widths)
        cat_width = max(15, int(width * 0.2))
        prompt_width = max(25, int(width * 0.3))
        preview_width = width - cat_width - prompt_width - 2
        # Draw Header
        header = f" 📚 PromptOps | Prompts: {len(self.filtered_prompts)} "
        self.safe_addstr(self.stdscr, 0, 0, header.ljust(width), curses.color_pair(2) | curses.A_BOLD)
        # Draw Categories Pane (Left)
        max_rows = height - 3
        start_cat = max(0, self.cat_row - (max_rows // 2))
        end_cat = min(len(self.categories), start_cat + max_rows)
        for i, idx in enumerate(range(start_cat, end_cat)):
            y = i + 2
            name = self.categories[idx]
            display_str = f" {name}".ljust(cat_width - 1)
            attr = 0
            if idx == self.cat_row:
                display_str = f"> {name}".ljust(cat_width - 1)
                if self.active_pane == "categories":
                    attr = curses.color_pair(1)
                else:
                    attr = curses.A_BOLD | curses.A_UNDERLINE
            self.safe_addstr(self.stdscr, y, 0, display_str, attr)
        # Vertical separator 1
        for y in range(1, height - 1):
            color = curses.color_pair(5) if self.active_pane == "categories" else 0
            self.safe_addstr(self.stdscr, y, cat_width, "│", color)
        # Draw Prompts Pane (Middle)
        if self.filtered_prompts:
            self.prompt_row = max(0, min(self.prompt_row, len(self.filtered_prompts) - 1))
            start_p = max(0, self.prompt_row - (max_rows // 2))
            end_p = min(len(self.filtered_prompts), start_p + max_rows)
            for i, idx in enumerate(range(start_p, end_p)):
                y = i + 2
                name = self.filtered_prompts[idx]['name']
                if len(name) > prompt_width - 3:
                    name = name[:prompt_width-6] + "..."
                display_str = f" {name}".ljust(prompt_width - 1)
                attr = 0
                if idx == self.prompt_row:
                    display_str = f"> {name}".ljust(prompt_width - 1)
                    if self.active_pane == "prompts":
                        attr = curses.color_pair(1)
                    else:
                        attr = curses.A_BOLD | curses.A_UNDERLINE
                self.safe_addstr(self.stdscr, y, cat_width + 1, display_str, attr)
        # Vertical separator 2
        for y in range(1, height - 1):
            color = curses.color_pair(5) if self.active_pane == "prompts" else 0
            self.safe_addstr(self.stdscr, y, cat_width + prompt_width + 1, "│", color)
        # Draw Preview Pane (Right)
        if self.filtered_prompts:
            p = self.filtered_prompts[self.prompt_row]
            base_x = cat_width + prompt_width + 3
            self.safe_addstr(self.stdscr, 2, base_x, p['name'], curses.A_BOLD | curses.color_pair(2))
            self.safe_addstr(self.stdscr, 4, base_x, p['description'])
            tags_str = ", ".join(p['tags'])
            self.safe_addstr(self.stdscr, 6, base_x, f"Tags: {tags_str}", curses.color_pair(3))
            self.safe_addstr(self.stdscr, 8, base_x, "--- Template ---")
            preview_lines = p['prompt'].split('\n')
            for i, line in enumerate(preview_lines):
                y_pos = 10 + i
                if y_pos >= height - 2:
                    break
                safe_line = line.replace('\t', '    ')
                self.safe_addstr(self.stdscr, y_pos, base_x, safe_line)
        # Draw Footer
        footer = " [↑/↓] Navigate | [←/→] Change Pane | [Enter] Use Prompt | [Q]uit "
        self.safe_addstr(self.stdscr, height - 1, 0, footer.ljust(width), curses.color_pair(4))
        self.stdscr.refresh()
    def run_input_modal(self, prompt_name):
        """Creates a textbox overlay to collect variable input"""
        try:
            prompt_template, variables = promptops_core.use_prompt(prompt_name, return_only=True)
        except Exception as e:
            self.safe_addstr(self.stdscr, 0, 0, f"Error loading prompt: {e}")
            self.stdscr.refresh()
            curses.napms(2000)
            return False
        if not variables:
            # No variables, just return the template
            self.final_hydrated_prompt = prompt_template
            return True
        height, width = self.stdscr.getmaxyx()
        for target_var in variables:
            # Create a centered window
            win_h = max(10, height - 6)
            win_w = max(40, width - 20)
            start_y = (height - win_h) // 2
            start_x = (width - win_w) // 2
            win = curses.newwin(win_h, win_w, start_y, start_x)
            win.box()
            # Title
            title = f" ✨ Inject Variable: {{{{{target_var}}}}} "
            self.safe_addstr(win, 0, 2, title, curses.color_pair(3) | curses.A_BOLD)
            instructions = " Paste/type your code here. Press Ctrl+G when finished. "
            self.safe_addstr(win, win_h - 1, 2, instructions, curses.color_pair(4))
            win.refresh()
            # Create the textpad inside the box
            text_win = curses.newwin(win_h - 2, win_w - 2, start_y + 1, start_x + 1)
            # Show cursor for typing
            curses.curs_set(1)
            box = curses.textpad.Textbox(text_win, insert_mode=True)
            # Let the user type/paste. Emacs-like keybindings apply (Ctrl+G to save)
            result = box.edit()
            curses.curs_set(0) # Hide cursor again
            # Clean up result
            result = result.strip()
            # Hydrate
            prompt_template = prompt_template.replace(f"{{{{{target_var}}}}}", result)
            # Re-draw the background before next variable
            self.draw()
        self.final_hydrated_prompt = prompt_template
        return True
    def run(self):
        curses.curs_set(0) # Hide cursor
        self.stdscr.nodelay(False)
        while True:
            self.draw()

            try:
                char = self.stdscr.getch()
            except curses.error:
                continue

            if char in (ord('q'), ord('Q')):

                return
            elif char in (curses.KEY_RIGHT, ord('l')):
                if self.active_pane == "categories" and self.filtered_prompts:
                    self.active_pane = "prompts"
            elif char in (curses.KEY_LEFT, ord('h')):
                if self.active_pane == "prompts":
                    self.active_pane = "categories"
            elif char in (curses.KEY_UP, ord('k')):
                if self.active_pane == "categories":
                    self.cat_row = max(0, self.cat_row - 1)
                    self.update_prompts_for_category()
                elif self.active_pane == "prompts":
                    self.prompt_row = max(0, self.prompt_row - 1)
            elif char in (curses.KEY_DOWN, ord('j')):
                if self.active_pane == "categories":
                    self.cat_row = min(len(self.categories) - 1, self.cat_row + 1)
                    self.update_prompts_for_category()
                elif self.active_pane == "prompts":
                    self.prompt_row = min(len(self.filtered_prompts) - 1, self.prompt_row + 1)
            elif char in (10, 13, curses.KEY_ENTER):
                if self.active_pane == "categories" and self.filtered_prompts:
                    self.active_pane = "prompts"
                elif self.active_pane == "prompts":
                    # Trigger Modal
                    p = self.filtered_prompts[self.prompt_row]
                    success = self.run_input_modal(p['prompt'])
                    if success:
                        return # Exit TUI to print
def main():
    try:
        tui = curses.wrapper(PromptOpsTUI)
        # curses.wrapper passes stdscr to the class, but we need to instantiate it differently
    except Exception as e:
        pass
def run_tui():
    try:
        def gui(stdscr):
            app = PromptOpsTUI(stdscr)
            app.run()
            return app.final_hydrated_prompt

        result = curses.wrapper(gui)

        if result:
            print(result)

        return True
    except curses.error:
        # Ignore silent curses tear-down errors like nocbreak
        return False
    except KeyboardInterrupt:
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    run_tui()

