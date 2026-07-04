import os
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import sympy as sp

# ============================================
# ۱. تعریف تابع مورد نظر
# ============================================
def f(x):
    return np.exp(x**2)

def f_sympy(x):
    return sp.exp(x**2)

# ============================================
# ۲. روش ذوزنقه‌ای (Trapezoidal Rule) - پیاده‌سازی دستی
# ============================================
def trapezoidal_rule(f, a, b, n):
    """
    محاسبه انتگرال با روش ذوزنقه‌ای
    """
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    result = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return result

# ============================================
# ۳. روش سیمپسون 1/3 (Simpson's Rule) - پیاده‌سازی دستی
# ============================================
def simpson_rule(f, a, b, n):
    """
    محاسبه انتگرال با روش سیمپسون 1/3
    n باید زوج باشد
    """
    if n % 2 != 0:
        n += 1  # در روش سیمپسون n باید زوج باشد
    
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    
    result = (h / 3) * (y[0] + 
                         4 * np.sum(y[1:-1:2]) + 
                         2 * np.sum(y[2:-2:2]) + 
                         y[-1])
    return result

# ============================================
# ۴. روش گاوس-لژاندر (Gaussian Quadrature) - پیاده‌سازی دستی
# ============================================
def gauss_legendre(f, a, b, n):
    """
    محاسبه انتگرال با روش گاوس-لژاندر با n نقطه
    پیاده‌سازی کامل و دستی
    """
    # محاسبه نقاط و وزن‌های گاوس-لژاندر
    x, w = np.polynomial.legendre.leggauss(n)
    
    # تبدیل بازه [-1,1] به [a,b]
    t = 0.5 * (x + 1) * (b - a) + a
    
    # محاسبه انتگرال
    result = 0.5 * (b - a) * np.sum(w * f(t))
    return result

# ============================================
# ۵. محاسبه با روش‌های مختلف و مقایسه
# ============================================
def run_integration():
    print("\n" + "="*70)
    print("--- Task 3: Numerical Integration Started ---")
    print("="*70)
    
    a, b = 0, 1   # بازه انتگرال‌گیری
    n = 100       # تعداد زیربازه‌ها برای روش‌های سیمپسون و ذوزنقه
    
    print(f"\n[+] Function: f(x) = e^(x²)")
    print(f"[+] Integration Interval: [{a}, {b}]")
    print(f"[+] Number of Subintervals (n): {n}")
    
    # ============================================
    # ۶. محاسبه با روش‌های مختلف
    # ============================================
    
    # روش ذوزنقه‌ای
    val_trap = trapezoidal_rule(f, a, b, n)
    
    # روش سیمپسون
    val_simp = simpson_rule(f, a, b, n)
    
    # روش گاوس-لژاندر با 5 نقطه
    val_gauss_5 = gauss_legendre(f, a, b, 5)
    
    # روش گاوس-لژاندر با 10 نقطه (برای مقایسه)
    val_gauss_10 = gauss_legendre(f, a, b, 10)
    
    # روش گاوس-لژاندر با 20 نقطه (برای مقایسه)
    val_gauss_20 = gauss_legendre(f, a, b, 20)
    
    # مقدار دقیق (مرجع) با استفاده از scipy
    exact_val, _ = quad(f, a, b)
    
    # ============================================
    # ۷. محاسبه خطاها
    # ============================================
    err_trap = abs(val_trap - exact_val)
    err_simp = abs(val_simp - exact_val)
    err_gauss_5 = abs(val_gauss_5 - exact_val)
    err_gauss_10 = abs(val_gauss_10 - exact_val)
    err_gauss_20 = abs(val_gauss_20 - exact_val)
    
    # ============================================
    # ۸. نمایش نتایج
    # ============================================
    print("\n[+] Results:")
    print("-"*70)
    print(f"{'Method':<25} | {'Value':<18} | {'Absolute Error':<15}")
    print("-"*70)
    print(f"{'Trapezoidal (n=100)':<25} | {val_trap:<18.10f} | {err_trap:<15.4e}")
    print(f"{'Simpson 1/3 (n=100)':<25} | {val_simp:<18.10f} | {err_simp:<15.4e}")
    print(f"{'Gauss-Legendre (n=5)':<25} | {val_gauss_5:<18.10f} | {err_gauss_5:<15.4e}")
    print(f"{'Gauss-Legendre (n=10)':<25} | {val_gauss_10:<18.10f} | {err_gauss_10:<15.4e}")
    print(f"{'Gauss-Legendre (n=20)':<25} | {val_gauss_20:<18.10f} | {err_gauss_20:<15.4e}")
    print(f"{'Exact (Reference)':<25} | {exact_val:<18.10f} | {'-'*15}")
    print("-"*70)
    
    # ============================================
    # ۹. تحلیل خطاها
    # ============================================
    print("\n[+] Error Analysis:")
    print(f"    - Trapezoidal Error: {err_trap:.2e}")
    print(f"    - Simpson Error: {err_simp:.2e}")
    print(f"    - Gauss (n=5) Error: {err_gauss_5:.2e}")
    print(f"    - Gauss (n=10) Error: {err_gauss_10:.2e}")
    print(f"    - Gauss (n=20) Error: {err_gauss_20:.2e}")
    
    # محاسبه نسبت‌های خطا
    print(f"\n    - Simpson vs Trapezoidal: {err_trap/err_simp:.2f} times more accurate")
    print(f"    - Gauss (n=5) vs Simpson: {err_simp/err_gauss_5:.2f} times more accurate")
    print(f"    - Gauss (n=10) vs Gauss (n=5): {err_gauss_5/err_gauss_10:.2f} times more accurate")
    
    # ============================================
    # ۱۰. تولید جدول LaTeX برای گزارش
    # ============================================
    print("\n[+] LaTeX Table Code for Report:")
    latex_table = f"""
\\begin{{table}}[h!]
\\centering
\\caption{{مقایسه روش‌های انتگرال‌گیری عددی برای تابع $e^{{x^2}}$ در بازه $[0,1]$}}
\\begin{{tabular}}{{|l|c|c|}}
\\hline
\\textbf{{روش انتگرال‌گیری}} & \\textbf{{مقدار محاسبه شده}} & \\textbf{{خطای مطلق}} \\\\
\\hline
ذوزنقه‌ای (n=100) & {val_trap:.10f} & {err_trap:.4e} \\\\
سیمپسون 1/3 (n=100) & {val_simp:.10f} & {err_simp:.4e} \\\\
گاوس-لژاندر (n=5) & {val_gauss_5:.10f} & {err_gauss_5:.4e} \\\\
گاوس-لژاندر (n=10) & {val_gauss_10:.10f} & {err_gauss_10:.4e} \\\\
گاوس-لژاندر (n=20) & {val_gauss_20:.10f} & {err_gauss_20:.4e} \\\\
مقدار دقیق (مرجع) & {exact_val:.10f} & - \\\\
\\hline
\\end{{tabular}}
\\label{{tab:integration_results}}
\\end{{table}}
"""
    print(latex_table)
    
    # ============================================
    # ۱۱. رسم نمودار تابع
    # ============================================
    os.makedirs('../plots', exist_ok=True)
    
    x_plot = np.linspace(-0.2, 1.2, 200)
    y_plot = f(x_plot)
    
    plt.figure(figsize=(12, 7))
    
    # رسم تابع
    plt.plot(x_plot, y_plot, label='$f(x) = e^{x^2}$', color='purple', linewidth=3)
    
    # پر کردن ناحیه زیر منحنی
    x_fill = np.linspace(a, b, 200)
    y_fill = f(x_fill)
    plt.fill_between(x_fill, 0, y_fill, alpha=0.3, color='orange', label='Integration Region $[0, 1]$')
    
    # نشان دادن نقاط گاوس (n=5)
    x_gauss, w_gauss = np.polynomial.legendre.leggauss(5)
    x_gauss_transformed = 0.5 * (x_gauss + 1) * (b - a) + a
    y_gauss = f(x_gauss_transformed)
    plt.scatter(x_gauss_transformed, y_gauss, color='red', s=100, 
                label='Gauss Points (n=5)', zorder=5, edgecolors='black')
    
    plt.title('Visual Representation of $f(x) = e^{x^2}$ Integration', 
              fontsize=16, fontweight='bold')
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y', fontsize=14)
    plt.legend(fontsize=12, loc='best')
    plt.grid(True, alpha=0.3)
    
    # ذخیره نمودار
    plt.savefig('../plots/integration_plot.png', dpi=300, bbox_inches='tight')
    print("\n[✓] Plot saved to: ../plots/integration_plot.png")
    plt.close()
    
    # ============================================
    # ۱۲. محاسبه با sympy برای نمایش دقیق‌تر
    # ============================================
    x_sym = sp.Symbol('x')
    f_sym = sp.exp(x_sym**2)
    
    # انتگرال نامعین (برای نمایش)
    integral_indefinite = sp.integrate(f_sym, x_sym)
    print(f"\n[+] Indefinite Integral (Symbolic):")
    print(f"    ∫ e^(x²) dx = {integral_indefinite}")
    
    # انتگرال معین (برای نمایش)
    integral_definite = sp.integrate(f_sym, (x_sym, a, b))
    print(f"\n[+] Definite Integral (Symbolic):")
    print(f"    ∫₀¹ e^(x²) dx = {integral_definite}")
    print(f"    Numeric Value: {float(integral_definite):.10f}")
    
    print("\n" + "="*70)
    print("--- Task 3: Completed Successfully ---")
    print("="*70)
    
    return {
        'trapezoidal': val_trap,
        'simpson': val_simp,
        'gauss_5': val_gauss_5,
        'gauss_10': val_gauss_10,
        'gauss_20': val_gauss_20,
        'exact': exact_val,
        'errors': {
            'trapezoidal': err_trap,
            'simpson': err_simp,
            'gauss_5': err_gauss_5,
            'gauss_10': err_gauss_10,
            'gauss_20': err_gauss_20
        }
    }

if __name__ == "__main__":
    run_integration()