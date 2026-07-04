import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def run_analysis():
    print("\n" + "="*70)
    print("--- Task 2: Excel Data Analysis Started ---")
    print("="*70)
    
    # ایجاد پوشه plots
    os.makedirs('../plots', exist_ok=True)
    
    # ============================================
    # ۱. خواندن فایل اکسل
    # ============================================
    file_path = '../data/project_data.xlsx'
    
    # بررسی وجود فایل
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found!")
        print("Creating a sample file...")
        create_sample_data(file_path)
    
    # خواندن داده
    df = pd.read_excel(file_path)
    print("\n[+] Data loaded successfully:")
    print(df.to_string(index=False))
    
    # ============================================
    # ۲. افزودن داده 700KB (با حفظ توانایی به‌روزرسانی)
    # ============================================
    # بررسی اینکه آیا داده 700KB وجود دارد یا خیر
    if '700KB' not in df.iloc[:, 0].values:
        print("\n[+] Adding new data (700KB)...")
        new_data = pd.DataFrame({
            df.columns[0]: ['700KB'],
            df.columns[1]: [80],   # Alg.1
            df.columns[2]: [320],  # Alg.2
            df.columns[3]: [700]   # Alg.3
        })
        df = pd.concat([df, new_data], ignore_index=True)
        
        # ذخیره فایل با داده جدید
        df.to_excel(file_path, index=False)
        print("[✓] Data added and file updated successfully!")
    
    # ============================================
    # ۳. محاسبه میانگین الگوریتم 2
    # ============================================
    alg2_col = df.columns[2]  # ستون Alg.2
    # فقط داده‌های 100 تا 600 را در نظر می‌گیریم
    df_100_600 = df[df.iloc[:, 0] != '700KB']
    avg_alg2 = df_100_600[alg2_col].mean()
    
    print(f"\n[+] Average execution time for {alg2_col} (100-600KB): {avg_alg2:.2f} ms")
    
    # محاسبه آمار توصیفی کامل
    print(f"\n[+] Descriptive Statistics for {alg2_col}:")
    print(df_100_600[alg2_col].describe())
    
    # ============================================
    # ۴. آماده‌سازی داده برای رسم نمودار
    # ============================================
    # تنظیم ستون اول به عنوان ایندکس
    df_indexed = df.set_index(df.columns[0])
    
    # استخراج نام ستون‌های الگوریتم
    alg_cols = [col for col in df.columns if 'Alg' in col]
    
    # ============================================
    # ۵. رسم نمودار میله‌ای (Bar Chart)
    # ============================================
    fig, ax = plt.subplots(figsize=(12, 7))
    df_indexed[alg_cols].plot(kind='bar', ax=ax, width=0.7)
    
    ax.set_title('Algorithm Execution Time Comparison (Bar Chart)', 
                 fontsize=16, fontweight='bold')
    ax.set_ylabel('Execution Time (ms)', fontsize=14)
    ax.set_xlabel('Data Size', fontsize=14)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('../plots/alg_bar_chart.png', dpi=300, bbox_inches='tight')
    print("[✓] Bar chart saved to: ../plots/alg_bar_chart.png")
    plt.close()
    
    # ============================================
    # ۶. رسم نمودار خطی (Line Chart)
    # ============================================
    fig, ax = plt.subplots(figsize=(12, 7))
    df_indexed[alg_cols].plot(kind='line', marker='o', ax=ax, linewidth=2.5, markersize=8)
    
    ax.set_title('Algorithm Execution Time Trend (Line Chart)', 
                 fontsize=16, fontweight='bold')
    ax.set_ylabel('Execution Time (ms)', fontsize=14)
    ax.set_xlabel('Data Size', fontsize=14)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('../plots/alg_line_chart.png', dpi=300, bbox_inches='tight')
    print("[✓] Line chart saved to: ../plots/alg_line_chart.png")
    plt.close()
    
    # ============================================
    # ۷. رسم نمودار جعبه‌ای (Box Plot)
    # ============================================
    fig, ax = plt.subplots(figsize=(10, 7))
    df[alg_cols].boxplot(ax=ax, grid=True, patch_artist=True)
    
    ax.set_title('Distribution of Execution Times (Box Plot)', 
                 fontsize=16, fontweight='bold')
    ax.set_ylabel('Execution Time (ms)', fontsize=14)
    ax.set_xlabel('Algorithms', fontsize=14)
    plt.tight_layout()
    plt.savefig('../plots/alg_box_plot.png', dpi=300, bbox_inches='tight')
    print("[✓] Box plot saved to: ../plots/alg_box_plot.png")
    plt.close()
    
    # ============================================
    # ۸. رسم نمودار ترکیبی برای تحلیل بهتر
    # ============================================
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # نمودار خطی با تفکیک داده‌ها
    for col in alg_cols:
        axes[0].plot(df_indexed.index, df_indexed[col], 
                     marker='o', linewidth=2.5, markersize=8, label=col)
    axes[0].set_title('Execution Time vs Data Size', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Data Size', fontsize=12)
    axes[0].set_ylabel('Execution Time (ms)', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, linestyle=':', alpha=0.6)
    
    # نمودار جعبه‌ای
    df[alg_cols].boxplot(ax=axes[1], grid=True)
    axes[1].set_title('Algorithm Performance Distribution', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Execution Time (ms)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('../plots/alg_combined_analysis.png', dpi=300, bbox_inches='tight')
    print("[✓] Combined analysis plot saved to: ../plots/alg_combined_analysis.png")
    plt.close()
    
    # ============================================
    # ۹. تحلیل آماری کامل
    # ============================================
    print("\n[+] Statistical Analysis Report:")
    print("-"*50)
    print(f"Data Range: {df.iloc[:, 0].min()} to {df.iloc[:, 0].max()}")
    print(f"Number of Data Points: {len(df)}")
    print("\n[+] Algorithm Comparison:")
    
    for col in alg_cols:
        mean_val = df[col].mean()
        std_val = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()
        print(f"\n    {col}:")
        print(f"        Mean: {mean_val:.2f} ms")
        print(f"        Std Dev: {std_val:.2f} ms")
        print(f"        Min: {min_val:.2f} ms")
        print(f"        Max: {max_val:.2f} ms")
    
    print("\n" + "="*70)
    print("--- Task 2: Completed Successfully ---")
    print("="*70)
    
    return df, avg_alg2

def create_sample_data(file_path):
    """ایجاد داده نمونه در صورت عدم وجود فایل"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data = {
        'Data Size': ['100KB', '200KB', '300KB', '400KB', '500KB', '600KB'],
        'Alg.1': [50, 55, 60, 65, 70, 75],
        'Alg.2': [200, 220, 240, 260, 280, 300],
        'Alg.3': [100, 200, 300, 400, 500, 600]
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"[✓] Sample data created at: {file_path}")

if __name__ == "__main__":
    run_analysis()