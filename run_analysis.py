"""
Script utama untuk analisis iklan Shopee
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Import custom modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shopee_data_processor import ShopeeDataProcessor
from shopee_analyzer import ShopeeAdAnalyzer
from shopee_report_generator import ShopeeReportGenerator

def main():
    """Main function"""
    print("="*70)
    print("🚀 SHOPEE AD PERFORMANCE ANALYZER")
    print("📊 Customized for Your Shopee Export Format")
    print("="*70)
    
    # 1. Initialize components
    processor = ShopeeDataProcessor()
    analyzer = ShopeeAdAnalyzer(processor)
    report_generator = ShopeeReportGenerator()
    
    # 2. Get input file
    input_file = get_input_file()
    
    if not input_file:
        print("❌ No input file provided. Exiting.")
        return
    
    # 3. Load and process data
    print(f"\n📂 Processing: {input_file}")
    raw_data = processor.load_data(input_file)
    
    if raw_data is None or raw_data.empty:
        print("❌ No data to analyze")
        return
    
    # 4. Clean data
    cleaned_data = processor.clean_data(raw_data)
    
    # 5. Calculate metrics
    processed_data = processor.calculate_additional_metrics(cleaned_data)
    
    # 6. Get summaries
    campaign_summary = processor.get_campaign_summary(processed_data)
    daily_summary = processor.get_daily_summary(processed_data)
    
    # 7. Analyze campaigns
    analysis_results = analyzer.analyze_campaigns(campaign_summary)
    
    # 8. Display analysis
    display_analysis(analysis_results, campaign_summary)
    
    # 9. Get current time for planning
    now = datetime.now()
    current_hour = now.hour
    current_day = now.weekday() + 1  # Monday = 1
    
    print(f"\n📅 Analysis Date: {now.strftime('%Y-%m-%d')}")
    print(f"⏰ Current Time: {current_hour:02d}:00")
    print(f"📆 Day of Week: {current_day}")
    
    # 10. Generate daily and weekly plans
    analyzer.generate_daily_plan(current_hour)
    analyzer.generate_weekly_plan(current_day)
    
    # 11. Generate Excel report
    print("\n" + "="*70)
    print("💾 GENERATING COMPREHENSIVE REPORT")
    print("="*70)
    
    report_file = report_generator.generate_excel_report(
        raw_data=raw_data,
        cleaned_data=cleaned_data,
        analysis_results=analysis_results,
        campaign_summary=campaign_summary,
        daily_summary=daily_summary
    )
    
    # 12. Final summary
    print("\n" + "="*70)
    print("🎯 ANALYSIS COMPLETE!")
    print("="*70)
    
    print(f"\n📁 Report saved: {report_file}")
    print("\n📋 Sheets included:")
    print("1. Raw_Data - Data original dari Shopee")
    print("2. Cleaned_Data - Data yang sudah dibersihkan")
    print("3. Campaign_Analysis - Analisis detail per campaign")
    print("4. Campaign_Summary - Ringkasan performa")
    print("5. Daily_Summary - Performa harian")
    print("6. Recommendations - Rekomendasi tindakan")
    print("7. Strategy_Guide - Panduan strategi harian & mingguan")
    print("8. Performance_Dashboard - Dashboard performa")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Buka file Excel untuk melihat laporan lengkap")
    print("2. Cek sheet 'Recommendations' untuk tindakan prioritas")
    print("3. Ikuti 'Strategy_Guide' untuk pengelolaan optimal")
    print("4. Export data baru ke sheet 'Raw_Data' dan jalankan ulang")
    
    # Wait for user input (Windows)
    if os.name == 'nt':
        input("\nPress Enter to exit...")

def get_input_file():
    """Get input file from user or auto-detect"""
    # Auto-detect common file names
    common_files = [
        'data_shopee.csv',
        'shopee_data.csv',
        'shopee_export.csv',
        'export.csv',
        'data.csv',
        'shopee_ready.csv',
        'shopee_converted.csv'
    ]
    
    for file in common_files:
        if os.path.exists(file):
            return file
    
    # If not found, ask user
    print("\n📁 Auto-detection: No common file found")
    user_input = input("Enter Shopee export file path: ").strip()
    
    if user_input and os.path.exists(user_input):
        return user_input
    
    return None

def display_analysis(analysis_results, campaign_summary):
    """Display analysis results in console"""
    print("\n" + "="*70)
    print("📊 PERFORMANCE ANALYSIS RESULTS")
    print("="*70)
    
    # Overall summary
    total_spend = campaign_summary['Spend'].sum()
    total_sales = campaign_summary['Sales'].sum()
    total_profit = campaign_summary['Profit'].sum()
    avg_roas = campaign_summary['ROAS'].mean()
    
    print(f"\n📈 OVERALL SUMMARY:")
    print(f"   Total Campaigns: {len(campaign_summary)}")
    print(f"   Total Spend: Rp {total_spend:,.0f}")
    print(f"   Total Sales: Rp {total_sales:,.0f}")
    print(f"   Total Profit: Rp {total_profit:,.0f}")
    print(f"   Average ROAS: {avg_roas:.2f}")
    
    # Campaign details
    print(f"\n🏆 CAMPAIGN DETAILS:")
    for _, row in analysis_results.iterrows():
        print(f"\n📌 {row['Campaign'][:40]}...")
        print(f"   Status: {row['Status']}")
        print(f"   ROAS: {row['ROAS']} | CTR: {row['CTR']} | ACOS: {row['ACOS']}")
        print(f"   Spend: {row['Spend']} | Sales: {row['Sales']} | Profit: {row['Profit']}")
        print(f"   Score: {row['Performance_Score']}/100 | Priority: {row['Priority']}")
        print(f"   Action: {row['Recommendations']}")
    
    # Priority actions
    print(f"\n🎯 PRIORITY ACTIONS:")
    high_priority = analysis_results[analysis_results['Priority'] == 'HIGH']
    medium_priority = analysis_results[analysis_results['Priority'] == 'MEDIUM']
    
    if not high_priority.empty:
        print(f"\n🔴 HIGH PRIORITY ({len(high_priority)} campaign):")
        for _, row in high_priority.iterrows():
            print(f"   • {row['Campaign'][:30]}...: {row['Recommendations']}")
    
    if not medium_priority.empty:
        print(f"\n🟡 MEDIUM PRIORITY ({len(medium_priority)} campaign):")
        for _, row in medium_priority.iterrows():
            print(f"   • {row['Campaign'][:30]}...: {row['Recommendations']}")

if __name__ == "__main__":
    main()