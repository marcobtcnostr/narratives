import sys
import tkinter as tk
from tkinter import scrolledtext
import threading
import logging
import os
from PIL import Image, ImageTk

class TextRedirector:
    """A class to redirect stdout or stderr to a tkinter Text widget."""
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass


class ServerGUI:
    def __init__(self, root, run_server):
        self.root = root
        self.root.title("Narratives Server Control Panel")
        self.server_thread = None
        self.is_running = False
        self.run_server = run_server

        # Define color palette based on the provided dark theme
        self.colors = {
            "logo_color": "#69b3a2",
            "logo_color_hover": "#56a085",
            "bg_color": "#474747",
            "text_color": "#f6f8fa",
            "text_color_hover": "#474747",
            "button_bg_color": "white",
            "button_bg_color_hover": "#dae0e5",
            "button_text_color": "#474747",
            "button_text_color_hover": "#474747",
            "navbar_bg_color": "#333",
            "navbar_bg_color_hover": "#f6f8fa",
            "navbar_text_color_hover": "#474747",
            "modal_bg_color": "#333",
            "event_card_bg_color": "#333",
            "separator_line_color": "#dae0e5",
            "event_card_connector_color": "#dae0e5",
        }

        # Set the window icon using Pillow
        self.set_window_icon()

        # Set the background color of the window
        self.root.configure(bg=self.colors['bg_color'])

        # Center the buttons and console output using a frame
        main_frame = tk.Frame(root, bg=self.colors['bg_color'])
        main_frame.pack(expand=True)

        # Create buttons with modern style
        self.start_button = tk.Button(main_frame, text="Start Server", command=self.start_server,
                                      bg=self.colors['button_bg_color'], fg=self.colors['button_text_color'],
                                      activebackground=self.colors['button_bg_color_hover'],
                                      activeforeground=self.colors['button_text_color_hover'],
                                      relief=tk.FLAT, font=("Arial", 14, "bold"), padx=20, pady=10)
        self.start_button.grid(row=0, column=0, padx=10, pady=20)

        self.stop_button = tk.Button(main_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED,
                                     bg=self.colors['button_bg_color'], fg=self.colors['button_text_color'],
                                     activebackground=self.colors['button_bg_color_hover'],
                                     activeforeground=self.colors['button_text_color_hover'],
                                     relief=tk.FLAT, font=("Arial", 14, "bold"), padx=20, pady=10)
        self.stop_button.grid(row=0, column=1, padx=10, pady=20)

        # Bind hover events to buttons
        self.start_button.bind("<Enter>", lambda e: self.on_hover(self.start_button, 'button_bg_color_hover', 'button_text_color_hover'))
        self.start_button.bind("<Leave>", lambda e: self.on_leave(self.start_button, 'button_bg_color', 'button_text_color'))

        self.stop_button.bind("<Enter>", lambda e: self.on_hover(self.stop_button, 'button_bg_color_hover', 'button_text_color_hover'))
        self.stop_button.bind("<Leave>", lambda e: self.on_leave(self.stop_button, 'button_bg_color', 'button_text_color'))

        # Console Output (Wider and taller)
        self.log_output = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=40, width=150, 
                                                    bg=self.colors['navbar_bg_color'], 
                                                    fg=self.colors['text_color'], 
                                                    insertbackground=self.colors['text_color'])  # Make text cursor visible
        self.log_output.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # Redirect stdout and stderr to the text widget
        sys.stdout = TextRedirector(self.log_output)
        sys.stderr = TextRedirector(self.log_output)

        # Capture Flask logging
        logger = logging.getLogger('werkzeug')
        handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(handler)

    def set_window_icon(self):
        """Sets the custom window icon using Pillow's ImageTk."""
        try:
            # Construct the correct relative path from the current file location to the image
            image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'N_Server_Broadway.ico')
            
            # Load the image using Pillow
            original_image = Image.open(image_path)

            # Resize the image to a larger size (e.g., 64x64)
            resized_image = original_image.resize((64, 64), Image.Resampling.LANCZOS)

            # Convert the resized image to ImageTk format
            logo_image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to prevent garbage collection
            self.root.logo_image = logo_image

            # Set the icon for the window
            self.root.iconphoto(True, logo_image)
        except Exception as e:
            print(f"Error loading icon: {e}")


    def log_message(self, message):
        self.log_output.insert(tk.END, f"{message}\n")
        self.log_output.see(tk.END)

    def start_server(self):
        if not self.is_running:
            self.is_running = True
            self.log_message("Starting the server...")
            self.server_thread = threading.Thread(target=self.run_server, daemon=True)
            self.server_thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log_message("Server started successfully.")

    def stop_server(self):
        if self.is_running:
            self.is_running = False
            self.log_message("Stopping the server...")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.log_message("Server stopped.")

    def on_hover(self, widget, bg_color_key, fg_color_key):
        """Handle button hover event."""
        widget.config(bg=self.colors[bg_color_key], fg=self.colors[fg_color_key])

    def on_leave(self, widget, bg_color_key, fg_color_key):
        """Handle button leave event."""
        widget.config(bg=self.colors[bg_color_key], fg=self.colors[fg_color_key])



