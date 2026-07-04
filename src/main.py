#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
پروژه پایانی درس نرم‌افزار ریاضی
پیاده‌سازی، تحلیل و مقایسه روش‌های عددی در درون‌یابی، تحلیل داده‌ها و انتگرال‌گیری

نام دانشجو: امیررضا محمدپور
شماره دانشجویی: 40312041
استاد: حسینقلی‌زاده
نیمسال: دوم 1404-1405
"""

import sys
import os
from pathlib import Path

# اضافه کردن مسیر src به sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ایمپورت ماژول‌ها
from task1_interpolation import run_interpolation
from task2_analysis import run_analysis
from task3_integration import run_integration

def main():
    """اجرای همه بخش‌های پروژه"""
    
    print("\n" + "="*70)
    print(" "*20 + "NUMERICAL METHODS PROJECT")
    print("="*70)
    print("\nStudent: Amirreza Mohammadpour")
    print("Student ID: 40312041")
    print("Professor: Hosseingholizadeh")
    print("Semester: Spring 2025")
    print("="*70)
    
    # اجرای بخش 1
    run_interpolation()
    
    # اجرای بخش 2
    run_analysis()
    
    # اجرای بخش 3
    run_integration()
    
    print("\n" + "="*70)
    print(" "*25 + "PROJECT COMPLETED")
    print("="*70)
    print("\n[✓] All tasks executed successfully!")
    print("[✓] Results saved in '../plots/' directory")
    print("[✓] Check the report for detailed analysis")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()