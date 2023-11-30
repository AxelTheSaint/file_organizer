# Automated File Organizer in Python with GUI
Automatic Files Organizer.
An automated file organizer categorizes files by their extensions and groups them by type. The software scans and moves files from a user-specified source path to a user-defined destination path (it doesn't copy the files; it moves them). Using the file extension, it determines the file type and organizes it alongside other files of the same type within the specified destination path.

# Problem
Review the backups conducted over the years, spanning from the past to the present, in order to declutter both external and internal hard drives as well as NAS. Establish an organized system for easy archiving of the accumulated contents in the future. This involves managing numerous disorganized folders, subfolders, and files of varying sizes. Additionally, considering the extensive duration of these backups, there may be numerous duplicate files, obsolete files generated by software that are still accessible, and intricate nested structures that pose challenges in navigation. Plus, manually reviewing and organizing all your backups takes too much time and effort.

# Solution
I require software that allows me to specify a source path and a destination path. The software should meticulously analyze all folders, subfolders, and files within the source path. It will then examine their extensions and cross-reference them with a pre-configured dictionary of extensions. The software will organize and transfer the files to the designated destination path, grouping them by type based on their extensions. Consequently, after the scanning process, the source path will be nearly empty, while the destination path will be structured into subfolders corresponding to file types, each containing all files of a specific type (e.g., images, videos, word documents, presentations, PDFs, etc.). I also want to monitor all the operations carried out by the software, therefore, I need to specify a log file path. The software will automatically generate a log file containing comprehensive information each time it executes a scan.

# Specifications and Requirements

GUI Requirements:
1. An input field where you can enter the path of the source folder to analyze.
2. An input field where you can enter the path of the destination folder of the files.
3. An input field where you can enter the path of the log file.
4. Each input field should open the Explorer tree where you can select the desired path.
5. A button "Start Scanning" to start the process.
6. Some statistics.
7. A button "Open Log File" to open the log file just created.
[For the GUI i use "tkinter"]

"SOURCE" process specifications:
1. When the user clicks "Start Scan", the software first checks whether all input fields are filled.
2. In that case, it switches to scanning the specified folder in the source path, including all subfolders and files.
3. For each file it checks the extension and compares it with the "extensions" dictionary in file_extensions.py.
4. The dictionary has "key:value" like this "extension:type", so based on the extension it applies a type to the scanned file.
5. Based on the assigned type it moves to the respective destination path.

"DESTINATION" process specifications:
1. When the software will move the file to the destination, it first checks whether the directory for the assigned type exists.
2. If not, it creates it.
3. The software checks if the file already exists.
4. If yes, rename it by adding a timestamp.

BEFORE MOVING process specifications:
Since this is a moving process and not a copying process, it is necessary to do some checks
1. Check if source and destination paths are correct and reachable.
2. Check if there is enough space in the destination path.

LOG process specifications:
In the log file i want to keep tracking every step the process does
1. execution_time_var -> the time the process taking (end_time - start_time)
2. error_count_var -> total error count during the process
3. files_examined_var -> total number of examined files
4. subfolders_examined_var -> total number of examined subfolders
5. source_size_var -> total amount of source size (GB)
6. subfolders_size_var (USELESS)
7. files_size_var -> total amount of files source size (GB)
8. folder_path ->  checking if existing folder
9. "[+] Making {folder_name} folder" -> keep trace of creating folder
10. "[+] {folder_name} folder already exists" -> keep trace of existing folder
11. path -> keep trace of source path from input field
12. main_path -> keep trace of destination path from input field
13. log_file-> keep trace of log file path from input field
14. start_time.strftime('%Y-%m-%d %H:%M:%S')}") -> keep trace of the time the process starts
15. end_time.strftime('%Y-%m-%d %H:%M:%S') -> keep trace of the time the process ends
16. total_files_moved -> total amount of moved files
17. total_files_renamed -> total amount of renamed files
18. total_files_remaining -> total amount of file remained in the source path

# How to use it

Requirements:
[Python installed ( up to 3.x)]
[tkinter installed (for the GUI)]

To start the program:
1. save both file in a single folder
2. execute the prompt in the folder
3. digit: "python file_organizer.py"




