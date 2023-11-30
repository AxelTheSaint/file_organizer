import os
import shutil
import glob
import logging
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle  # Import the ThemedStyle class
from file_extension import extensions


class FileOrganizer:

    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("450x700")  # Increase the window size

        # Apply a themed style
        style = ThemedStyle(self.root)
        style.set_theme("plastik")

        self.source_path = tk.StringVar()
        self.destination_path = tk.StringVar()
        self.log_path = tk.StringVar()

        # Add new variables to store information
        self.execution_time_var = tk.StringVar()
        self.error_count_var = tk.StringVar()
        self.files_examined_var = tk.StringVar()
        self.subfolders_examined_var = tk.StringVar()
        self.source_size_var = tk.StringVar()
        self.subfolders_size_var = tk.StringVar()
        self.files_size_var = tk.StringVar()

        # Add this line to create the progress_var attribute
        self.progress_var = tk.DoubleVar()

        # Add a new variable to store the log file name
        self.log_file_name = ""

        # Add a new variable to store the log link label
        self.log_link_label = None

        self.create_widgets()

    def create_widgets(self):
        # Source path
        source_label = tk.Label(self.root, text="Source Path:", font=("Arial", 12))
        source_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")

        source_entry = tk.Entry(self.root, textvariable=self.source_path, state="readonly", font=("Arial", 12))
        source_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        source_button = tk.Button(self.root, text="Select", command=self.select_source_path)
        source_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")

        # Destination path
        dest_label = tk.Label(self.root, text="Destination Path:", font=("Arial", 12))
        dest_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="w")

        dest_entry = tk.Entry(self.root, textvariable=self.destination_path, state="readonly", font=("Arial", 12))
        dest_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        dest_button = tk.Button(self.root, text="Select", command=self.select_destination_path)
        dest_button.grid(row=1, column=2, padx=(0, 10), pady=10, sticky="e")

        # Log path
        # log_label = tk.Label(self.root, text="Log File Path:", font=("Arial", 12))
        # log_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="w")

        # log_entry = tk.Entry(self.root, textvariable=self.log_path, state="readonly", font=("Arial", 12))
        # log_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # log_button = tk.Button(self.root, text="Select", command=self.select_log_path)
        # log_button.grid(row=2, column=2, padx=(0, 10), pady=10, sticky="e")

        # Log path
        log_label = tk.Label(self.root, text="Log File Path:", font=("Arial", 12))
        log_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="w")

        log_entry = tk.Entry(self.root, textvariable=self.log_path, state="readonly", font=("Arial", 12))
        log_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        log_button = tk.Button(self.root, text="Select", command=self.select_log_path)
        log_button.grid(row=2, column=2, padx=(0, 10), pady=10, sticky="e")

        # Log file link
        self.log_link_label = tk.Label(
            self.root,
            text="Open Log File",
            font=("Arial", 12),
            fg="blue",
            cursor="hand2",
        )
        self.log_link_label.grid(row=13, column=0, columnspan=3, pady=10, sticky="nsew")
        self.log_link_label.bind("<Button-1>", self.open_log_file)

        # Start button
        start_button = tk.Button(self.root, text="Start Scanning", command=self.start_scanning, font=("Arial", 12))
        start_button.grid(row=3, column=0, columnspan=3, pady=20, sticky="nsew")  # Center the button
        #self.root.grid_rowconfigure(3, weight=1)  # Allow row to expand vertically
        self.root.grid_columnconfigure(0, weight=1)  # Allow column to expand horizontally

        # Add this line to create the progress_var attribute
        self.progress_var = tk.DoubleVar()

        # Progress bar
        #progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")


        labels = [
            ("Execution Time:", self.execution_time_var, 5),
            ("Errors:", self.error_count_var, 6),
            ("Files Examined:", self.files_examined_var, 7),
            ("Subfolders Examined:", self.subfolders_examined_var, 8),
            ("Source Total (GB):", self.source_size_var, 9),
            ("Source Subfolders (GB):", self.subfolders_size_var, 10),
            ("Source Files (GB):", self.files_size_var, 11),
        ]

        for label_text, label_var, row in labels:
            label = tk.Label(self.root, text=label_text, font=("Arial", 12))
            label.grid(row=row, column=0, padx=(10, 0), pady=10, sticky="w")

            value_label = tk.Label(self.root, textvariable=label_var, font=("Arial", 12))
            value_label.grid(row=row, column=1, padx=10, pady=10, sticky="ew")  

    # def select_log_path(self):
    #    log_path = filedialog.askdirectory()
    #    if log_path:
    #        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    #        log_file_name = f"log_file_{timestamp}.txt"
    #        log_file_path = os.path.join(log_path, log_file_name)
    #        self.log_path.set(log_file_path)
    #        self.log_file_path.set(log_file_path)  # Update log_file_path variable

    def select_log_path(self):
        log_path = filedialog.askdirectory()
        if log_path:
            # Automatically generate a unique log file name based on the current date and time
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file_name = f"log_file_{timestamp}.txt"
            log_file_path = os.path.join(log_path, log_file_name)
            self.log_path.set(log_file_path)
            self.log_file_name = log_file_name  # Store the log file name for future reference

    def update_progress_bar(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()
        self.root.update()

    def create_destination_folders(self, main_path):
        for folder_name in set(extensions.values()):
            # create the folder if it does not exist before
            folder_path = os.path.join(main_path, folder_name)
            logging.info(f"Checking folder: {folder_path}")
            if not os.path.isdir(folder_path):
                logging.info(f"[+] Making {folder_name} folder")
                os.mkdir(folder_path)
            else:
                logging.info(f"[+] {folder_name} folder already exists")

    def select_source_path(self):
        self.source_path.set(filedialog.askdirectory())

    def select_destination_path(self):
        self.destination_path.set(filedialog.askdirectory())

    # def select_log_path(self):
    #    #self.log_path.set(filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")]))
    #    log_path = filedialog.askdirectory()
    #    if log_path:
    #        # Automatically generate the log file name based on current date and time
    #        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    #        log_file_name = f"log_file_{timestamp}.txt"
    #        log_file_path = os.path.join(log_path, log_file_name)
    #        self.log_path.set(log_file_path)
    
    def select_log_path(self):
        log_path = filedialog.askdirectory()
        if log_path:
            # Automatically generate the log file name based on the current date and time
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file_name = f"log_file_{timestamp}.txt"
            log_file_path = os.path.join(log_path, log_file_name)
            self.log_path.set(log_file_path)
            self.log_file_name = log_file_name  # Store the log file name for future reference
    
    # def open_log_file(self, event):
    #    log_file_path = os.path.join(self.log_path.get(), self.log_file_name)
    #    if os.path.exists(log_file_path):
    #        os.startfile(log_file_path)  # Open the log file using the default associated application
    #    else:
    #        messagebox.showerror("Error", "Log file not found.")

    def open_log_file(self, event):
        log_file_path = self.log_path.get()  # Remove self.log_file_name from here
        if os.path.exists(log_file_path):
            os.startfile(log_file_path)
        else:
            messagebox.showerror("Error", "Log file not found.")

    def start_scanning(self):
        start_time = datetime.now()
        path = self.source_path.get()
        main_path = self.destination_path.get()
        log_file = self.log_path.get()

        if not path or not main_path or not log_file:
            messagebox.showerror("Error", "Please select source path, destination path, and log file path.")
            return

        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

        # Continue with the rest of your scanning code (similar to the previous examples)
        error_count, renamed_files_count = self.scan_files(path, main_path)

        end_time = datetime.now()
        execution_time = end_time - start_time
        self.execution_time_var.set(str(execution_time))

        self.error_count_var.set(str(error_count))

         # Recalculate and display source statistics in GUI after scanning is complete
        files_count, subfolders_count, total_size = self.calculate_source_statistics(path)

        self.files_examined_var.set(str(files_count))
        self.subfolders_examined_var.set(str(subfolders_count))
        self.source_size_var.set(f"{total_size:.2f} GB")

        # Calculate and display source, subfolders, and files sizes in GB
        source_size = self.get_folder_size(path)
        subfolders_size = self.get_subfolders_size(path)
        files_size = self.get_files_size(path)

        self.subfolders_size_var.set(f"{subfolders_size:.2f} GB")
        self.files_size_var.set(f"{files_size:.2f} GB")

        # Additional information for the log file
        total_files_moved = files_count - int(self.files_examined_var.get())
        total_files_renamed = renamed_files_count
        total_files_remaining = int(self.files_examined_var.get()) - total_files_moved - total_files_renamed
        #logging.info(f"Total Files Moved to Destination: {total_files_moved}")


        logging.info("Scan Summary:")
        logging.info(f"Source Path: {path}")
        logging.info(f"Destination Path: {main_path}")
        logging.info(f"Log file path: {log_file}")
        logging.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"Total Execution Time: {execution_time}")
        logging.info(f"Total Files Examined: {self.files_examined_var.get()}")
        logging.info(f"Total Files Moved to Destination: {total_files_moved}")
        logging.info(f"Total Files Renamed: {total_files_renamed}")
        logging.info(f"Total Files Remaining in Source: {total_files_remaining}")

        
        # total_files_moved = files_count - int(self.files_examined_var.get())
        # total_files_renamed = renamed_files_count
        # total_files_remaining = int(self.files_examined_var.get()) - total_files_moved - total_files_renamed

        # Update log file name in the GUI
        # Update log file name in the GUI
        # log_file_path = os.path.join(self.log_path.get(), self.log_file_name)
        # self.log_file_name = os.path.basename(log_file_path)
        # log_file_path = os.path.join(self.log_path.get(), f"log_file_{timestamp}.txt")  # Update with your log file naming convention
        log_file_path = os.path.join(self.log_path.get(), self.log_file_name)
        self.log_file_name = os.path.basename(log_file_path)
        self.log_link_label.config(state="normal")  # Enable the link label
        self.log_link_label.bind("<Button-1>", self.open_log_file)  # Rebind the callback with the updated log_file_path
        self.log_link_label.config(text="Open Log File")  # Reset the text
        #self.root.update_idletasks()

        messagebox.showinfo("Scan Complete", f"Scan Complete - {error_count} Errors")

    def scan_files(self, path, main_path):
        # Initialize subfolders_scanned to zero
        subfolders_scanned = 0
        files_scanned = 0
        error_count = 0  # Track the number of errors
        renamed_files_count = 0  # Track the number of files that are renamed


        for folder_name in set(extensions.values()):
            # create the folder if it does not exist before
            folder_path = os.path.join(main_path, folder_name)
            if not os.path.isdir(folder_path):
                logging.info(f"[+] Making {folder_name} folder")
                os.mkdir(folder_path)

        self.files_scanned = 0
        self.subfolders_scanned = 0
        
        max_files = 1  # Default value to handle the case where there are no files initially

        for root, dirs, files in os.walk(path):
            subfolders_scanned += 1
            if files:
                # Calculate the maximum number of files if there are files
                max_files = len(files)  # Update max_files calculation
            for file in files:
                files_scanned += 1
                # get the file extension
                _, extension = os.path.splitext(file)
                extension = extension[1:].lower()  # remove the dot from the extension and convert to lower case

                # check if the extension is in the extensions dictionary
                if extension in extensions:
                    src = os.path.join(root, file)
                    dst_folder_name = extensions[extension]
                    dst = os.path.join(main_path, dst_folder_name, file)

                    logging.info(f"Scanned file: {file}")
                    logging.info(f"Source path: {src}")
                    logging.info(f"Checking file extension: {extension}")
                    logging.info(f"Making directory extension: {dst_folder_name}")

                    try:
                        # Check if source and destination paths are correct and reachable
                        if not os.path.exists(src):
                            raise FileNotFoundError(f"Source file not found: {src}")

                        if not os.path.exists(os.path.join(main_path, dst_folder_name)):
                            raise FileNotFoundError(f"Destination folder not found: {os.path.join(main_path, dst_folder_name)}")

                        # Check if there is enough space in the destination path
                        destination_drive = os.path.splitdrive(main_path)[0]
                        if shutil.disk_usage(destination_drive).free < os.path.getsize(src):
                            raise OSError(f"Not enough space in the destination path: {main_path}")
                        
                        # Check if there are files with the same name in the destination
                        while os.path.exists(dst):
                            # Rename the source file by adding the time to the name
                            renamed_files_count += 1  # Increment renamed files count
                            timestamp = datetime.now().strftime('%H-%M-%S-%f')
                            _, file_extension = os.path.splitext(file)
                            file = f"{os.path.splitext(file)[0]}_{timestamp}{file_extension}"
                            dst = os.path.join(main_path, dst_folder_name, file)
                            logging.info(f"File with the same name already exists. Renaming file to: {file}")

                        # Move the file to the destination
                        shutil.move(src, dst)
                        logging.info(f"Moving file to: {dst}")
                        logging.info(f"Destination path: {os.path.join(main_path, dst_folder_name)}")
                        logging.info(f"Date and time of operation: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                    except Exception as e:
                        # Log the error and continue with the next file
                        logging.error(f"Error processing file: {file}. Error: {e}")
                        error_count += 1  # Increment error count
                        continue

                # Update progress bar after processing each file
                progress_percentage = (files_scanned / max_files) * 100
                self.update_progress_bar(progress_percentage)

                # Allow the GUI to update by adding a small delay
                # self.root.update_idletasks()
                # self.root.update()


            # Update the StringVar variables directly after the loop
            self.files_examined_var.set(str(files_scanned))
            self.subfolders_examined_var.set(str(subfolders_scanned))


        logging.info(f"Control - Total files scanned: {files_scanned}")
        logging.info(f"Control - Total subfolders scanned: {subfolders_scanned}")

        # Display scan completion message in Windows
        # if error_count > 0:
        #    messagebox.showinfo("Scan Complete", f"Scan Complete - {error_count} Errors")
        # else:
        #    messagebox.showinfo("Scan Complete", "Scan Complete - All good - 0 Errors")

        # Display scan completion messagge in GUI
        # self.error_count_var.set(str(error_count))
        #self.subfolders_examined_var.set(str(subfolders_scanned))
        
        return error_count, renamed_files_count  # Return the error count and renamed files count
    
    def get_folder_size(self, folder):
        total_size = sum(os.path.getsize(os.path.join(root, file)) for root, dirs, files in os.walk(folder) for file in files)
        return total_size / (1024 ** 3)  # Convert to GB
    
    def get_subfolders_size(self, folder):
        total_size = sum(os.path.getsize(os.path.join(root, dir)) for root, dirs, files in os.walk(folder) for dir in dirs)
        return total_size / (1024 ** 3)  # Convert to GB

    def get_files_size(self, folder):
        total_size = sum(os.path.getsize(os.path.join(root, file)) for root, dirs, files in os.walk(folder) for file in files)
        return total_size / (1024 ** 3)  # Convert to GB
    
    def calculate_source_statistics(self, path):
        files_count = 0
        subfolders_count = 0
        total_size = 0

        for root, dirs, files in os.walk(path):
            subfolders_count += len(dirs)
            files_count += len(files)
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)

        return files_count, subfolders_count, total_size / (1024 ** 3)  # Convert to GB

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizer(root)
    root.mainloop()
