
#Used to create spagetthi plot of random effect of null model (lmm) of b0 (ddm)

# Ensure necessary packages are installed and loaded
required_packages <- c("lme4", "ggplot2")
new_packages <- required_packages[!required_packages %in% installed.packages()[,"Package"]]
if(length(new_packages)) install.packages(new_packages)
lapply(required_packages, require, character.only = TRUE)

# Load your data
b0_sham.data <- read.csv("C:/Users/Darren/Desktop/CODE/FASTDM/b0_sham-lmm.csv")
b0_sham.data$subject <- as.factor(b0_sham.data$subject)
b0_sham.data$session <- as.factor(b0_sham.data$session)

# Fit the null model for st0 only
null_model_st0 <- lmer(st0 ~ 1 + (1 | subject), data = b0_sham.data, REML = FALSE)

# Extract intercept value from the null model
intercept_value <- fixef(null_model_st0)[1]

# Create spaghetti plot with actual st0 values and APA style, with adjusted x-axis limits
ggplot(b0_sham.data, aes(x = session, y = st0, group = subject, color = subject)) +
  geom_line() +
  geom_hline(yintercept = intercept_value, linetype = "dashed", color = "blue") +
  labs(title = " ", x = "Session", y = "Inter-trial Variability of Non-Decision Time (st0)") +
  theme_minimal() +
  theme(
    legend.position = "none",
    panel.grid = element_blank(),
    panel.background = element_rect(fill = "white", colour = NA),
    plot.background = element_rect(fill = "white", colour = NA),
    axis.line = element_line(),
    axis.ticks = element_line(),
    axis.text.x = element_text(color = "black"),
    axis.text.y = element_text(color = "black"),
    panel.border = element_blank(),
    axis.line.x = element_line(color = "black"),
    axis.line.y = element_line(color = "black"),
    plot.margin = margin(5.5, 5.5, 5.5, 5.5)
  ) +
  scale_x_discrete(expand = c(0.15, 0.15)) # Adjust the expand argument to reduce space



# You can save the plot using ggsave()
# ggsave("path_to_save_plot/spaghetti_plot_st0.png")
