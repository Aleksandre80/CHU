import tkinter as tk
from tkinter import filedialog, messagebox

def launch_config_ui():
    root = tk.Tk()
    root.title("Batch Configuration for Genomic Processing")

    configurations = []

    def add_configuration():
        base_output_dir = base_output_dir_entry.get()
        input_dir = input_dir_entry.get()
        ref_genome = ref_genome_entry.get()
        qs_scores = qs_score_entry.get()
        cuda_device = cuda_device_entry.get()
        kit_name = kit_name_entry.get()
        
        if not all([base_output_dir, input_dir, ref_genome, qs_scores, cuda_device, kit_name]):
            messagebox.showerror("Error", "Please fill all fields before adding a configuration.")
            return
        
        configurations.append({
            "base_output_dir": base_output_dir,
            "input_dir": input_dir,
            "ref_genome": ref_genome,
            "qs_scores": qs_scores,
            "cuda_device": cuda_device,
            "kit_name": kit_name
        })
        
        listbox.insert(tk.END, f"Input Dir: {input_dir}, Output Dir: {base_output_dir}, Q-Scores: {qs_scores}")
        base_output_dir_entry.delete(0, tk.END)
        input_dir_entry.delete(0, tk.END)
        ref_genome_entry.delete(0, tk.END)
        qs_score_entry.delete(0, tk.END)
        cuda_device_entry.delete(0, tk.END)
        kit_name_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Configuration added successfully.")

    def generate_and_run_script():
        script_path = "all_configurations_processing.sh"
        with open(script_path, "w") as script_file:
            script_file.write("#!/bin/bash\n\n")
            script_file.write("source ~/miniconda3/etc/profile.d/conda.sh\n")
            script_file.write("conda activate genomics\n\n")
            for config in configurations:
                qs_scores_list = config['qs_scores'].split()
                qs_scores_array = ' '.join(f"{qs}" for qs in qs_scores_list)
                script_file.write(f"BASE_OUTPUT_DIR=\"{config['base_output_dir']}\"\n")
                script_file.write("mkdir -p \"${BASE_OUTPUT_DIR}\"\n")
                for qscore in qs_scores_list:
                    output_dir = f"${{BASE_OUTPUT_DIR}}/demultiplexed_q{qscore}"
                    script_file.write(f"""
DORADO_BIN="/home/grid/dorado-0.7.2-linux-x64/bin/dorado"
MODEL_PATH="/home/grid/dorado-0.7.2-linux-x64/bin/dna_r10.4.1_e8.2_400bps_hac@v5.0.0"
REF_GENOME="{config['ref_genome']}"
INPUT_DIR="{config['input_dir']}/"
OUTPUT_DIR="{output_dir}"
mkdir -p "${{OUTPUT_DIR}}"
${{DORADO_BIN}} basecaller -x "{config['cuda_device']}" --min-qscore "{qscore}" --no-trim --emit-fastq ${{MODEL_PATH}} ${{INPUT_DIR}} | \\
${{DORADO_BIN}} demux --kit-name "{config['kit_name']}" --emit-fastq --output-dir "${{OUTPUT_DIR}}"
echo "Processing complete for {config['input_dir']} with Q-score {qscore}"
""")
        messagebox.showinfo("Done", f"All configurations have been written to {script_path}. Please run the script manually.")

    # GUI layout settings
    tk.Label(root, text="Set the base output directory BASE_OUTPUT_DIR:").pack()
    base_output_dir_entry = tk.Entry(root, width=50)
    base_output_dir_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=lambda: base_output_dir_entry.insert(0, filedialog.askdirectory())).pack()

    tk.Label(root, text="Select the folder for INPUT_DIR:").pack()
    input_dir_entry = tk.Entry(root, width=50)
    input_dir_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=lambda: input_dir_entry.insert(0, filedialog.askdirectory())).pack()

    tk.Label(root, text="Select the genome file REF_GENOME (.mmi):").pack()
    ref_genome_entry = tk.Entry(root, width=50)
    ref_genome_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=lambda: ref_genome_entry.insert(0, filedialog.askopenfilename(filetypes=[("FASTA files", "*.mmi")]))).pack()

    tk.Label(root, text="Enter Q-scores separated by spaces:").pack()
    qs_score_entry = tk.Entry(root, width=50)
    qs_score_entry.pack(padx=20, pady=5)

    tk.Label(root, text="Specify the CUDA device (e.g., cuda:0):").pack()
    cuda_device_entry = tk.Entry(root, width=50)
    cuda_device_entry.insert(0, "cuda:0")
    cuda_device_entry.pack(padx=20, pady=5)

    tk.Label(root, text="Enter the kit name (e.g., SQK-NBD114-24):").pack()
    kit_name_entry = tk.Entry(root, width=50)
    kit_name_entry.insert(0, "SQK-NBD114-24")
    kit_name_entry.pack(padx=20, pady=5)

    tk.Button(root, text="Add Configuration", command=add_configuration).pack(pady=10)

    listbox = tk.Listbox(root, height=6, width=50)
    listbox.pack(pady=10)

    tk.Button(root, text="Generate Script", command=generate_and_run_script).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    launch_config_ui()
