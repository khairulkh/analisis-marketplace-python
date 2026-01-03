"""
Analisis performa iklan Shopee dengan strategi khusus
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ShopeeAdAnalyzer:
    """Class untuk analisis iklan Shopee"""
    
    def __init__(self, processor):
        self.processor = processor
        self.raw_data = None
        self.cleaned_data = None
        self.campaign_summary = None
        
    def analyze_campaigns(self, df):
        """Analisis mendalam semua campaign"""
        print("\n" + "="*60)
        print("📊 DETAILED CAMPAIGN ANALYSIS")
        print("="*60)
        
        analysis_results = []
        
        for _, campaign in df.iterrows():
            campaign_name = campaign['Campaign']
            roas = campaign.get('ROAS', 0)
            ctr = campaign.get('CTR', 0)
            acos = campaign.get('ACOS', 0)
            spend = campaign.get('Spend', 0)
            sales = campaign.get('Sales', 0)
            
            # Status berdasarkan ROAS
            if spend == 0:
                status = 'TIDAK AKTIF'
                priority = 'MEDIUM'
            elif roas < 0.5:
                status = 'BONCOS'
                priority = 'HIGH'
            elif roas < 1:
                status = 'RUGI'
                priority = 'HIGH'
            elif roas < 1.2:
                status = 'BREAK EVEN'
                priority = 'MEDIUM'
            elif roas < 2:
                status = 'UNTUNG'
                priority = 'LOW'
            else:
                status = 'UNTUNG TINGGI'
                priority = 'LOW'
            
            # Rekomendasi berdasarkan status
            recommendations = self._get_recommendations(status, roas, ctr, acos, spend, sales)
            
            # Score performa (0-100)
            score = self._calculate_performance_score(roas, ctr, acos)
            
            analysis_results.append({
                'Campaign': campaign_name,
                'Status': status,
                'ROAS': roas,
                'CTR': f"{ctr*100:.2f}%",
                'ACOS': f"{acos:.2f}%",
                'Spend': f"Rp {spend:,.0f}",
                'Sales': f"Rp {sales:,.0f}",
                'Profit': f"Rp {sales - spend:,.0f}",
                'Performance_Score': score,
                'Priority': priority,
                'Recommendations': recommendations['action'],
                'Budget_Advice': recommendations['budget'],
                'Focus_Area': recommendations['focus']
            })
        
        return pd.DataFrame(analysis_results)
    
    def _get_recommendations(self, status, roas, ctr, acos, spend, sales):
        """Beri rekomendasi berdasarkan performa"""
        recommendations = {
            'TIDAK AKTIF': {
                'action': 'Aktifkan dengan budget testing Rp 50-100k',
                'budget': 'Rp 50.000 - 100.000',
                'focus': 'Aktivasi campaign'
            },
            'BONCOS': {
                'action': 'HENTIKAN SEMENTARA! ROAS < 0.5. Revisi total creatives & targeting',
                'budget': 'Turunkan 50% atau PAUSE',
                'focus': 'Total Revamp'
            },
            'RUGI': {
                'action': 'Optimasi mendesak: turunkan bid, revisi creatives, tambah negative keywords',
                'budget': 'Turunkan 20-30%',
                'focus': 'Bid & Creative Optimization'
            },
            'BREAK EVEN': {
                'action': 'Pertahankan, bisa naikkan budget 10-20% secara bertahap',
                'budget': 'Naikkan 10-20%',
                'focus': 'Budget Scaling'
            },
            'UNTUNG': {
                'action': 'Scale up: naikkan budget 20-30%, ekspansi keyword',
                'budget': 'Naikkan 20-30%',
                'focus': 'Budget Expansion'
            },
            'UNTUNG TINGGI': {
                'action': 'MAXIMIZE! Naikkan budget 50-100%, duplikat campaign, ekspansi produk',
                'budget': 'Naikkan 50-100%',
                'focus': 'Aggressive Expansion'
            }
        }
        
        return recommendations.get(status, {
            'action': 'Monitor performa',
            'budget': 'Pertahankan',
            'focus': 'Monitoring'
        })
    
    def _calculate_performance_score(self, roas, ctr, acos):
        """Hitung score performa (0-100)"""
        score = 0
        
        # ROAS score (max 40)
        if roas >= 2:
            score += 40
        elif roas >= 1.5:
            score += 35
        elif roas >= 1.2:
            score += 30
        elif roas >= 1:
            score += 20
        elif roas >= 0.5:
            score += 10
        else:
            score += 0
        
        # CTR score (max 30)
        if ctr >= 0.03:  # 3%
            score += 30
        elif ctr >= 0.025:  # 2.5%
            score += 25
        elif ctr >= 0.02:  # 2%
            score += 20
        elif ctr >= 0.015:  # 1.5%
            score += 15
        elif ctr >= 0.01:  # 1%
            score += 10
        else:
            score += 5
        
        # ACOS score (max 30)
        if acos <= 10:  # ACOS ≤ 10%
            score += 30
        elif acos <= 15:  # ACOS ≤ 15%
            score += 25
        elif acos <= 20:  # ACOS ≤ 20%
            score += 20
        elif acos <= 30:  # ACOS ≤ 30%
            score += 15
        elif acos <= 40:  # ACOS ≤ 40%
            score += 10
        else:
            score += 5
        
        return min(score, 100)
    
    def generate_daily_plan(self, current_hour):
        """Generate daily plan berdasarkan waktu"""
        print("\n" + "="*60)
        print("⏰ DAILY MANAGEMENT PLAN")
        print("="*60)
        
        plans = {
            'morning': {
                'hours': (7, 9),
                'title': '🌅 PAGI (07:00-09:00)',
                'actions': [
                    'Boleh ubah ROAS & budget setting',
                    'Shopee mulai push iklan hari ini',
                    'Evaluasi performa kemarin',
                    'Set target untuk hari ini'
                ]
            },
            'noon': {
                'hours': (12, 13),
                'title': '☀️ SIANG (12:00-13:00)',
                'actions': [
                    'Cek CTR & klik sementara',
                    'Pantau apakah budget terserap',
                    'Jangan ubah setting besar',
                    'Catat observasi untuk evaluasi malam'
                ]
            },
            'evening': {
                'hours': (20, 22),
                'title': '🌙 MALAM (20:00-22:00)',
                'actions': [
                    'Evaluasi performa harian lengkap',
                    'Analisis ROAS, konversi, biaya',
                    'Bandingkan dengan target',
                    'Siapkan action untuk besok'
                ]
            },
            'midnight': {
                'hours': (0, 1),
                'title': '🌌 TENGAH MALAM (00:00-01:00)',
                'actions': [
                    'JANGAN ubah setting apapun!',
                    'Shopee sedang reset learning phase',
                    'Biarkan sistem menentukan performa besok',
                    'Istirahat, lanjut besok pagi'
                ]
            }
        }
        
        current_plan = None
        for period, info in plans.items():
            if info['hours'][0] <= current_hour < info['hours'][1]:
                current_plan = info
                break
        
        if current_plan:
            print(f"\n{current_plan['title']}")
            for action in current_plan['actions']:
                print(f"• {action}")
        else:
            print("\n⏳ Diluar jam optimal pengelolaan:")
            print("• Monitor saja performa")
            print("• Hindari perubahan setting")
            print("• Catat observasi untuk evaluasi")
        
        return current_plan
    
    def generate_weekly_plan(self, day_of_week):
        """Generate weekly plan berdasarkan hari"""
        print("\n" + "="*60)
        print("📅 WEEKLY MANAGEMENT RHYTHM")
        print("="*60)
        
        weekly_plans = {
            1: {  # Monday
                'day': 'HARI 1 (Senin)',
                'focus': 'Evaluasi data weekend',
                'actions': [
                    'Analisis performa Sabtu-Minggu',
                    'Lihat tren klik, ROAS, penjualan',
                    'Identifikasi pattern performa',
                    'Siapkan plan untuk minggu ini'
                ]
            },
            2: {  # Tuesday
                'day': 'HARI 2 (Selasa)',
                'focus': 'Pantau konsistensi',
                'actions': [
                    'Monitor performa campaign',
                    'Jangan langsung ubah setting',
                    'Observasi konsistensi performa',
                    'Catat pattern yang muncul'
                ]
            },
            3: {  # Wednesday
                'day': 'HARI 3 (Rabu)',
                'focus': 'Eksekusi Scale Up/Down',
                'actions': [
                    'Naikkan budget 20-30% untuk campaign yang ready',
                    'Turunkan budget untuk campaign rugi',
                    'Expect ROAS turun pelan (normal)',
                    'Jangan takut dengan fluktuasi'
                ]
            },
            4: {  # Thursday
                'day': 'HARI 4 (Kamis)',
                'focus': 'Biarkan sistem belajar',
                'actions': [
                    'JANGAN otak-atik iklan!',
                    'Biarkan algoritma Shopee belajar',
                    'Monitor saja tanpa perubahan',
                    'Observasi hasil dari perubahan kemarin'
                ]
            },
            5: {  # Friday
                'day': 'HARI 5 (Jumat)',
                'focus': 'Evaluasi hasil scale',
                'actions': [
                    'Evaluasi hasil scale up/down',
                    'Jika bagus: lanjutkan strategy',
                    'Jika drop: rollback ke setting lama',
                    'Siapkan untuk weekend'
                ]
            },
            6: {  # Saturday
                'day': 'HARI 6 (Sabtu)',
                'focus': 'Maintenance & Testing',
                'actions': [
                    'Maintenance campaign yang stabil',
                    'Split testing untuk campaign eksperimen',
                    'Testing kreatif baru',
                    'Analisis performa weekend'
                ]
            },
            7: {  # Sunday
                'day': 'HARI 7 (Minggu)',
                'focus': 'Review & Planning',
                'actions': [
                    'Review performa minggu ini',
                    'Plan untuk minggu depan',
                    'Duplikat campaign yang sukses',
                    'Siapkan testing untuk minggu depan'
                ]
            }
        }
        
        plan = weekly_plans.get(day_of_week, {
            'day': f'HARI {day_of_week}',
            'focus': 'Monitor performa',
            'actions': ['Monitor campaign performa']
        })
        
        print(f"\n{plan['day']}: {plan['focus']}")
        for action in plan['actions']:
            print(f"• {action}")
        
        return plan