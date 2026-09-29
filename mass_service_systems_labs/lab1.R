variant_number <- 17 # Номер варианта
lambda <- variant_number + 1 # Интенсивность
mu <- variant_number + 2 # Мат. ожидание
s <- 4 # Произвольная дисперсия больше 0
sd <- sqrt(s) # Стандартное отклонение

###########################
# ПОКАЗАТЕЛЬНОЕ РАСПРЕДЕЛЕНИЕ
###########################

x <- rexp(n = 10000, rate = lambda)

par(mfrow= c(1, 3))

# Размер выборки 10_000
hist(x, breaks = 50, probability = TRUE,
     main = "Выборка 10000",
     xlab = "x", col = "lightblue")
curve(dexp(x, rate = lambda),
      add = TRUE, col = "red", lwd = 2)

# Размер выборки 1000
hist(x[1:1000], breaks = 30, probability = TRUE,
     main = "Выборка 1000",
     xlab = "x", col = "lightgreen")
curve(dexp(x, rate = lambda),
      add = TRUE, col = "red", lwd = 2)

# Размер выборки 100
hist(x[1:100], breaks = 15, probability = TRUE,
     main = "Выборка 100",
     xlab = "x", col = "lightyellow")
curve(dexp(x, rate = lambda),
      add = TRUE, col = "red", lwd = 2)



###########################
# НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ
###########################
x <- rnorm(10000, mean=mu, sd=sd)

# Выборка 10_000
hist(x, breaks = 40, probability = TRUE,
     main = "Выборка 10000",
     xlab = "x",
     col = "lightblue")

curve(dnorm(x, mean = mu, sd = sd),
      add = TRUE, col = "red", lwd = 2)


# Выборка 1000
hist(x[1:1000], breaks = 30, probability = TRUE,
     main = "Выборка 1000",
     xlab = "x",
     col = "lightgreen")

curve(dnorm(x, mean = mu, sd = sd),
      add = TRUE, col = "red", lwd = 2)


# Выборка 100
hist(x[1:100], breaks = 15, probability = TRUE,
     main = "Выборка 100",
     xlab = "x",
     col = "lightyellow")

curve(dnorm(x, mean = mu, sd = sd),
      add = TRUE, col = "red", lwd = 2)

###########################
# ЗАКОН БОЛЬШИХ ЧИСЕЛ
###########################
s1 <- 1
s2 <- 4
s3 <- 9

x1 <- rnorm(10000, mean = mu, sd = sqrt(s1))
x2 <- rnorm(10000, mean = mu, sd = sqrt(s2))
x3 <- rnorm(10000, mean = mu, sd = sqrt(s3))

mean1 <- cumsum(x1) / (1:10000)
mean2 <- cumsum(x2) / (1:10000)
mean3 <- cumsum(x3) / (1:10000)

par(mfrow= c(1, 1))

plot(1:10000, mean1,
     type = "l",
     xlab = "Объём выборки",
     ylab = "Выборочное среднее",
     main = "Закон больших чисел",
     ylim = c(15, 23))

lines(1:10000, mean2, col = "red")
lines(1:10000, mean3, col = "green")

# Теоретическое математическое ожидание
abline(h = mu, col = "blue", lwd = 2, lty = 2)

legend("topright",
       legend = c("D = 1", "D = 4", "D = 9", "m = 19"),
       col = c("black", "red", "green", "blue"),
       lty = c(1, 1, 1, 2))

###########################
# ЦЕНТРАЛЬНАЯ ПРЕДЕЛЬНАЯ ТЕОРЕМА
###########################
# 1. Параметры задания
n <- 1            # Подставь свой номер варианта!
mu <- n + 2       # Параметр среднего (n + 2)
s <- 4            # Произвольная дисперсия s > 0
sd_val <- sqrt(s) # Среднеквадратичное отклонение sigma
N <- 10000        # Объём выборки (10 000 с.ч.)

# 2. Генерация 10 000 нормальных случайных чисел по ЦПТ
# Создаём матрицу 10000 x 12 из равномерных чисел U(0, 1)
u_matrix <- matrix(runif(N * 12), nrow = N, ncol = 12)

# Суммируем по строкам и центрируем (Z ~ N(0, 1))
z_clt <- rowSums(u_matrix) - 6

# Масштабируем и сдвигаем к заданному среднему mu и дисперсии s
x_clt <- mu + sd_val * z_clt

# 3. Построение гистограммы частот
hist_info <- hist(x_clt, 
                  breaks = 40, 
                  freq = TRUE, 
                  main = paste0("Гистограмма частот (ЦПТ)\nmu = ", mu, ", s = ", s),
                  xlab = "Значения x", 
                  ylab = "Частота (Counts)",
                  col = "lightgreen", 
                  border = "white")

# Наложение теоретической кривой частот
x_seq <- seq(min(x_clt), max(x_clt), length.out = 200)
bin_width <- diff(hist_info$mids[1:2])
y_theory_freq <- dnorm(x_seq, mean = mu, sd = sd_val) * N * bin_width
lines(x_seq, y_theory_freq, col = "darkgreen", lwd = 2)

# 4. Тест Колмогорова-Смирнова
ks_result <- ks.test(x_clt, "pnorm", mean = mu, sd = sd_val)
print(ks_result)

###########################
# РАСПРЕДЕЛЕНИЕ ПАРЕТО
###########################
# 1. Параметры по условию
n <- 1          # Подставь свой номер варианта!
x0 <- 2         # Коэффициент масштаба
alpha <- n + 5  # Параметр Парето
N <- 10000      # Объём выборки

# 2. Генерация методом обратной функции
u <- runif(N)
x_pareto <- x0 / ((1 - u)^(1 / alpha))

# 3. Функция теоретической плотности
f_theory <- function(x) {
  ifelse(x >= x0, (alpha * (x0^alpha)) / (x^(alpha + 1)), 0)
}

# 4. Визуализация и сравнение
# Из-за длинного "хвоста" ограничим график 99-м перцентилем для наглядности
xlim_max <- quantile(x_pareto, 0.99)

hist(x_pareto, breaks = 100, probability = TRUE,
     xlim = c(x0, xlim_max),
     main = paste0("Распределение Парето (n = ", n, ", alpha = ", alpha, ")"),
     xlab = "x", ylab = "Плотность",
     col = "lightblue", border = "white")

# Эмпирическая плотность (оценка)
lines(density(x_pareto), col = "blue", lwd = 2)

# Теоретическая плотность
curve(f_theory(x), from = x0, to = xlim_max,
      col = "red", lwd = 2, lty = 2, add = TRUE)

legend("topright", 
       legend = c("Эмпирическая плотность", "Теоретическая плотность"),
       col = c("blue", "red"), lty = c(1, 2), lwd = 2)