import os
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange, CubicSpline

def run_interpolation():
    print("\n" + "="*70)
    print("--- Task 1: Interpolation Started ---")
    print("="*70)
    
    # ایجاد پوشه plots در صورت عدم وجود
    os.makedirs('../plots', exist_ok=True)
    
    # ============================================
    # ۱. داده‌های اصلی (تصحیح شده مطابق صورت سوال)
    # ============================================
    # نقاط: (6,2), (5,5), (4,8), (3,5), (1,1), (2,3)
    points = [(6, 2), (5, 5), (4, 8), (3, 5), (1, 1), (2, 3)]
    
    # مرتب‌سازی بر اساس x برای رسم بهتر
    points_sorted = sorted(points, key=lambda p: p[0])
    x = np.array([p[0] for p in points_sorted])
    y = np.array([p[1] for p in points_sorted])
    
    print("\n[+] Data Points (Sorted):")
    for i, (xi, yi) in enumerate(zip(x, y)):
        print(f"    P{i+1}: ({xi}, {yi})")
    
    # ============================================
    # ۲. درون‌یابی لاگرانژ
    # ============================================
    poly_lagrange = lagrange(x, y)
    
    # استخراج ضابطه نمادین لاگرانژ با SymPy
    t = sp.Symbol('x')
    # تبدیل ضرایب لاگرانژ به چندجمله‌ای نمادین
    coeffs = poly_lagrange.coefficients
    lagrange_expr = sp.Poly(coeffs, t).as_expr()
    lagrange_expr_simplified = sp.simplify(lagrange_expr)
    
    print("\n[+] Lagrange Polynomial (Simplified):")
    print(f"    P(x) = {lagrange_expr_simplified}")
    
    # ============================================
    # ۳. درون‌یابی اسپلاین مکعبی (Cubic Spline)
    # ============================================
    cs = CubicSpline(x, y, bc_type='natural')  # اسپلاین طبیعی
    
    # استخراج ضابطه تکه‌ای اسپلاین به صورت نمادین
    print("\n[+] Cubic Spline Piecewise Function:")
    spline_pieces = []
    for i in range(len(x) - 1):
        coeffs = cs.c[:, i]
        # فرمول: a*(x - x_i)^3 + b*(x - x_i)^2 + c*(x - x_i) + d
        a, b, c, d = coeffs[0], coeffs[1], coeffs[2], coeffs[3]
        
        # ساخت عبارت نمادین برای هر تکه
        x_i = x[i]
        piece = (a * (t - x_i)**3 + 
                 b * (t - x_i)**2 + 
                 c * (t - x_i) + 
                 d)
        
        # ساده‌سازی
        piece_simplified = sp.simplify(piece)
        spline_pieces.append((x[i], x[i+1], piece_simplified))
        
        print(f"    S_{i}(x) = {piece_simplified},  for x ∈ [{x[i]}, {x[i+1]}]")
    
    # ساخت تابع تکه‌ای کامل با Piecewise
    piecewise_expr = sp.Piecewise(
        *[(piece, sp.And(t >= x[i], t <= x[i+1])) for i, (x_i, x_ip1, piece) in enumerate(spline_pieces)]
    )
    
    print("\n[+] Complete Piecewise Function (LaTeX format):")
    print(f"    {sp.latex(piecewise_expr)}")
    
    # ============================================
    # ۴. تولید نقاط بیشتر برای رسم نمودار نرم
    # ============================================
    x_dense = np.linspace(min(x), max(x), 300)
    
    # ============================================
    # ۵. رسم نمودار
    # ============================================
    plt.figure(figsize=(12, 7))
    
    # نقاط داده
    plt.scatter(x, y, color='red', s=100, label='Data Points', zorder=5, edgecolors='black')
    
    # لاگرانژ
    plt.plot(x_dense, poly_lagrange(x_dense), 
             label='Lagrange Polynomial (Degree 5)', 
             linestyle='--', color='blue', linewidth=2)
    
    # اسپلاین
    plt.plot(x_dense, cs(x_dense), 
             label='Cubic Spline (Natural)', 
             color='green', linewidth=2.5)
    
    plt.title('Interpolation: Lagrange vs Cubic Spline', fontsize=16, fontweight='bold')
    plt.xlabel('X Axis', fontsize=14)
    plt.ylabel('Y Axis', fontsize=14)
    plt.legend(fontsize=12, loc='best')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # ذخیره خودکار نمودار
    plot_path = '../plots/interpolation_plot.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\n[✓] Plot saved to: {plot_path}")
    plt.close()
    
    # ============================================
    # ۶. خروجی LaTeX برای گزارش
    # ============================================
    print("\n[+] LaTeX Code for Lagrange Polynomial:")
    print(f"    P(x) = {sp.latex(lagrange_expr_simplified)}")
    
    print("\n[+] LaTeX Code for Cubic Spline:")
    print(f"    {sp.latex(piecewise_expr)}")
    
    print("\n" + "="*70)
    print("--- Task 1: Completed Successfully ---")
    print("="*70)

if __name__ == "__main__":
    run_interpolation()