# This script is designed to check for issues of multicollinearity in LMM. 
# It involves installing and loading necessary packages, loading and preparing data, defining dependent variables, 
# and running a series of mixed models and then checking the assumption of multicollinearity.

# Ensure necessary packages are installed and loaded
required_packages <- c("lme4", "lmerTest", "emmeans", "performance")
new_packages <- required_packages[!required_packages %in% installed.packages()[,"Package"]]
if(length(new_packages)) install.packages(new_packages)  # Install packages that are not already installed
lapply(required_packages, require, character.only = TRUE)  # Load the necessary packages

# Load your data
data <- read.csv("C:/Users/Darren/Desktop/CODE/FASTDM/b0_sham-lmm.csv")  # Load data from a specified path

# Recategorize relevant data as factors
data$subject <- as.factor(data$subject)  
data$session <- as.factor(data$session)  
data$cohort <- as.factor(data$cohort)  

# Define dependent variables and their names
dependent_vars <- c("a", "v", "t0", "st0")  # List of dependent variables
var_names <- c("Boundary Separation", "Drift Rate", "Non-Decision Time", "ITV of Non-Decision Time")  # Corresponding names for the variables

# Function to run models for a given variable
run_model <- function(var, var_name, data, plot_path) {
  # Define various model formulas for the analysis
  model_formulas <- list(
    null_model = as.formula(paste(var, "~ (1 | subject)")),
    group_model = as.formula(paste(var, "~ group + (1 | subject)")),
    session_model = as.formula(paste(var, "~ session + (1 | subject)")),
    simple_model = as.formula(paste(var, "~ session + group + (1 | subject)")),
    itx_model = as.formula(paste(var, "~ session * group + (1 | subject)")),
    cohort_model = as.formula(paste(var, "~ cohort + (1 | subject)")),
    full_model = as.formula(paste(var, "~ session + group + session * group + (1 | subject)"))
  )
  
  # Running each model and checking for multicollinearity issues
  models <- lapply(model_formulas, function(formula) lmer(formula, data = data, REML = FALSE))  # Fit each model
  model_names <- names(model_formulas)  # Get names of each model
  for (i in seq_along(models)) {
    print(paste("Checking multicollinearity for Variable:", var_name, "in Model:", model_names[i]))
    print(check_collinearity(models[[i]]))  # Check and print collinearity diagnostics
  }
}

# Running the function for each dependent variable
lapply(dependent_vars, function(var) run_model(var, var_names[which(dependent_vars == var)], data, plot_path = NULL))  # Apply the function to each variable
