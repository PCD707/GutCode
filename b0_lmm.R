# This script is designed to automate the process of running linear mixed models (LMMs) on a given dataset.
# It begins by redirecting the R output to a text file, ensuring the installation and loading of necessary packages.
# Then, it loads the data, reformats certain columns as factors, and specifies paths for saving plots.
# The script defines a function to run a series of models for each dependent variable and another function for creating plots.
# Finally, it executes the models for each dependent variable and closes the output redirection.

# Redirect output to a text file for logging
sink("C:/Users/Darren/Desktop/CODE/FASTDM/b0_lmm_output.txt")

# Check and install necessary packages, then load them
required_packages <- c("lme4", "lmerTest", "emmeans", "performance")
new_packages <- required_packages[!required_packages %in% installed.packages()[,"Package"]]
if(length(new_packages)) install.packages(new_packages)
lapply(required_packages, require, character.only = TRUE)

# Load dataset
b0_sham.data <- read.csv("C:/Users/Darren/Desktop/CODE/FASTDM/b0_sham-lmm.csv")

# Convert certain columns to factors to enable proper analysis in LMM
b0_sham.data$subject <- as.factor(b0_sham.data$subject)
b0_sham.data$session <- as.factor(b0_sham.data$session)
b0_sham.data$cohort <- as.factor(b0_sham.data$cohort)

# Define paths for saving the generated plots
plot_paths <- list(
  null_model = "C:/Users/Darren/Desktop/CODE/FASTDM/Graphs/RStudio/b0-lmm/nullmodel",
  group_model = "C:/Users/Darren/Desktop/CODE/FASTDM/Graphs/RStudio/b0-lmm/groupmodel",
  session_model = "C:/Users/Darren/Desktop/CODE/FASTDM/Graphs/RStudio/b0-lmm/sessionmodel",
  simple_model = "C:/Users/Darren/Desktop/CODE/FASTDM/Graphs/RStudio/b0-lmm/simplemodel/",
  itx_model = "C:/Users/Darren/Desktop/CODE/FASTDM/Graphs/RStudio/b0-lmm/interactionmodel",
  cohort_model = "C:/Users/Darren/Desktop/CODE/FASTDM/Graphs/RStudio/b0-lmm/cohortmodel/",
  full_model = "C:/Users/Darren/Desktop/CODE/FASTDM/Graphs/RStudio/b0-lmm/fullmodel/"
)

# Define the dependent variables and their descriptive names
dependent_vars <- c("a", "v", "t0", "st0")
var_names <- c("Boundary Separation", "Drift Rate", "Non-Decision Time", "ITV of Non-Decision Time")

# Function to run LMM models for a given variable and output results
run_model <- function(var, var_name, data, plot_path) {
  # Define various model formulas for comparison
  model_formulas <- list(
    null_model = as.formula(paste(var, "~ 1 + (1 | subject)")),
    group_model = as.formula(paste(var, "~ group + (1 | subject)")),
    session_model = as.formula(paste(var, "~ session + (1 | subject)")),
    simple_model = as.formula(paste(var, "~ session + group + (1 | subject)")),
    cohort_model = as.formula(paste(var, "~ cohort + (1 | subject)")),
    full_model = as.formula(paste(var, "~ session + group + session * group + (1 | subject)"))
  )
  
  # Execute models and store their results
  models <- lapply(model_formulas, function(formula) lmer(formula, data = data, REML = FALSE))
  model_names <- names(models)
  
  # Perform and store comprehensive likelihood ratio tests between models
  anova_results <- list()
  for (i in 1:(length(models) - 1)) {
    for (j in (i + 1):length(models)) {
      model1 <- model_names[i]
      model2 <- model_names[j]
      comparison_name <- paste(model1, "vs", model2)
      anova_results[[comparison_name]] <- anova(models[[model1]], models[[model2]])
    }
  }
  
  # Output summaries, emmeans, and plots for each model
  lapply(names(models), function(model_name) {
    model <- models[[model_name]]
    print(paste("MODEL:", model_name, "-", var_name, "-", var))
    print(summary(model))
    print(anova(model))
    
    # Determine variables present in the model for emmeans calculation
    model_vars <- all.vars(formula(model))
    has_session <- "session" %in% model_vars
    has_group <- "group" %in% model_vars
    has_cohort <- "cohort" %in% model_vars
    
    # Adjust emmeans call based on the variables present in the model
    if (has_session || has_group || has_cohort) {
      specs <- if (has_session && has_group) ~ session * group
      else if (has_session) ~ session
      else if (has_group) ~ group
      else ~ cohort
      emm <- emmeans(model, specs = specs)
      pairwise_comparisons <- pairs(emm)  
      print(pairwise_comparisons)
    }
    
    #
    # Generate and save plots for each model
    create_plots(model, var, plot_path[[model_name]], model_vars)
  })
  
  # Print ANOVA results for likelihood ratio tests
  print(paste("Likelihood Ratio Tests for", var_name, "-", var))
  lapply(names(anova_results), function(name) {
    print(name)
    print(anova_results[[name]])
  })
}

# Function to create and save plots for a given model
create_plots <- function(model, var, path, model_vars) {
  plot_types <- c("qq", "hist", "scatter", "box")  # Types of plots to create
  
  for (plot_type in plot_types) {
    file_name <- paste0(path, "/", var, "_", plot_type, ".png")  # Construct filename for the plot
    png(file_name, 600, 400)  # Open a PNG device for plotting
    
    # Set the plot parameters for APA (American Psychological Association) style
    par(mar = c(5, 4, 1, 2) + 0.1, bty = "l")  # Set margins and box type for plots
    
    if (plot_type == "qq") {
      # Create a QQ plot of the residuals
      qqnorm(residuals(model), main = "", xlab = paste("Theoretical Quantiles (", var, ")", sep = ""), ylab = paste("Sample Quantiles (", var, ")", sep = ""))
      qqline(residuals(model))  # Add a QQ line
    } else if (plot_type == "hist") {
      # Create a histogram of the residuals
      hist(residuals(model), main = "", xlab = paste("Residuals (", var, ")", sep = ""))
    } else if (plot_type == "scatter") {
      # Create a scatter plot of fitted values vs residuals
      plot(fitted(model), residuals(model), main = "", xlab = paste("Fitted values (", var, ")", sep = ""), ylab = paste("Residual values (", var, ")", sep = ""))
      abline(h = 0, lty = 2, col = "red")  # Add a horizontal line at 0
    } else { # boxplot
      # Create a boxplot if there are intersecting variables
      intersecting_vars <- intersect(model_vars, c("session", "group", "cohort"))
      if (length(intersecting_vars) > 0) {
        formula <- as.formula(paste(var, "~", paste(intersecting_vars, collapse = " + ")))
        boxplot(formula, data = model.frame(model), main = "")
      } else {
        # Create an empty plot if there are no intersecting variables
        plot(1, type = "n", axes = FALSE, xlab = "", ylab = "", main = "") 
      }
    }
    
    dev.off()  # Close the PNG device
  }
}

# Run models and generate outputs
for (i in seq_along(dependent_vars)) {
  run_model(dependent_vars[i], var_names[i], b0_sham.data, plot_paths)
}

sink()  # Divert R output to a file or back to the console