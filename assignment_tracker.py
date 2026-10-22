import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment Tracker")
        self.root.geometry("800x500")
        
        self.filename = "assignments.json"
        self.assignments = self.load_assignments()
        
        # --- Input Frame ---
        input_frame = ttk.LabelFrame(root, text="Add New Assignment", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=5)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=3)
        
        ttk.Label(input_frame, text="Subject:").grid(row=0, column=2, sticky="w", padx=5)
        self.subject_entry = ttk.Entry(input_frame, width=20)
        self.subject_entry.grid(row=0, column=3, padx=5, pady=3)
        
        ttk.Label(input_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=5)
        self.due_entry = ttk.Entry(input_frame, width=15)
        self.due_entry.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        
        ttk.Label(input_frame, text="Priority:").grid(row=1, column=2, sticky="w", padx=5)
        self.priority_combo = ttk.Combobox(input_frame, values=["Low", "Medium", "High"], width=10, state="readonly")
        self.priority_combo.set("Medium")
        self.priority_combo.grid(row=1, column=3, padx=5, pady=3, sticky="w")
        
        add_btn = ttk.Button(input_frame, text="Add Assignment", command=self.add_assignment)
        add_btn.grid(row=0, column=4, rowspan=2, padx=15, sticky="ns")
        
        # --- Treeview (List of Assignments) ---
        columns = ("title", "subject", "due", "priority", "status")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        
        self.tree.heading("title", text="Title")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("due", text="Due Date")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("status", text="Status")
        
        self.tree.column("title", width=250)
        self.tree.column("subject", width=120)
        self.tree.column("due", width=120)
        self.tree.column("priority", width=80)
        self.tree.column("status", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # --- Buttons Frame ---
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Mark Complete", command=self.mark_complete).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_assignment).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side="left", padx=5)
        
        # Load existing data
        self.refresh_list()
    
    def load_assignments(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_assignments(self):
        with open(self.filename, "w") as f:
            json.dump(self.assignments, f, indent=2)
    
    def add_assignment(self):
        title = self.title_entry.get().strip()
        subject = self.subject_entry.get().strip()
        due = self.due_entry.get().strip()
        priority = self.priority_combo.get()
        
        if not title or not subject or not due:
            messagebox.showwarning("Missing Info", "Please fill in Title, Subject, and Due Date.")
            return
        
        # Basic date validation
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please use the format YYYY-MM-DD (example: 2026-10-30)")
            return
        
        assignment = {
            "title": title,
            "subject": subject,
            "due": due,
            "priority": priority,
            "status": "Pending"
        }
        
        self.assignments.append(assignment)
        self.save_assignments()
        self.refresh_list()
        
        # Clear inputs
        self.title_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.priority_combo.set("Medium")
    
    def refresh_list(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Sort by due date
        sorted_assignments = sorted(self.assignments, key=lambda x: x["due"])
        
        for a in sorted_assignments:
            self.tree.insert("", "end", values=(
                a["title"],
                a["subject"],
                a["due"],
                a["priority"],
                a["status"]
            ))
    
    def get_selected_index(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Please select an assignment first.")
            return None
        
        item = self.tree.item(selected[0])
        values = item["values"]
        
        # Find the matching assignment in the list
        for i, a in enumerate(self.assignments):
            if (a["title"] == values[0] and 
                a["subject"] == values[1] and 
                a["due"] == values[2]):
                return i
        return None
    
    def mark_complete(self):
        index = self.get_selected_index()
        if index is not None:
            self.assignments[index]["status"] = "Completed"
            self.save_assignments()
            self.refresh_list()
    
    def delete_assignment(self):
        index = self.get_selected_index()
        if index is not None:
            if messagebox.askyesno("Confirm", "Delete this assignment?"):
                del self.assignments[index]
                self.save_assignments()
                self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentTracker(root)
    root.mainloop()
