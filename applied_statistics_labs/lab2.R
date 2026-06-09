library(readxl)
options(warn = -1)

# Чтение таблицы Excel
my_data <- read_excel("./statistic_table_lab1.xlsx")

# Выбор трёх параметров
x1 <- my_data$`Количество студентов (СПО)`
x2 <- my_data$`Количество студентов (ВПО)`
x3 <- my_data$`ВРП`

# Функция критерия согласия
goodness_of_fit_test <- function(selection, param_name, alpha = 0.1) {
  cat("============================\n")
  cat("ПАРАМЕТР:", param_name, "\n")
  cat("============================\n")
  
  selection_mean <- mean(selection) # Мат. Ожидание
  selection_sd <- sd(selection) # Средн. отклонение
  lambda <- 1 / selection_mean # Интенсивность 
  a <- min(selection) # Нижняя граница
  b <- max(selection) # Верхняя граница
  
  # Критерий Колмогорова-Смирнова
  cat("КРИТЕРИЙ КОЛМОГОРОВА-СМИРНОВА\n")
  
  # Нормальное распределение
  ks_norm <- ks.test(selection, "pnorm", selection_mean, selection_sd)
  cat("\nНормальное распределение:\n"); print(ks_norm)
  cat(ifelse(ks_norm$p.value > alpha, "-> не отвергаем", "-> отвергаем"), "\n")

  # Показательное распределение
  ks_exp <- ks.test(selection, "pexp", lambda)
  cat("\nПоказательное распределение:\n"); print(ks_exp)
  cat(ifelse(ks_exp$p.value > alpha, "-> не отвергаем", "-> отвергаем"), "\n")

  # Равномерное распределение 
  ks_unif <- ks.test(selection, "punif", a, b)
  cat("\nРавномерное распределение:\n"); print(ks_unif)
  cat(ifelse(ks_unif$p.value > alpha, "-> не отвергаем", "-> отвергаем"), "\n")
  
  # Критерий Пирсона
  cat("КРИТЕРИЙ ПИРСОНА\n")

  # Разбиваем данные на интервалы (число интервалов = корень из объёма выборки)
  breaks_num <- round(sqrt(length(selection)))
  breaks <- hist(selection, plot = FALSE, breaks = breaks_num)$breaks
  observed <- hist(selection, plot = FALSE, breaks = breaks)$counts   # частоты
  
  # Нормальное распределение
  p_norm <- diff(pnorm(breaks, selection_mean, selection_sd))      # теоретические вероятности
  chisq_norm <- chisq.test(observed, p = p_norm, rescale.p = TRUE)
  cat("\nНормальное распределение:\n"); print(chisq_norm)
  cat(ifelse(chisq_norm$p.value > alpha, "-> не отвергаем", "-> отвергаем"), "\n")
  
  # Показательное распределение
  p_exp <- diff(pexp(breaks, lambda))
  chisq_exp <- chisq.test(observed, p = p_exp, rescale.p = TRUE)
  cat("\nПоказательное распределение:\n"); print(chisq_exp)
  cat(ifelse(chisq_exp$p.value > alpha, "-> не отвергаем", "-> отвергаем"), "\n")
  
  # Равномерное распределение
  p_unif <- diff(punif(breaks, a, b))
  chisq_unif <- chisq.test(observed, p = p_unif, rescale.p = TRUE)
  cat("\nРавномерное распределение:\n"); print(chisq_unif)
  cat(ifelse(chisq_unif$p.value > alpha, "-> не отвергаем", "-> отвергаем"), "\n")
  
  par(mfrow = c(1, 3))

  # Нормальное
  hist(selection, probability = TRUE, main = paste(param_name, "\nНормальное"), col = "lightblue")
  curve(dnorm(x, mean = selection_mean, sd = selection_sd), col = "red", lwd = 2, add = TRUE)
  # Показательное
  hist(selection, probability = TRUE, main = paste(param_name, "\nПоказательное"), col = "lightgreen")
  curve(dexp(x, rate = lambda), col = "blue", lwd = 2, add = TRUE)
  # Равномерное
  hist(selection, probability = TRUE, main = paste(param_name, "\nРавномерное"), col = "lightpink")
  curve(dunif(x, min = a, max = b), col = "darkgreen", lwd = 2, add = TRUE)
}

goodness_of_fit_test(x1, "Количество студентов (СПО)")
goodness_of_fit_test(x2, "Количество студентов (ВПО)")
goodness_of_fit_test(x3, "ВРП")

# --- Вспомогательная функция для критерия серий
# Проверяет, случайно ли чередуются значения из двух выборок при сортировке
runs_test <- function(x, y) {
  combined <- c(x, y)                          # объединяем выборки
  labels <- c(rep(0, length(x)), rep(1, length(y))) # метки: 0 – север, 1 – юг
  ord <- order(combined)                       # сортируем значения по возрастанию
  sorted_labels <- labels[ord]                 # метки в порядке сортировки
  runs <- 1                                    # начинаем с первой серии
  for (i in 2:length(sorted_labels)) {
    if (sorted_labels[i] != sorted_labels[i-1]) runs <- runs + 1
  }
  n1 <- length(x); n2 <- length(y)
  exp_runs <- 2*n1*n2/(n1+n2) + 1              # ожидаемое число серий
  var_runs <- (2*n1*n2*(2*n1*n2 - n1 - n2)) / ((n1+n2)^2 * (n1+n2 - 1))
  z <- (runs - exp_runs) / sqrt(var_runs)
  p_value <- 2 * pnorm(-abs(z))                # двусторонний p-value
  return(p_value)
}

# Медианный критерий для двух групп
# Проверяет, различаются ли доли наблюдений выше и ниже общей медианы
median_test <- function(x, y) {
  med <- median(c(x, y))                       # общая медиана
  # Таблица 2×2: [выше медианы, ниже/равно медианы] для каждой группы
  tab <- matrix(c(sum(x > med), sum(x <= med),
                  sum(y > med), sum(y <= med)), nrow = 2, byrow = TRUE)
  chisq.test(tab, correct = FALSE)$p.value     # p-value хи-квадрат
}

# Пункт 2
north <- subset(my_data, my_data$`тип региона` == "с")
south <- subset(my_data, my_data$`тип региона` == "ю")
center <- subset(my_data, my_data$`тип региона` == "ц")

# Функция критерия однородности для двух групп
homogeneity_test <- function(first_selection, second_selection, column_name, alpha = 0.1) {
  x <- first_selection[[column_name]]
  y <- second_selection[[column_name]]
  
  # Критерий Колмогорова-Смирнова
  ks_test <- ks.test(x, y)
  cat("Колмогоров-Смирнов: p =", ks_test$p.value,
      ifelse(ks_test$p.value < alpha, "-> отвергаем", "-> не отвергаем"), "\n")
  
  # Критерий Вилкоксона
  wilcox_test <- wilcox.test(x, y)
  cat("Вилкоксон: p =", wilcox_test$p.value,
      ifelse(wilcox_test$p.value < alpha, "-> отвергаем", "-> не отвергаем"), "\n")
  
  # Критерий серий
  runs_p <- runs_test(x, y)
  cat("Критерий серий: p =", runs_p,
      ifelse(runs_p < alpha, "-> отвергаем", "-> не отвергаем"), "\n")

  # Медианный критерий
  med_p <- median_test(x, y)
  cat("Медианный критерий: p =", med_p,
      ifelse(med_p < alpha, "-> отвергаем", "-> не отвергаем"), "\n")

    # 5. Краскела-Уоллиса –-- для двух групп
  kruskal_test <- kruskal.test(list(x, y))
  cat("Краскела-Уоллиса: p =", kruskal_test$p.value,
      ifelse(kruskal_test$p.value < alpha, "-> отвергаем", "-> не отвергаем"), "\n")

    # График
  boxplot(x, y,
          names = c("Север", "Юг"),
          main = column_name,
          ylab = column_name,
          col = c("lightblue", "lightgreen"))
}

homogeneity_test(north, south, "Количество студентов (СПО)")
homogeneity_test(north, south, "Количество студентов (ВПО)")
homogeneity_test(north, south, "ВРП")

x <- north$`Количество студентов (СПО)`
y <- south$`Количество студентов (СПО)`
z <- center$`Количество студентов (СПО)`

cat("\n========== Три группы (Валовой региональный продукт) ==========\n")
alpha = 0.1

# 1. Краскела-Уоллиса
kw3 <- kruskal.test(list(x, y, z))
cat("Краскела-Уоллиса: p =", kw3$p.value,
    ifelse(kw3$p.value < alpha, "-> отвергаем", "-> не отвергаем"), "\n")

# 2. Медианный критерий для трёх групп
med_all <- median(c(x, y, z))                # общая медиана
# Таблица 3×2: выше/ниже медианы для каждой группы
tab <- matrix(c(sum(x > med_all), sum(x <= med_all),
                sum(y > med_all), sum(y <= med_all),
                sum(z > med_all), sum(z <= med_all)), nrow = 3, byrow = TRUE)
med_p3 <- chisq.test(tab, correct = FALSE)$p.value
cat("Медианный критерий: p =", med_p3,
    ifelse(med_p3 < alpha, "-> отвергаем", "-> не отвергаем"), "\n")

# График
boxplot(x, y, z, names = c("Север", "Юг", "Центр"),
        main = "Валовой региональный продукт", ylab = "млн руб.",
        col = c("lightblue", "lightgreen", "lightyellow"))
