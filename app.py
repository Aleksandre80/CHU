import tkinter as tk
from basecalling import launch_config_ui
from merge import launch_bam_merger_ui

def open_basecalling():
    launch_config_ui()

def open_bam():
    launch_bam_merger_ui()

def open_vcf_creator():
    print("VCF creation functionality here")

def open_full_pipeline():
    print("Full pipeline functionality here")

root = tk.Tk()
root.title("Genomic Processing Main Menu")

tk.Button(root, text="Open Basecalling and Configuration", command=open_basecalling).pack(pady=10)
tk.Button(root, text="Merge BAM Files", command=open_bam).pack(pady=10)
tk.Button(root, text="Create VCF Files", command=open_vcf_creator).pack(pady=10)
tk.Button(root, text="Run Full Pipeline", command=open_full_pipeline).pack(pady=10)

root.mainloop()
