library(readxl)

table <- read_excel("table.xlsx", sheet="Таблица")

df_raw <- data.frame(
  Занятые = table$`Число занятых в экономике`,
  Безработица = table$`Уровень безработицы`,
  Доходы = table$`Уровень доходов населения`,
  Розница = table$`Розничные продажи`,
  Индекс = table$`Индекс пром. Производства`,
  ВРП = table$`Валовой региональный продукт`
)

df_raw <- na.omit(df_raw)

# Отделяем признаки X и Y
X <- df_raw[, 1:5]
Y <- df_raw$ВРП

# Краткая статистика исходных данных
cat("Исходные данные:\n")
print(head(X))
cat("\nРазмерность:", dim(X), "\n")

# Стандартизация
X_scaled <- scale(X)

# Метод главных компонент

pca_result <- prcomp(X_scaled, center = TRUE, scale. = TRUE)

# Вывод результатов
cat("\n========================================\n")
cat("РЕЗУЛЬТАТЫ КОМПОНЕНТНОГО АНАЛИЗА\n")
cat("========================================\n")

# Собственные значения (дисперсии компонент) и их доли
eigenvals <- pca_result$sdev^2
prop_variance <- eigenvals / sum(eigenvals)
cum_prop <- cumsum(prop_variance)

cat("\nСобственные значения (дисперсии):\n")
print(round(eigenvals, 4))

cat("\nДоля объяснённой дисперсии каждой компонентой:\n")
print(round(prop_variance, 4))

cat("\nНакопленная доля объяснённой дисперсии:\n")
print(round(cum_prop, 4))

# График
plot(eigenvals, type = "b", pch = 19, col = "blue",
     main = "Собственные значения",
     xlab = "Номер главной компоненты", ylab = "Собственное значение")
abline(h = 1, col = "red", lty = 2)

# Необходимое число компонент
n_comp_kaiser <- sum(eigenvals > 1) # собственное значение > 1 (правило Кайзера)
n_comp_80 <- which(cum_prop >= 0.8)[1] # накопленная доля дисперсии

cat("\nПравило Кайзера (собственные значения > 1):", n_comp_kaiser, "компоненты\n")
cat("Накопленная дисперсия >= 80% требует", n_comp_80, "компонент(ы)\n")

# Рекомендуемое число компонент
n_comp <- min(n_comp_kaiser, n_comp_80)
cat("Рекомендуемое число главных компонент:", n_comp, "\n")

# Факторные нагрузки (корреляции исходных переменных с компонентами)

# коэффициенты корреляции = умножить веса на sqrt(собственного значения)
loadings <- pca_result$rotation %*% diag(sqrt(eigenvals))
colnames(loadings) <- paste0("PC", 1:ncol(loadings))
rownames(loadings) <- colnames(X)

cat("\n========================================\n")
cat("Факторные нагрузки (корреляции переменных с компонентами)\n")
cat("========================================\n")
print(round(loadings, 4))

# Квадраты нагрузок –-- вклад каждой переменной в компоненту
squared_loadings <- loadings^2
cat("\nКвадраты факторных нагрузок (доля дисперсии переменной, объяснённая компонентой):\n")
print(round(squared_loadings, 4))

# Суммы квадратов нагрузок по строкам --– не должны быть > 1
communalities <- rowSums(squared_loadings)
cat("\nОбщности (доля дисперсии каждой переменной, объяснённая всеми компонентами):\n")
print(round(communalities, 4))

# Интерпретация ГК

# Смотрим на нагрузки с большими абсолютными значениями
cat("\n========================================\n")
cat("Интерпретация компонент (по нагрузкам)\n")
cat("========================================\n")

for (i in 1:n_comp) {
  cat("\nГлавная компонента", i, "(доля дисперсии:", round(prop_variance[i], 3), ")\n")
  # Находим переменные с нагрузкой по модулю > 0.5 (значимый вклад)
  high_loadings <- loadings[, i][abs(loadings[, i]) > 0.5]
  if (length(high_loadings) > 0) {
    cat("  Переменные с высокой нагрузкой:\n")
    print(round(sort(high_loadings, decreasing = TRUE), 4))
  } else {
    cat("  Нет переменных с нагрузкой >0.5 (все слабые)\n")
  }
}

# Графики

# График долей дисперсии
barplot(prop_variance, names.arg = paste0("PC", 1:length(prop_variance)),
        main = "Доля объяснённой дисперсии каждой компонентой",
        xlab = "Главные компоненты", ylab = "Доля дисперсии",
        col = "lightblue")
lines(cum_prop, type = "b", pch = 19, col = "red")
legend("topright", legend = c("Доля", "Накопленная"), col = c("lightblue", "red"), lty = 1, pch = c(15, 19))

# Проекция наблюдений и нагрузок
biplot(pca_result, main = "Первые 2 ГК",
       xlab = paste0("PC1 (", round(prop_variance[1]*100, 1), "%)"),
       ylab = paste0("PC2 (", round(prop_variance[2]*100, 1), "%)"))

# Связь первой главной компоненты С Y

PC1 <- pca_result$x[, 1]

# Корреляция Пирсона между PC1 и Y
cor_pearson <- cor(PC1, Y, method = "pearson")
cat("\n========================================\n")
cat("Связь первой ГК с Y (ВРП)\n")
cat("========================================\n")
cat("Коэффициент корреляции Пирсона: r =", round(cor_pearson, 4), "\n")
if (abs(cor_pearson) > 0.7) {
  cat("Связь сильная (|r| > 0.7)\n")
} else if (abs(cor_pearson) > 0.4) {
  cat("Связь умеренная\n")
} else {
  cat("Связь слабая\n")
}

# График разброса
plot(PC1, Y, pch = 19, col = "darkgreen",
     main = "Зависимость ВРП от первой ГК",
     xlab = "Первая ГК (PC1)", ylab = "ВРП (млн руб.)")
abline(lm(Y ~ PC1), col = "red", lwd = 2)

# Тест значимости корреляции
cor_test <- cor.test(PC1, Y)
cat("\nПроверка значимости корреляции: p-value =", cor_test$p.value, "\n")
if (cor_test$p.value < 0.05) {
  cat("Корреляция статистически значима (p < 0.05).\n")
} else {
  cat("Корреляция незначима\n")
}

# Выводы

cat("\n========================================\n")
cat("ВЫВОДЫ\n")
cat("========================================\n")
cat("1. Для описания основных закономерностей достаточно", n_comp, "главных компонент.\n")
cat("   Они объясняют", round(cum_prop[n_comp]*100, 1), "% суммарной дисперсии исходных признаков.\n")
cat("2. Наибольший вклад в первую компоненту вносят переменные:\n")
first_comp_load <- sort(loadings[,1], decreasing = TRUE)
print(round(first_comp_load, 4))
cat("3. Вторая компонента наиболее сильно связана с:\n")
second_comp_load <- sort(loadings[,2], decreasing = TRUE)
print(round(second_comp_load, 4))
cat("4. Корреляция первой главной компоненты с ВРП составляет",
    round(cor_pearson, 4), "и является", 
    ifelse(cor_test$p.value < 0.05, "статистически значимой", "незначимой"), "\n")

cat("\nАнализ завершён.\n")