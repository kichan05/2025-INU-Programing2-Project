import tkinter as tk
from .typography import Typography


class AIResultPage(tk.Frame):
    def __init__(self, parent, controller: 'ReactionGameApp'):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = tk.Canvas(self, width=controller.w, height=controller.h, highlightthickness=0, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # --- Widgets ---
        cx, h = controller.cx, controller.h

        # Title
        self.canvas.create_text(cx, 80, text="AI 분석 리포트", font=Typography.FONT_TITLE, fill="black")

        # Back Button
        back_btn = self.canvas.create_text(120, 80, text="< STATS", font=Typography.FONT_HOVER, fill="black")
        self.canvas.tag_bind(back_btn, "<Button-1>", lambda e: self.controller.show_frame("StatsPage"))

        # Frame for the scrollable text result
        result_frame = tk.Frame(self, bg="#F0F0F0")
        self.result_text = tk.Text(result_frame, wrap="word", height=20, width=100,
                                   font=Typography.FONT_NORMAL, bg="#F0F0F0",
                                   bd=0, highlightthickness=0, relief="flat", padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.result_text.pack(side="left", fill="both", expand=True)
        
        self.canvas.create_window(cx, h * 0.5, window=result_frame)

    def on_show(self):
        """Called when the page is raised to the top."""
        # Get the analysis content from the controller and display it
        content = self.controller.ai_analysis_content
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, content)
        self.result_text.config(state="disabled")
