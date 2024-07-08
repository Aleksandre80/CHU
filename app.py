import tkinter as tk
from tkinter import ttk  # Pour les widgets stylisés

# Simulons les fonctions des autres modules
def launch_config_ui():
    print("Basecalling and Configuration UI")

def launch_bam_merger_ui():
    print("BAM Merger UI")

def launch_vcf_creator_ui():
    print("VCF Creator UI")

def open_basecalling():
    launch_config_ui()

def open_bam():
    launch_bam_merger_ui()

def open_vcf_creator():
    launch_vcf_creator_ui()
    print("Open VCF")

def open_full_pipeline():
    print("Full pipeline functionality here")

root = tk.Tk()
root.title("Genomic Processing Main Menu")
root.geometry("400x300")  # Définit la taille de la fenêtre

# Style
style = ttk.Style()
style.configure("TButton", font=('Helvetica', 12), padding=10)
style.configure("TLabel", font=('Helvetica', 14, 'bold'), padding=10)

# Frame pour les boutons
button_frame = ttk.Frame(root, padding="10 10 10 10")
button_frame.pack(fill=tk.BOTH, expand=True)

# Ajout des boutons
ttk.Label(button_frame, text="Choose a Task:", style="TLabel").pack()
ttk.Button(button_frame, text="Open Basecalling and Configuration", command=open_basecalling).pack(fill=tk.X, expand=True, pady=5)
ttk.Button(button_frame, text="Merge BAM Files", command=open_bam).pack(fill=tk.X, expand=True, pady=5)
ttk.Button(button_frame, text="Create VCF Files", command=open_vcf_creator).pack(fill=tk.X, expand=True, pady=5)
ttk.Button(button_frame, text="Run Full Pipeline", command=open_full_pipeline).pack(fill=tk.X, expand=True, pady=5)

root.mainloop()
