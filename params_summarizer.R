# This script is designed to automate the process of parsing and summarizing data from multiple text files. 
# It sets a working directory, defines functions for parsing individual data files and for processing 
# a collection of files to create a summary. The script is particularly useful for data extraction and 
# aggregation tasks where data is stored across multiple text files.

# Set working directory
# Make sure to set the correct working directory!
setwd(r"(C:\Users\Darren\Desktop\CODE\FASTDM\datasets_GSCsplit\probiotics\session 2)")

# Function to parse data from a single file
parse_data_from_file <- function(file) {
  lines <- readLines(file)  # Read all lines from the file
  # Extract parameter values using regular expressions
  a <- as.numeric(sub(".*=\\s*(\\d+.\\d+)", "\\1", grep("a =", lines, value = TRUE)[1]))
  v <- as.numeric(sub(".*=\\s*(\\d+.\\d+)", "\\1", grep("v =", lines, value = TRUE)[1]))
  t0 <- as.numeric(sub(".*=\\s*(\\d+.\\d+)", "\\1", grep("t0 =", lines, value = TRUE)[1]))
  st0 <- as.numeric(sub(".*=\\s*(\\d+.\\d+)", "\\1", grep("st0 =", lines, value = TRUE)[1]))
  # Return a data frame with the extracted parameters
  return(data.frame(a = a, v = v, t0 = t0, st0 = st0))
}

# Function to process files from a selected folder and create summary file
process_files_and_create_summary <- function() {
  # Use a folder selection dialog to get the folder path
  folder_path <- choose.dir(default = getwd(), caption = "Select Folder Containing Parameters Files")
  # Get a list of all text files in the selected folder
  file_list <- list.files(path = folder_path, pattern = "\\.txt$", full.names = TRUE)
  
  # Initialize a data frame to store combined data
  summary_data <- data.frame(subject = character(), a = numeric(), v = numeric(), t0 = numeric(), st0 = numeric(), stringsAsFactors = FALSE)
  
  # Loop through each file, parse data, and add it to the summary data frame
  for (file in file_list) {
    params <- parse_data_from_file(file)  # Parse data from each file
    # Extract subject name from file name
    subject_name <- gsub("parameters_", "", basename(file))
    subject_name <- gsub("\\.txt$", "", subject_name)
    # Combine parsed data with subject name and add to summary data frame
    summary_data <- rbind(summary_data, cbind(data.frame(subject = subject_name), params))
  }
  
  # Write summary data to a .txt file in tab-separated format
  write.table(summary_data, file = "summary.txt", row.names = FALSE, sep = "\t", quote = FALSE)
}

# Run the function to process files and create a summary
process_files_and_create_summary()
