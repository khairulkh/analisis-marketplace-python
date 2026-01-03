"""
Konfigurasi untuk Shopee Analyzer
"""

# Strategi Pengelolaan Iklan
DAILY_SCHEDULE = {
    'morning': {'start': 7, 'end': 9, 'action': 'adjust_roas_budget'},
    'noon': {'start': 12, 'end': 13, 'action': 'monitor_ctr_spend'},
    'evening': {'start': 20, 'end': 22, 'action': 'daily_evaluation'},
    'midnight': {'start': 0, 'end': 1, 'action': 'learning_reset'}
}

WEEKLY_RHYTHM = {
    1: {'action': 'evaluate_yesterday', 'focus': 'Weekend performance analysis'},
    2: {'action': 'monitor_consistency', 'focus': 'Observe without changes'},
    3: {'action': 'execute_scale', 'focus': 'Scale up/down campaigns'},
    4: {'action': 'let_system_learn', 'focus': 'No changes allowed'},
    5: {'action': 'evaluate_scale', 'focus': 'Review scale results'},
    6: {'action': 'maintenance_testing', 'focus': 'Split testing'},
    7: {'action': 'review_planning', 'focus': 'Weekly review'}
}

# Kriteria Performa
PERFORMANCE_THRESHOLDS = {
    'ROAS_EXCELLENT': 2.0,
    'ROAS_GOOD': 1.5,
    'ROAS_BREAK_EVEN': 1.2,
    'ROAS_MINIMUM': 1.0,
    'ROAS_CRITICAL': 0.5,
    
    'CTR_EXCELLENT': 0.03,      # 3%
    'CTR_GOOD': 0.025,          # 2.5%
    'CTR_AVERAGE': 0.02,        # 2%
    'CTR_POOR': 0.01,           # 1%
    
    'ACOS_EXCELLENT': 0.10,     # 10%
    'ACOS_GOOD': 0.15,          # 15%
    'ACOS_AVERAGE': 0.20,       # 20%
    'ACOS_POOR': 0.30,          # 30%
    
    'CONVERSION_EXCELLENT': 0.08,   # 8%
    'CONVERSION_GOOD': 0.05,        # 5%
    'CONVERSION_AVERAGE': 0.03,     # 3%
    'CONVERSION_POOR': 0.01         # 1%
}

# Kriteria Scale Up
SCALE_UP_CRITERIA = {
    'sales_increase': 0.15,      # 15% increase
    'revenue_increase': 0.20,    # 20% increase
    'clicks_increase': 0.20,     # 20% increase
    'ctr_minimum': 0.025,        # 2.5% minimum
    'roas_minimum': 1.2,         # ROAS > 1.2
    'budget_absorption': 0.70,   # >70% budget used
    'consecutive_days': 2        # 2 consecutive days
}

# Rekomendasi Budget
BUDGET_RECOMMENDATIONS = {
    'BONCOS': {'action': 'DECREASE', 'percentage': 50, 'advice': 'Turunkan 50% atau PAUSE'},
    'RUGI': {'action': 'DECREASE', 'percentage': 30, 'advice': 'Turunkan 20-30%'},
    'BREAK_EVEN': {'action': 'INCREASE', 'percentage': 20, 'advice': 'Naikkan 10-20%'},
    'UNTUNG': {'action': 'INCREASE', 'percentage': 30, 'advice': 'Naikkan 20-30%'},
    'UNTUNG TINGGI': {'action': 'INCREASE', 'percentage': 50, 'advice': 'Naikkan 50-100%'}
}

# Kolom Wajib Shopee
SHOPEE_REQUIRED_COLUMNS = [
    'Nama Iklan',
    'Dilihat',
    'Jumlah Klik',
    'Konversi',
    'Omzet Penjualan',
    'Biaya',
    'Tanggal Mulai'
]

# Format Tanggal Shopee
SHOPEE_DATE_FORMATS = [
    '%d/%m/%Y %H:%M:%S',
    '%d/%m/%Y %H.%M.%S',
    '%d/%m/%Y %H:%M',
    '%d/%m/%Y %H.%M'
]