import tkinter as tk
from tkinter import filedialog, messagebox

def launch_bam_merger_ui():
    root = tk.Tk()
    root.title("BAM Merger Configuration")

    configurations = []

    def add_configuration():
        input_dir = input_dir_entry.get()
        output_dir = output_dir_entry.get()
        
        if not all([input_dir, output_dir]):
            messagebox.showerror("Error", "Please specify both input and output directories.")
            return
        
        configurations.append({
            "input_dir": input_dir,
            "output_dir": output_dir
        })
        
        listbox.insert(tk.END, f"Input: {input_dir}, Output: {output_dir}")
        input_dir_entry.delete(0, tk.END)
        output_dir_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Configuration added successfully.")

    def generate_script():
        script_path = "merge_all_bam.sh"
        with open(script_path, "w") as script_file:
            script_file.write("#!/bin/bash\n\n")
            for config in configurations:
                script_file.write(f"mkdir -p \"{config['output_dir']}\"\n")
                script_file.write(f"samtools merge \"{config['output_dir']}/merged.bam\" \"{config['input_dir']}\"/*.bam\n")
                script_file.write(f"echo \"Merging complete for BAM files in {config['input_dir']}\"\n\n")
        messagebox.showinfo("Done", f"All configurations have been written to {script_path}.")

    tk.Label(root, text="Select the input folder containing BAM files:").pack()
    input_dir_entry = tk.Entry(root, width=50)
    input_dir_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=lambda: input_dir_entry.insert(0, filedialog.askdirectory())).pack()

    tk.Label(root, text="Select the output folder for merged BAM file:").pack()
    output_dir_entry = tk.Entry(root, width=50)
    output_dir_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=lambda: output_dir_entry.insert(0, filedialog.askdirectory())).pack()

    tk.Button(root, text="Add Configuration", command=add_configuration).pack(pady=10)

    listbox = tk.Listbox(root, height=6, width=50)
    listbox.pack(pady=10)

    tk.Button(root, text="Generate Script", command=generate_script).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    launch_bam_merger_ui()
