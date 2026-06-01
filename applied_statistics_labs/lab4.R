library(readxl)

my_data <- read_excel("./statistic_table_lab1.xlsx")

# параметры
x1 <- my_data$`Уровень инновационного производства`
x2 <- my_data$`Количество студентов (СПО)`
x3 <- my_data$`Количество студентов (ВПО)`
x4 <- my_data$`ВРП`
x5 <- my_data$`Розничные продажи`
x6 <- my_data$`Потребительские расходы`

X <- data.frame(x1, x2, x3, x4, x5, x6)

# корреляционная матрица
cor_matrix <- cor(X)
print(cor_matrix)

# проверка гипотез о независимости
vars <- list(x1, x2, x3, x4, x5, x6)
names <- c("x1", "x2", "x3", "x4", "x5", "x6")
independent_couples <- list()

for(i in 1:(length(vars)-1)) {
  for(j in (i+1):length(vars)) {
    test <- cor.test(vars[[i]], vars[[j]])
    
    cat("\n")
    cat(names[i], "--", names[j], "\n")
    cat("correlation =", test$estimate, "\n")
    cat("p-value =", test$p.value, "\n")
    
    if(test$p.value > 0.05) {
      cat("Пара независима\n")
    } else {
      cat("Пара зависима\n")
      plot(
        vars[[i]],
        vars[[j]],
        main = paste(names[i], "vs", names[j]),
        xlab = names[i],
        ylab = names[j]
      )
    }
  }
}

# линейная регрессия
y <- my_data$`Розничные продажи`
linear_model <- lm(y ~ x1 + x2 + x3 + x4 + x6)
summary_model <- summary(linear_model)
print(summary_model)

summary(x6)
summary(y)

# логарифмическая регрессия
log_model <- lm(y ~ log(x6))
summary(log_model)

# показательная регрессия
exp_model <- lm(log(y) ~ x6)
summary(exp_model)

# степенная регрессия
power_model <- lm(log(y) ~ log(x6))
summary(power_model)
