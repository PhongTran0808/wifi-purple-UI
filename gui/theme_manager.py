import customtkinter as ctk
import json
import os

class ThemeManager:
    """Theme management system"""
    
    def __init__(self):
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "name": "Dark Theme",
                "colors": {
                    "bg_primary": "#0d0d0d",
                    "bg_secondary": "#1a1a1a", 
                    "bg_tertiary": "#2d2d2d",
                    "text_primary": "#ffffff",
                    "text_secondary": "#cccccc",
                    "accent": "#1f6aa5",
                    "accent_hover": "#144e75",
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "error": "#F44336"
                }
            },
            "light": {
                "name": "Light Theme",
                "colors": {
                    "bg_primary": "#ffffff",
                    "bg_secondary": "#f5f5f5",
                    "bg_tertiary": "#e0e0e0", 
                    "text_primary": "#000000",
                    "text_secondary": "#333333",
                    "accent": "#2196F3",
                    "accent_hover": "#1976D2",
                    "success": "#4CAF50",
                    "warning": "#FF9800", 
                    "error": "#F44336"
                }
            },
            "cyberpunk": {
                "name": "Cyberpunk",
                "colors": {
                    "bg_primary": "#0a0a0a",
                    "bg_secondary": "#1a0a1a",
                    "bg_tertiary": "#2a1a2a",
                    "text_primary": "#00ff41",
                    "text_secondary": "#00cc33",
                    "accent": "#ff0080",
                    "accent_hover": "#cc0066",
                    "success": "#00ff41",
                    "warning": "#ffff00",
                    "error": "#ff0040"
                }
            },
            "ocean": {
                "name": "Ocean Blue",
                "colors": {
                    "bg_primary": "#0d1421",
                    "bg_secondary": "#1e2a3a",
                    "bg_tertiary": "#2f4050",
                    "text_primary": "#ffffff",
                    "text_secondary": "#b0c4de",
                    "accent": "#00bcd4",
                    "accent_hover": "#0097a7",
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "error": "#F44336"
                }
            }
        }
        
        self.load_theme_preference()
    
    def load_theme_preference(self):
        """Load saved theme preference"""
        try:
            config_file = 'config.json'
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                self.current_theme = config.get('ui_settings', {}).get('theme', 'dark')
        except Exception as e:
            print(f"Error loading theme preference: {e}")
            self.current_theme = "dark"
    
    def save_theme_preference(self):
        """Save theme preference to config"""
        try:
            config_file = 'config.json'
            config = {}
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
            
            if 'ui_settings' not in config:
                config['ui_settings'] = {}
            
            config['ui_settings']['theme'] = self.current_theme
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
                
        except Exception as e:
            print(f"Error saving theme preference: {e}")
    
    def get_current_theme(self):
        """Get current theme configuration"""
        return self.themes.get(self.current_theme, self.themes["dark"])
    
    def get_color(self, color_name):
        """Get specific color from current theme"""
        theme = self.get_current_theme()
        return theme["colors"].get(color_name, "#ffffff")
    
    def set_theme(self, theme_name):
        """Set new theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_theme_preference()
            self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme to CustomTkinter"""
        theme = self.get_current_theme()
        colors = theme["colors"]
        
        # Set CustomTkinter appearance mode
        if self.current_theme == "light":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        
        # Create custom theme file
        self.create_custom_theme_file(colors)
    
    def create_custom_theme_file(self, colors):
        """Create CustomTkinter theme file"""
        theme_config = {
            "CTk": {
                "fg_color": [colors["bg_primary"], colors["bg_primary"]]
            },
            "CTkToplevel": {
                "fg_color": [colors["bg_primary"], colors["bg_primary"]]
            },
            "CTkFrame": {
                "corner_radius": 15,
                "border_width": 0,
                "fg_color": [colors["bg_secondary"], colors["bg_secondary"]],
                "top_fg_color": [colors["bg_secondary"], colors["bg_secondary"]],
                "border_color": [colors["accent"], colors["accent"]]
            },
            "CTkButton": {
                "corner_radius": 10,
                "border_width": 0,
                "fg_color": [colors["accent"], colors["accent"]],
                "hover_color": [colors["accent_hover"], colors["accent_hover"]],
                "border_color": [colors["accent"], colors["accent"]],
                "text_color": [colors["text_primary"], colors["text_primary"]],
                "text_color_disabled": ["#A3A3A3", "#A3A3A3"]
            },
            "CTkLabel": {
                "corner_radius": 0,
                "fg_color": [colors["bg_primary"], colors["bg_primary"]],
                "text_color": [colors["text_primary"], colors["text_primary"]]
            },
            "CTkEntry": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": [colors["bg_tertiary"], colors["bg_tertiary"]],
                "border_color": [colors["accent"], colors["accent"]],
                "text_color": [colors["text_primary"], colors["text_primary"]],
                "placeholder_text_color": [colors["text_secondary"], colors["text_secondary"]]
            },
            "CTkTextbox": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": [colors["bg_tertiary"], colors["bg_tertiary"]],
                "border_color": [colors["accent"], colors["accent"]],
                "text_color": [colors["text_primary"], colors["text_primary"]],
                "scrollbar_button_color": [colors["text_secondary"], colors["text_secondary"]],
                "scrollbar_button_hover_color": [colors["accent"], colors["accent"]]
            },
            "CTkScrollableFrame": {
                "label_fg_color": [colors["bg_secondary"], colors["bg_secondary"]]
            },
            "CTkCheckBox": {
                "corner_radius": 6,
                "border_width": 3,
                "fg_color": [colors["accent"], colors["accent"]],
                "border_color": [colors["accent"], colors["accent"]],
                "hover_color": [colors["accent_hover"], colors["accent_hover"]],
                "checkmark_color": [colors["text_primary"], colors["text_primary"]],
                "text_color": [colors["text_primary"], colors["text_primary"]],
                "text_color_disabled": [colors["text_secondary"], colors["text_secondary"]]
            },
            "CTkProgressBar": {
                "corner_radius": 1000,
                "border_width": 0,
                "fg_color": [colors["bg_tertiary"], colors["bg_tertiary"]],
                "progress_color": [colors["accent"], colors["accent"]],
                "border_color": [colors["bg_tertiary"], colors["bg_tertiary"]]
            }
        }
        
        # Save theme file
        theme_file = "assets/themes/current_theme.json"
        os.makedirs(os.path.dirname(theme_file), exist_ok=True)
        
        with open(theme_file, 'w') as f:
            json.dump(theme_config, f, indent=4)
        
        # Apply theme
        try:
            ctk.set_default_color_theme(theme_file)
        except Exception as e:
            print(f"Error applying theme: {e}")
    
    def get_available_themes(self):
        """Get list of available themes"""
        return [(name, theme["name"]) for name, theme in self.themes.items()]

class ThemeSelector(ctk.CTkFrame):
    """Theme selection widget"""
    
    def __init__(self, parent, theme_manager, callback=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.callback = callback
        
        # Title
        title = ctk.CTkLabel(self, text="🎨 Theme Selection", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Theme options
        self.theme_var = ctk.StringVar(value=theme_manager.current_theme)
        
        for theme_id, theme_name in theme_manager.get_available_themes():
            radio = ctk.CTkRadioButton(
                self, text=theme_name, variable=self.theme_var,
                value=theme_id, command=self.on_theme_change
            )
            radio.pack(pady=5, anchor="w", padx=20)
        
        # Preview colors
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.pack(pady=10, padx=20, fill="x")
        
        self.update_preview()
    
    def on_theme_change(self):
        """Handle theme change"""
        new_theme = self.theme_var.get()
        self.theme_manager.set_theme(new_theme)
        self.update_preview()
        
        if self.callback:
            self.callback(new_theme)
    
    def update_preview(self):
        """Update theme preview"""
        # Clear preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        theme = self.theme_manager.get_current_theme()
        colors = theme["colors"]
        
        # Preview label
        preview_label = ctk.CTkLabel(
            self.preview_frame, text="Preview:",
            font=("Roboto", 12, "bold")
        )
        preview_label.pack(pady=5)
        
        # Color swatches
        color_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        color_frame.pack(pady=5)
        
        color_names = ["accent", "success", "warning", "error"]
        for i, color_name in enumerate(color_names):
            color_swatch = ctk.CTkFrame(
                color_frame, width=30, height=30,
                fg_color=colors[color_name]
            )
            color_swatch.pack(side="left", padx=2)

# Global theme manager instance
theme_manager = ThemeManager()