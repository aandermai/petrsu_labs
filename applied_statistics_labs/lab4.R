library(readxl)
library(corrplot)
library(car)
library(ggplot2)
library(dplyr)

my_data <- read_excel("./statistic_table_lab1.xlsx")
df <- my_data[, 1:7]
X <- df[, c("Уровень инновационного производства", "Количество студентов (СПО)", "Количество студентов (ВПО)", "ВРП", "Розничные продажи", "Потребительские расходы")]

# корреляционная матрица
cor_matrix <- cor(X)
print(cor_matrix)

# p-value для каждой пары, p-value (<0.05) --- связь
# статистически значима (есть основания отвергнуть гипотезу о независимости)
p_matrix <- cor.mtest(X, conf.level = 0.95)$p

cat("Корреляционная матрица Пирсона:\n")
print(round(cor_matrix, 3))

# График
corrplot(cor_matrix, method = "color", type = "upper", order = "hclust",
         addCoef.col = "black", tl.col = "black", tl.srt = 45,
         p.mat = p_matrix, sig.level = 0.05, insig = "blank",
         title = "Корреляционная матрица (Пирсон)", mar = c(0,0,1,0))

# Находим пары, у которых p-value < 0.05 (значимая связь) и которые находятся
# в нижнем треугольнике матрицы
pairs_signif <- which(p_matrix < 0.05 & lower.tri(p_matrix), arr.ind = TRUE)

# Если такие пары есть, для каждой рисуем диаграмму рассеяния
if (nrow(pairs_signif) > 0) {
  for (i in 1:nrow(pairs_signif)) {
    row_idx <- pairs_signif[i, 1]
    col_idx <- pairs_signif[i, 2]
    var1 <- colnames(X)[col_idx]
    var2 <- colnames(X)[row_idx]
    
    # График
    p <- ggplot(X, aes(x = .data[[var1]], y = .data[[var2]])) +
      geom_point(color = "steelblue", alpha = 0.7) +
      geom_smooth(method = "lm", se = FALSE, color = "red") +
      labs(title = paste("Диаграмма рассеяния:", var1, "vs", var2),
           x = var1, y = var2) +
      theme_minimal()
    print(p)
  }
} else {
  cat("Нет значимых пар (p < 0.05)\n")
}

# 4.2 Ранговая корреляция

# Модули коэффициентов
cor_abs <- abs(cor_matrix)

# Убираем диагональ (корреляция с самой собой = 1)
diag(cor_abs) <- NA

# Находим координаты ячейки с максимальным значением
ind_max <- which(cor_abs == max(cor_abs, na.rm = TRUE), arr.ind = TRUE)[1, ]
var_i <- colnames(X)[ind_max[1]]   # первая переменная пары
var_j <- colnames(X)[ind_max[2]]   # вторая
cat("\nМаксимальная |r| =", round(max(cor_abs, na.rm = TRUE), 4),
    "между", var_i, "и", var_j, "\n")

# Два столбца в отдельные векторы
x <- X[[var_i]]
y <- X[[var_j]]

# Ранговые корреляции
# Спирмен –-- считает по рангам значений
spearman_test <- cor.test(x, y, method = "spearman")
# Кэнделл --- основан на числе согласованных и несогласованных пар
kendall_test  <- cor.test(x, y, method = "kendall")

cat("Коэффициент Спирмена: rho =", round(spearman_test$estimate, 4), 
    "p =", format(spearman_test$p.value, scientific = TRUE), "\n")
cat("Коэффициент Кэнделла: tau =", round(kendall_test$estimate, 4), 
    "p =", format(kendall_test$p.value, scientific = TRUE), "\n")

# Хи-квадрат
# Для этого разбиваем каждую переменную на 3 равные части:
bx <- quantile(x, probs = c(0, 1/3, 2/3, 1), na.rm = TRUE)   # границы для x
by <- quantile(y, probs = c(0, 1/3, 2/3, 1), na.rm = TRUE)   # границы для y
# Превращаем числа в категории "Низкий", "Средний", "Высокий"
x_cat <- cut(x, breaks = bx, include.lowest = TRUE, labels = c("Низкий","Средний","Высокий"))
y_cat <- cut(y, breaks = by, include.lowest = TRUE, labels = c("Низкий","Средний","Высокий"))
# Строим таблицу сопряжённости и применяем тест хи-квадрат
chi2 <- chisq.test(table(x_cat, y_cat))
cat("Критерий Хи-квадрат: X2 =", round(chi2$statistic, 2), 
    "df =", chi2$parameter, "p =", format(chi2$p.value, scientific = TRUE), "\n")

# 4.3 Линейная регрессия

# Y -- зависимая переменная (то, что предсказываем)
Y <- X$ВРП

# X_reg -- независимые переменные (все, кроме ВРП)
X_reg <- X[, c("Уровень инновационного производства", "Количество студентов (СПО)", "Количество студентов (ВПО)", "Розничные продажи", "Потребительские расходы")]  

# Линейная модель
model_lin <- lm(Y ~ ., data = X_reg)

# Сводка
summary(model_lin)

# Диагностические графики модели
# Residuals vs Fitted: остатки против предсказанных
# Q-Q plot: нормальность остатков (точки должны лечь на прямую)
# Scale-Location: постоянство дисперсии
# Residuals vs Leverage: влиятельные наблюдения
par(mfrow = c(2, 2))
plot(model_lin)

# 4.4

# Какой из пяти предикторов (кроме ВРП) сильнее всего коррелирует с Y
vars <- c("Уровень инновационного производства", "Количество студентов (СПО)", "Количество студентов (ВПО)", "Розничные продажи", "Потребительские расходы")
cor_with_Y <- sapply(X[vars], function(x) cor(x, Y))   # считаем корреляции
best_x_name <- names(which.max(abs(cor_with_Y)))       # имя самого сильного X
best_x <- X[[best_x_name]]                             # его значения
cat("\nДля нелинейных регрессий выбран X =", best_x_name, 
    "корреляция с Y =", round(max(abs(cor_with_Y)), 4), "\n")

# Регрессии
# Логарифмическая: Y = a + b * ln(X)   (исходный Y, логарифм X)
model_log <- lm(Y ~ log(best_x))

# Степенная: ln(Y) = a + b * ln(X)  => Y = exp(a) * X^b
model_pow <- lm(log(Y) ~ log(best_x))

# Показательная: ln(Y) = a + b * X  => Y = exp(a) * exp(b*X)
model_exp <- lm(log(Y) ~ best_x)

# Сравниваем качество моделей
cat("\nСравнение моделей (R²):\n")
cat("Логарифмическая:", round(summary(model_log)$r.squared, 4), "\n")
cat("Степенная:", round(summary(model_pow)$r.squared, 4), "\n")
cat("Показательная:", round(summary(model_exp)$r.squared, 4), "\n")

# Строим график исходных точек и всех трёх кривых регрессии
# Последовательность X от минимума до максимума (100 точек)
x_seq <- seq(min(best_x), max(best_x), length = 100)

# Предсказания по каждой модели
pred_log <- predict(model_log, newdata = data.frame(best_x = x_seq))   # Y
pred_pow <- exp(predict(model_pow, newdata = data.frame(best_x = x_seq))) # Y
pred_exp <- exp(predict(model_exp, newdata = data.frame(best_x = x_seq))) # Y

ggplot(data.frame(X = best_x, Y = Y), aes(x = X, y = Y)) +
  geom_point(alpha = 0.6, color = "black") +   # исходные точки
  geom_line(aes(x = x_seq, y = pred_log), color = "blue", linewidth = 1, linetype = "solid") +   # логарифмическая
  geom_line(aes(x = x_seq, y = pred_pow), color = "red", linewidth = 1, linetype = "dashed") +    # степенная
  geom_line(aes(x = x_seq, y = pred_exp), color = "green", linewidth = 1, linetype = "dotted") +  # показательная
  labs(title = paste("Регрессии Y (ВРП) на X =", best_x_name),
       x = best_x_name, y = "Валовой региональный продукт") +
  theme_minimal()
