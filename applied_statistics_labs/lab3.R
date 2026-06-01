# =====
# ГЕНЕРАТОР 100 ЗНАЧЕНИЙ НА ОТРЕЗКЕ [0, 1] C РАВНОМЕРНЫМ РАСПРЕДЕЛЕНИЕМ
# =====

rand_var_unif <- runif(100, min = 0, max = 1)
ks_unif <- ks.test(rand_var_unif, "punif", 0, 1) # Критерий Колмогорова-Смирнова

# Проверка гипотезы о равн. распределении
cat(sprintf("p-value = %f -- ", ks_unif$p.value))
cat(ifelse(ks_unif$p.value > 0.05,
           "не отвергаем\n",
           "отвергаем\n"))

# Вывод графика
hist(rand_var_unif,
     probability = TRUE,
     main = "Гистограмма равн. распр. на [0,1]",
     xlab = "Значения случайной величины",
     ylab = "Плотность")
curve(dunif(x, 0, 1), add = TRUE, col = "red", lwd = 2) # Теоретическая плотность

# =====
# МОДЕЛИРОВАНИЕ СВ С РАВНОМЕРНЫМ РАСПРЕДЕЛЕНИЕМ
# =====

create_rand_var_unif <- function(n, a, b) {
  rand_var <- runif(n, min = a, max = b)
  return(rand_var)
}

print("Моделирование СВ с равн. распред.")
n <- as.numeric(readline("Введите количество значений: "))
a <- as.numeric(readline("Введите нижнюю границу: "))
b <- as.numeric(readline("Введите верхнюю границу: "))

test_rand_var <- create_rand_var_unif(n, a, b)
print(test_rand_var)

hist(test_rand_var,
     probability = TRUE,
     main = "Гистограмма равн. распр. на [a,b]",
     xlab = "Значения случайной величины",
     ylab = "Плотность")
curve(dunif(x, a, b), add = TRUE, col = "red", lwd = 2) # Теоретическая плотность

# =====
# МОДЕЛИРОВАНИЕ СВ С НОРМАЛЬНЫМ РАСПРЕДЕЛЕНИЕМЦ
# =====

create_rand_var_norm <- function(n, mean, sd) {
  rand_var <- rnorm(n, mean = mean, sd = sd)
  return(rand_var)
}

print("Моделирование СВ с норм. распред.")
n <- as.numeric(readline("Введите количество значений: "))
mean <- as.numeric(readline("Введите мат. ожидание: "))
sd <- as.numeric(readline("Введите станд. отклонение: "))

test_rand_var <- create_rand_var_norm(n, mean, sd)

hist(test_rand_var,
     probability = TRUE,
     main = "Гистограмма норм. распр.",
     xlab = "Значения случайной величины",
     ylab = "Плотность")
curve(dnorm(x, mean, sd), add = TRUE, col = "red", lwd = 2) # Теоретическая плотность

# =====
# МОДЕЛИРОВАНИЕ СВ С ПОКАЗАТЕЛЬНЫМ РАСПРЕДЕЛЕНИЕМ
# =====

create_rand_var_exp <- function(n, lambda) {
  rand_var <- rexp(n, rate = lambda)
  return(rand_var)
}

print("Моделирование СВ с показ. распред.")
n <- as.numeric(readline("Введите количество значений: "))
lambda <- as.numeric(readline("Введите интенсивность: "))

test_rand_var <- create_rand_var_exp(n, lambda)

hist(test_rand_var,
     probability = TRUE,
     main = "Гистограмма показ. распр.",
     xlab = "Значения случайной величины",
     ylab = "Плотность")
curve(dexp(x, lambda), add = TRUE, col = "red", lwd = 2) # Теоретическая плотность

# =====
# МЕТОД МОНТЕ-КАРЛО ДЛЯ ИНТЕГРАЛОВ
# =====

monte_carlo_integral <- function(f, a, b, n = 10000) {
  x <- create_rand_var_unif(n, a, b)
  fx <- f(x)
  result <- (b - a) * mean(fx)
  return(result)
}

print("Метод Монте-Карло для интегралов")
f_input <- readline("Введите функцию f(x): ")
f <- function(x) eval(parse(text = f_input)) # Преобразуем строку в функцию
a <- as.numeric(readline("Введите нижнюю границу: "))
b <- as.numeric(readline("Введите верхнюю границу: "))

result <- monte_carlo_integral(f, a, b)
print(result)

# =====
# МЕТОД МОНТЕ-КАРЛО ДЛЯ ЭКСТРЕМУМОВ
# =====

monte_carlo_extremum <- function(f, a, b, n = 10000) {
  x <- create_rand_var_unif(n, a, b)
  fx <- f(x)

  return(list(max(fx), min(fx)))
}

print("Метод Монте-Карло для экстремумов")
f_input <- readline("Введите функцию f(x): ")
f <- function(x) eval(parse(text = f_input))
a <- as.numeric(readline("Введите нижнюю границу: "))
b <- as.numeric(readline("Введите верхнюю границу: "))

result <- monte_carlo_extremum(f, a, b)
print(result)