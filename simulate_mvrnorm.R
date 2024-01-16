# This script is designed for running a series of simulations based on a set of parameters.
# It first sets the working directory, loads necessary parameter data, and calculates a covariance matrix.
# Then, it defines a function to run individual simulations and combines their results.
# Finally, it executes the simulations for each row of parameter data.

library(parallel)  # For parallel computing capabilities
library(data.table)  # Data manipulation and access to large datasets
library(MASS)  # Contains functions and datasets to support Venables and Ripley's "Modern Applied Statistics with S" (4th edition, 2002).

# Set working directory to the specified path
setwd(r"(C:\Users\Darren\Desktop\CODE\FASTDM\models\simulated models\sim_b0)")

# Load parameter data from a text file
params_data <- fread("params_for_simulation.txt")

# Function to calculate covariance matrix of the parameters
calculate_cov_matrix <- function(params_data) {
  # Calculate covariance matrix using complete observations
  cov_matrix <- cov(params_data[, .(a, v, t0, st0)], use = "complete.obs")
  
  # Check if the matrix is positive definite; if not, stop the script
  if (any(eigen(cov_matrix)$values <= 0)) {
    stop("cov_matrix is not positive definite")
  }
  return(cov_matrix)
}

# Calculate the covariance matrix using the loaded parameter data
cov_matrix <- calculate_cov_matrix(params_data)

# Function to run a simulation based on given parameters and covariance matrix
run_simulation <- function(group, session, condition, subject, a, v, t0, st0, row_number, cov_matrix) {
  mean_params <- c(a, v, t0, st0)  # Set mean parameters for the simulation
  
  # Generate simulation parameters using multivariate normal distribution
  sim_params <- mvrnorm(1, mean_params, cov_matrix)
  # Ensure parameters are non-negative and adhere to specific constraints
  params <- list(a = max(sim_params[1], 0), v = max(sim_params[2], 0), t = max(sim_params[3], 3 * sim_params[4]), T = max(sim_params[4], 0))
  
  # Construct the command to run the simulation with generated parameters
  base_filename <- sprintf("%s_%s_%s_%s_sim_%d", group, session, condition, subject, row_number)
  cmd <- sprintf("construct-samples.exe -a %f -z %f -v %f -t %f -d %f -Z %f -V %f -T %f -r -n 250 -N 1000 -p 4 -o %s_%%d.dat",
                 params$a, 0.5, params$v, params$t, 0, 0, 0, params$T, base_filename)
  
  # Run the simulation and handle any errors
  if (system(cmd) != 0) {
    message(sprintf("Error running simulation command for row %d", row_number))
    return(NULL)
  }
  
  # Combine the output data files from the simulation into a single dataset
  combined_data <- NULL
  for (file_idx in 0:999) {  # Loop over expected output files
    file_name <- sprintf("%s_%d.dat", base_filename, file_idx)
    if (file.exists(file_name)) {
      sim_data <- read.table(file_name, header = FALSE)
      unlink(file_name)  # Delete the file after reading
      combined_data <- rbind(combined_data, sim_data)
    }
  }
  
  # Write the combined simulation data to a file
  combined_output_filename <- sprintf("%s_%s_%s_%s_sim.dat", group, session, condition, subject)
  if (!is.null(combined_data)) {
    write.table(combined_data, combined_output_filename, col.names = FALSE, row.names = FALSE, quote = FALSE)
  }
  
  return(combined_data)
}

# Main loop to run simulations for each row in the parameter data
simulation_results <- list()
for (i in seq_len(nrow(params_data))) {
  row <- params_data[i, ]
  simulation_results[[i]] <- run_simulation(row$group, row$session, row$condition, row$subject, row$a, row$v, row$t0, row$st0, i, cov_matrix)
}
