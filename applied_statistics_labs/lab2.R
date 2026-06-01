library(readxl)

# Чтение таблицы Excel
my_data <- read_excel("./statistic_table_lab1.xlsx")

# Выбор трёх параметров
spo_students_count <- my_data$`Количество студентов (СПО)`
vpo_students_count <- my_data$`Количество студентов (ВПО)`
innovation_level <- my_data$`Уровень инновационного производства`

# Функция критерия согласия
goodness_of_fit_test <- function(selection) {
  selection_mean <- mean(selection) # Мат. Ожидание
  selection_sd <- sd(selection) # Средн. отклонение
  lambda <- 1 / selection_mean # Интенсивность 
  a <- min(selection) # Нижняя граница
  b <- max(selection) # Верхняя граница
  
  # Критерий Колмогорова-Смирнова
  ks_norm <- ks.test(selection, "pnorm", selection_mean, selection_sd)
  ks_exp <- ks.test(selection, "pexp", lambda)
  ks_unif <- ks.test(selection, "punif", a, b)

  # Критерий Пирсона
  histogram <-  hist(selection, plot = FALSE)
  observed <- histogram$counts # Что получилось
  breaks <- histogram$breaks # Границы интервалов
  
  # Нормальное распределение
  expected_prob <- diff(pnorm(breaks, selection_mean, selection_sd))
  expected_prob <- expected_prob / sum(expected_prob)
  pirson_norm <- chisq.test(observed, p = expected_prob)

  # Показательное распределение  
  expected_prob <- diff(pexp(breaks, rate = lambda))
  expected_prob <- expected_prob / sum(expected_prob)
  pirson_exp <- chisq.test(observed, p = expected_prob)
  
  # Равномерное распределение
  expected_prob <- diff(punif(breaks, a, b))
  expected_prob <- expected_prob / sum(expected_prob)
  pirson_unif <- chisq.test(observed, p = expected_prob)
  
  par(mfrow = c(1, 3))

  hist(selection, probability = TRUE, main = "Normal")
  curve(dnorm(x, mean(selection), sd(selection)), add = TRUE)
  
  hist(selection, probability = TRUE, main = "Exponential")
  curve(dexp(x, rate = 1/mean(selection)), add = TRUE)
  
  hist(selection, probability = TRUE, main = "Uniform")
  curve(dunif(x, min(selection), max(selection)), add = TRUE)
  
  return(list(
    ks_norm = ks_norm$p.value,
    ks_exp = ks_exp$p.value,
    ks_unif = ks_unif$p.value,
    pirson_norm = pirson_norm$p.value,
    pirson_exp = pirson_exp$p.value,
    pirson_unif = pirson_unif$p.value
  ))
}

# Функция для проверки p-value с уровнем значимости
decision <- function(p_value, alpha = 0.1) {
  ifelse(p_value > alpha,
         "Не отвергается",
         "Отвергается")
}

# Проверка критерия согласия на параметрах
spo_test <- goodness_of_fit_test(spo_students_count)
vpo_test <- goodness_of_fit_test(vpo_students_count)
innovation_test <- goodness_of_fit_test(innovation_level)
cat("=== СТУДЕНТЫ СПО ===\n")
print(sapply(spo_test, decision))
cat("=== СТУДЕНТЫ ВПО ===\n")
print(sapply(vpo_test, decision))
cat("=== УРОВЕНЬ ИННОВАЦИИ ===\n")
print(sapply(innovation_test, decision))

# Пункт 2
north_regions <- subset(my_data, my_data$`тип региона` == "с")
south_regions <- subset(my_data, my_data$`тип региона` == "ю")
central_regions <- subset(my_data, my_data$`тип региона` == "ц")

# Функция критерия однородности
homogeneity_test <- function(first_selection, second_selection, column_name, alpha = 0.1) {
  # Критерий Колмогорова-Смирнова
  ks_test <- ks.test(first_selection[[column_name]], second_selection[[column_name]])
  
  # Критерий Вилкоксона
  wilcox_test <- wilcox.test(first_selection[[column_name]], second_selection[[column_name]])
  
  # Критерий серий
  runs_test <- runs.test(c(first_selection[[column_name]], second_selection[[column_name]]))
  
homogeneity_test(north_regions, south_regions, "Количество студентов (ВПО)")
  
  
}
