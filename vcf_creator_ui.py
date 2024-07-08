import tkinter as tk
from tkinter import filedialog, messagebox

def launch_vcf_creator_ui():
    root = tk.Tk()
    root.title("VCF Creator Configuration")

    configurations = []

    def add_configuration():
        ref_genome = ref_genome_entry.get()
        bam_file = bam_file_entry.get()
        output_vcf = output_vcf_entry.get()
        
        if not all([ref_genome, bam_file, output_vcf]):
            messagebox.showerror("Error", "Please fill all fields before adding a configuration.")
            return
        
        configurations.append({
            "ref_genome": ref_genome,
            "bam_file": bam_file,
            "output_vcf": output_vcf
        })
        
        listbox.insert(tk.END, f"BAM: {bam_file}, VCF: {output_vcf}")
        ref_genome_entry.delete(0, tk.END)
        bam_file_entry.delete(0, tk.END)
        output_vcf_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Configuration added successfully.")

    def generate_script():
        script_path = "create_vcf_all.sh"
        with open(script_path, "w") as script_file:
            script_file.write("#!/bin/bash\n\n")
            script_file.write("conda activate genomics\n\n")
            for config in configurations:
                script_file.write(f"samtools faidx {config['ref_genome']}\n")
                script_file.write(f"samtools index {config['bam_file']}\n")
                script_file.write(f"bcftools mpileup -Ou -f {config['ref_genome']} {config['bam_file']} | bcftools call -mv -Ob -o {config['output_vcf']}.bcf\n")
                script_file.write(f"bcftools index {config['output_vcf']}.bcf\n")
                script_file.write(f"bcftools view -Oz -o {config['output_vcf']}.vcf.gz {config['output_vcf']}.bcf\n")
                script_file.write(f"tabix -p vcf {config['output_vcf']}.vcf.gz\n\n")
            script_file.write("echo \"Variant calling and file processing completed.\"\n")
        messagebox.showinfo("Done", f"All configurations have been written to {script_path}. Please run the script manually.")

    tk.Label(root, text="Select the genome reference file (.mmi):").pack()
    ref_genome_entry = tk.Entry(root, width=50)
    ref_genome_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=lambda: ref_genome_entry.insert(0, filedialog.askopenfilename(filetypes=[("FASTA files", "*.mmi")]))).pack()

    tk.Label(root, text="Select the BAM file:").pack()
    bam_file_entry = tk.Entry(root, width=50)
    bam_file_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=lambda: bam_file_entry.insert(0, filedialog.askopenfilename(filetypes=[("BAM files", "*.bam")]))).pack()

    tk.Label(root, text="Specify the output VCF file name (without extension):").pack()
    output_vcf_entry = tk.Entry(root, width=50)
    output_vcf_entry.pack(padx=20, pady=5)

    tk.Button(root, text="Add Configuration", command=add_configuration).pack(pady=10)

    listbox = tk.Listbox(root, height=6, width=50)
    listbox.pack(pady=10)

    tk.Button(root, text="Generate Script", command=generate_script).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    launch_vcf_creator_ui()
