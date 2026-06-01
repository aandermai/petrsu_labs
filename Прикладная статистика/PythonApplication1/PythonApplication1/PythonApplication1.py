from tkinter import W
import numpy as np
import pandas as pd
import scipy.stats as stats
import math

def pareto_rvs(shape, scale=1, size=None):
    #"""Генерация случайных чисел по распределению Парето."""
    U = np.random.uniform(size=size)
    return scale / (U**(1/shape))

def exponential_rvs(rate, size=None):
    #"""Генерация случайных чисел по экспоненциальному распределению."""
    U = np.random.uniform(size=size)
    return -np.random.exponential(1/rate, size=size)

def lindli_pareto(N, lambd, location, shape):
    w = np.zeros(N)
    s = pareto_rvs(shape, location, N)
    S = s**2
    tau = exponential_rvs(lambd / np.mean(s), N)
    print(np.mean(s) / np.mean(tau))
    
    for i in range(1, N):
        
        w[i] = max(0, w[i-1] + (s[i-1] - tau[i-1]))
        
    rho = np.mean(s) / np.mean(tau)
    df = pd.DataFrame({'w': w, 'rho': rho})
    return df

def rssimple(x):
    n = len(x)
    y = x - np.mean(x)
    s = np.cumsum(y)
    rs = (np.max(s) - np.min(s)) / np.std(x)
    return np.log(rs) / np.log(n)

def q(X, L):
    return (np.abs(np.sum(X*np.exp(1j*L*np.arange(len(X)))**2) / (2*np.pi*len(X))))

def FDtest(X, alpha, s):
    n = len(X)
    m = int(math.sqrt(n))
    l = n // m
    Q = 0
    
    for j in range(1, s+1):
        L = 2*np.pi*j/n
        denominator = np.mean([q(X[i:i+m],L) for i in range(0, n, m)])
        nominator = q(X, L)
        Q += nominator / denominator
    
    gamma_dist = stats.gamma(a=s)
    G = gamma_dist.isf(alpha)
    if Q > G:
        FD = np.array([Q, G])
        return "LRD"
    else:
        FD = np.array([Q, G])
        return "SRD"

def LRtest(X, alpha):
    n = len(X)
    #phi1 = np.correlate(X, X, mode='full')[:n]
    #phi = phi1[1]
    phi = 0.01
    m_bot = 0.06*n**(4/5)
    m_top = 1.2*n**(4/5)
    m_mid = ((3*n/(4*np.pi))**(4/5)*abs(-phi/(-(1-phi)**2))**(-2/5))
    
    if m_mid > m_bot:
        if m_mid < m_top:
            m = math.trunc( m_mid)
        else:
            m =  math.trunc(m_top)
    else:
        m = math.trunc(m_bot)
    nu=np.log(np.arange(1, m+1)-np.mean(np.log(np.arange(1, m+1))))
    nominator=0
    denominator=0
    for j in range(1, m+1):
        L = 2*np.pi*j/n
        denominator+=q(X, L)
        nominator+=nu[j-1]*q(X, L)
    
    T = np.sqrt(m)*(nominator / denominator)
    LM = T**2
    P = stats.norm().isf(1-alpha/2)
    
    if T < P:
        if T > -P:
            return "SRD"
        else:
            return "LRD"
    else:
        return "Anti-persistent"

def swap_rho(lambda_, shape):
    N = 1000
    M = 10
    s = 3
    alpha = 0.1
    FD = pd.DataFrame(columns=[f'FD_{M}', f'FD_EW_{M}'])
    LR = pd.DataFrame(columns=[f'LR_{M}', f'LR_EW_{M}'])
    W = lindli_pareto(N, lambd=lambda_, location=1, shape=shape)
    FD[f'FD_{1}'] = FDtest(W['w'], alpha, s)
    LR[f'LR_{1}'] = LRtest(W['w'], alpha)
    rho = W['rho'][0]
    EW = (lambda_*(2/shape**2) / (2*(1 - rho)))
    EW = np.mean(W['w'])
    W_EW = W['w'] - EW
    FD[f'FD_EW_{1}'] = FDtest(W_EW, alpha, s)
    LR[f'LR_EW_{1}'] = LRtest(W_EW, alpha)
    
    for i in range(2, M+1):
        W = pd.concat([W, lindli_pareto(N, lambd=lambda_, location=1, shape=shape)])
        FD[f'FD_{i}'] = FDtest(W['w'], alpha, s)
        LR[f'LR_{i}'] = LRtest(W['w'], alpha)
        rho = W['rho'][0]
        EW = (lambda_*(2/shape**2) / (2*(1 - rho)))
        EW = np.mean(W['w'])
        W_EW = W['w'] - EW
        FD[f'FD_EW_{i}'] = FDtest(W_EW, alpha, s)
        LR[f'LR_EW_{i}'] = LRtest(W_EW, alpha)

    name_FD = f'FD_pareto_{shape}_rho_{lambda_}.csv'
    name_LR = f'LR_pareto_{shape}_rho_{lambda_}.csv'
    FD.to_csv(name_FD)
    LR.to_csv(name_LR)
    name_FD_EW = f'FDEW_pareto_{shape}_rho_{lambda_}.csv'
    name_LR_EW = f'LREW_pareto_{shape}_rho_{lambda_}.csv'
    #FD_EW.to_csv(name_FD_EW)
    #LR_EW.to_csv(name_LR_EW)

for a in [3.2, 4.8]:
    for r in np.arange(0.1, 0.91, 0.1):
        swap_rho(r, a)