#!/usr/bin/env python3
"""
Test script để kiểm tra GUI có chạy được không
"""

import sys
import os

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import customtkinter as ctk
    print("✓ CustomTkinter imported successfully")
    
    from PIL import Image, ImageTk
    print("✓ Pillow imported successfully")
    
    # Test theme loading
    theme_path = os.path.join("assets", "themes", "dark-theme.json")
    if os.path.exists(theme_path):
        print("✓ Theme file exists")
        ctk.set_default_color_theme(theme_path)
        print("✓ Theme loaded successfully")
    else:
        print("⚠ Theme file not found, using default")
        ctk.set_default_color_theme("blue")
    
    ctk.set_appearance_mode("dark")
    
    # Test basic window creation
    root = ctk.CTk()
    root.title("Test Window")
    root.geometry("400x300")
    
    # Test frame creation (this was causing the error)
    frame = ctk.CTkFrame(root, fg_color="transparent")
    frame.pack(fill="both", expand=True)
    
    label = ctk.CTkLabel(frame, text="Test thành công!", font=("Arial", 16))
    label.pack(pady=50)
    
    button = ctk.CTkButton(frame, text="Đóng", command=root.quit)
    button.pack(pady=20)
    
    print("✓ GUI components created successfully")
    print("✓ Tất cả test đều PASS! GUI sẽ hiển thị trong 3 giây...")
    
    # Hiển thị window trong 3 giây rồi tự động đóng
    root.after(3000, root.quit)
    root.mainloop()
    
    print("✓ Test hoàn thành thành công!")
    
except Exception as e:
    print(f"✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()