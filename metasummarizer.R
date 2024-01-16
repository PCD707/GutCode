# This R script is designed for aggregating data from multiple text files into a single file. 
# It sets the working directory, loads the necessary library, and defines a function to process 
# and combine data files. The script is useful in situations where data is fragmented across 
# multiple files and needs to be consolidated for analysis or simulation purposes.

# Set working directory
setwd(r"(C:\Users\Darren\Desktop\CODE\FASTDM\datasets_GSCsplit\basic_st0_params)")

# Load necessary library
# Check if 'data.table' is installed, install if not, and then load it
if (!require("data.table")) install.packages("data.table")
library(data.table)

# Function to process files from a selected folder and combine them
process_files_and_combine <- function() {
  # Use a folder selection dialog to get the folder path
  folder_path <- choose.dir(default = getwd(), caption = "Select Folder Containing Summary Files")
  # Get a list of all files ending with '_summary.txt' in the selected folder
  file_list <- list.files(path = folder_path, pattern = "_summary\\.txt$", full.names = TRUE)
  
  # Initialize an empty list to store data frames from each file
  list_data <- list()
  
  # Loop through each file and process
  for (file in file_list) {
    # Read data from the file using 'fread' for fast data loading
    file_data <- fread(file, header = TRUE, sep = "\t")
    
    # Extract metadata (group, session, condition) from the file name
    file_name <- basename(file)
    metadata <- unlist(strsplit(gsub("_summary\\.txt$", "", file_name), "_"))
    group <- metadata[1]
    session <- metadata[2]
    condition <- metadata[3]
    
    # Add metadata columns to the beginning of the data frame
    file_data <- cbind(group = group, session = session, condition = condition, file_data)
    
    # Add the processed data frame to the list
    list_data[[length(list_data) + 1]] <- file_data
  }
  
  # Combine all data frames in the list into one data frame
  combined_data <- rbindlist(list_data)
  
  # Write the combined data to a new file, 'params_for_simulation.txt'
  write.table(combined_data, file = "params_for_simulation.txt", row.names = FALSE, sep = "\t", quote = FALSE)
}

# Run the function to process and combine files
process_files_and_combine()
