import matplotlib.pyplot as plt
import numpy as np

# 定义函数 P(n)
def P(n, a=0.3, b=0.7, k=0.2):
    return a + (b - a) * (1 - np.exp(-k * n))

# 定义 n 的范围
n_values = np.linspace(1, 30, 400)
P_values = P(n_values)

# 绘制曲线
plt.figure(figsize=(10, 6))
plt.plot(n_values, P_values, label='P(n)', color='b')
plt.axhline(y=0.3, color='r', linestyle='--', label='P(n) = 0.3 (min value)')
plt.axhline(y=0.7, color='g', linestyle='--', label='P(n) = 0.7 (max value)')
plt.title('P(n) vs n')
plt.xlabel('n')
plt.ylabel('P(n)')
plt.legend()
plt.grid(True)
plt.show()
