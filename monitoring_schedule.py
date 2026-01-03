"""
Jadwal monitoring iklan berdasarkan waktu pemasangan
"""

from datetime import datetime, timedelta

def get_monitoring_schedule(start_time):
    """
    Generate jadwal monitoring berdasarkan waktu mulai
    """
    
    schedule = []
    
    # Hari 0 (Hari pemasangan)
    if start_time.hour >= 21:  # Jika pasang malam
        schedule.append({
            'time': 'HARI 0 (Sekarang)',
            'action': 'PASANG IKLAN',
            'check': 'Pastikan iklan aktif',
            'do_not': 'JANGAN ubah setting apapun!'
        })
        
        schedule.append({
            'time': '00:00-01:00',
            'action': 'SYSTEM RESET',
            'check': 'Shopee reset learning phase',
            'do_not': 'TIDAK BOLEH analisis atau ubah setting'
        })
    
    # Hari 1
    schedule.append({
        'time': 'HARI 1 (07:00-09:00)',
        'action': 'ANALISIS PERTAMA',
        'check': ['Impressions > 0?', 'Iklan live?', 'Budget mulai terserap?'],
        'action_if_good': 'Biarkan jalan',
        'action_if_bad': 'Optimasi creatives/judul'
    })
    
    schedule.append({
        'time': 'HARI 1 (12:00-13:00)',
        'action': 'CEK PERFORMANCE SEMENTARA',
        'check': ['CTR berapa?', 'Ada klik?', 'Budget absorption?'],
        'action_if_good': 'Monitor saja',
        'action_if_bad': 'Catat untuk evaluasi malam'
    })
    
    schedule.append({
        'time': 'HARI 1 (20:00-22:00)',
        'action': 'EVALUASI HARIAN PERTAMA',
        'check': ['Total impressions', 'Total clicks', 'CTR akhir', 'Ada konversi?'],
        'metrics': 'Hitung: CTR, CPC, Budget usage',
        'decision': 'Pertahankan atau optimasi besok'
    })
    
    # Hari 2
    schedule.append({
        'time': 'HARI 2 (07:00-09:00)',
        'action': 'EVALUASI KONSISTENSI',
        'check': ['Perform sama/turun/naik?', 'Ada pattern?'],
        'action_if_consistent': 'Biarkan, monitor',
        'action_if_drop': 'Investigasi penyebab'
    })
    
    schedule.append({
        'time': 'HARI 2 (20:00-22:00)',
        'action': 'ANALISIS 48 JAM',
        'check': ['Total konversi?', 'ROAS awal?', 'Conversion rate?'],
        'metrics': 'Hitung: ROAS, Conversion Rate, ACOS',
        'decision': 'Scale up/down besok pagi'
    })
    
    # Hari 3
    schedule.append({
        'time': 'HARI 3 (07:00-09:00)',
        'action': 'EXECUTE SCALE UP/DOWN',
        'check': 'Berdasarkan analisis 48 jam',
        'scale_up_if': 'ROAS > 1.2 & CTR > 2%',
        'scale_down_if': 'ROAS < 0.8 & CTR < 1%',
        'budget_change': '20-30% naik/turun'
    })
    
    # Hari 7
    schedule.append({
        'time': 'HARI 7',
        'action': 'ANALISIS KOMPREHENSIF',
        'check': ['ROAS 7-hari', 'CTR average', 'Total konversi', 'Total profit'],
        'decision': 'Lanjutkan, stop, atau major optimization'
    })
    
    return schedule

def print_schedule(schedule):
    """Print jadwal monitoring"""
    print("="*70)
    print("📅 JADWAL MONITORING & ANALISIS IKLAN SHOPEE")
    print("="*70)
    
    for item in schedule:
        print(f"\n⏰ {item['time']}")
        print(f"🎯 {item['action']}")
        
        if 'check' in item:
            if isinstance(item['check'], list):
                for check_item in item['check']:
                    print(f"   ✓ {check_item}")
            else:
                print(f"   ✓ {item['check']}")
        
        if 'action_if_good' in item:
            print(f"   📈 Jika baik: {item['action_if_good']}")
        
        if 'action_if_bad' in item:
            print(f"   📉 Jika buruk: {item['action_if_bad']}")
        
        if 'metrics' in item:
            print(f"   🧮 Metrics: {item['metrics']}")
        
        if 'decision' in item:
            print(f"   🤔 Decision: {item['decision']}")

# Generate schedule untuk iklan yang dipasang sekarang
now = datetime.now()
schedule = get_monitoring_schedule(now)

print_schedule(schedule)

print("\n" + "="*70)
print("📌 KESIMPULAN:")
print("="*70)
print("1. Analisis pertama: BESOK PAGI (07:00-09:00)")
print("2. Analisis bermakna: SETELAH 48 JAM")
print("3. Analisis komprehensif: SETELAH 7 HARI")
print("4. JANGAN analisis: MALAM INI (00:00-01:00)")
print("="*70)