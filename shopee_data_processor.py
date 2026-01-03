"""
Processor data khusus untuk format Shopee export
"""

import pandas as pd
import numpy as np
from datetime import datetime

class ShopeeDataProcessor:
    """Class untuk memproses data export Shopee"""
    
    def __init__(self):
        # Mapping kolom Shopee ke nama standar
        self.column_mapping = {
            # Kolom utama
            'Nama Iklan': 'Campaign',
            'Dilihat': 'Impressions',
            'Jumlah Klik': 'Clicks',
            'Konversi': 'Orders',
            'Omzet Penjualan': 'Sales',
            'Biaya': 'Spend',
            'Tanggal Mulai': 'Tanggal',
            
            # Kolom metrik
            'Persentase Klik': 'CTR',
            'Tingkat konversi': 'Conversion_Rate',
            'Efektifitas Iklan': 'ROAS',
            'Persentase Biaya Iklan terhadap Penjualan dari Iklan (ACOS)': 'ACOS',
            
            # Kolom tambahan untuk referensi
            'Status': 'Status_Iklan',
            'Kode Produk': 'Kode_Produk',
            'Mode Bidding': 'Mode_Bidding',
            'Penempatan Iklan': 'Penempatan_Iklan',
            'Tanggal Selesai': 'Tanggal_Selesai'
        }
        
        # Kolom yang perlu dibersihkan (numeric)
        self.numeric_columns = [
            'Dilihat', 'Jumlah Klik', 'Konversi', 'Konversi Langsung',
            'Omzet Penjualan', 'Penjualan Langsung (GMV Langsung)',
            'Biaya', 'Biaya per Konversi', 'Biaya per Konversi Langsung',
            'Produk Terjual', 'Terjual Langsung'
        ]
        
        # Kolom persentase
        self.percentage_columns = [
            'Persentase Klik', 'Tingkat konversi', 'Tingkat Konversi Langsung',
            'Persentase Biaya Iklan terhadap Penjualan dari Iklan (ACOS)',
            'Persentase Biaya Iklan terhadap Penjualan dari Iklan Langsung (ACOS Langsung)'
        ]
    
    def load_data(self, file_path):
        """Load data dari file CSV/Excel Shopee"""
        print(f"📂 Loading data from: {file_path}")
        
        try:
            # Deteksi format file
            if file_path.endswith('.csv'):
                # Coba berbagai delimiter
                try:
                    df = pd.read_csv(file_path, sep=',', encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                    except:
                        df = pd.read_csv(file_path, encoding='latin-1')
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Format file tidak didukung")
            
            print(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def clean_data(self, df):
        """Cleaning data Shopee"""
        print("\n🧹 Cleaning Shopee data...")
        
        df_clean = df.copy()
        
        # 1. Clean column names
        df_clean.columns = [col.strip() for col in df_clean.columns]
        
        # 2. Clean numeric columns (remove thousand separators)
        for col in self.numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str)
                df_clean[col] = df_clean[col].str.replace('.', '', regex=False)
                df_clean[col] = df_clean[col].str.replace(',', '.', regex=False)
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
                print(f"   ✅ Cleaned: {col}")
        
        # 3. Clean percentage columns
        for col in self.percentage_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str)
                df_clean[col] = df_clean[col].str.replace('%', '', regex=False)
                df_clean[col] = df_clean[col].str.replace(',', '.', regex=False)
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce') / 100
                print(f"   ✅ Cleaned: {col}")
        
        # 4. Clean date columns
        date_columns = ['Tanggal Mulai', 'Tanggal Selesai']
        for col in date_columns:
            if col in df_clean.columns:
                try:
                    df_clean[col] = pd.to_datetime(
                        df_clean[col], 
                        format='%d/%m/%Y %H:%M:%S',
                        errors='coerce'
                    )
                    print(f"   ✅ Parsed: {col}")
                except:
                    try:
                        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                    except:
                        print(f"   ⚠️ Could not parse: {col}")
        
        # 5. Apply column mapping
        for shopee_col, program_col in self.column_mapping.items():
            if shopee_col in df_clean.columns and program_col not in df_clean.columns:
                df_clean[program_col] = df_clean[shopee_col]
        
        print("✅ Data cleaning completed")
        return df_clean
    
    def calculate_additional_metrics(self, df):
        """Hitung metrik tambahan jika perlu"""
        print("\n🧮 Calculating additional metrics...")
        
        df_calc = df.copy()
        
        # Jika ROAS tidak ada, hitung dari Efektifitas Iklan
        if 'ROAS' not in df_calc.columns and 'Efektifitas Iklan' in df_calc.columns:
            df_calc['ROAS'] = df_calc['Efektifitas Iklan']
            print("   ✅ ROAS from Efektifitas Iklan")
        
        # Hitung ACOS jika tidak ada
        if 'ACOS' not in df_calc.columns and 'Sales' in df_calc.columns and 'Spend' in df_calc.columns:
            df_calc['ACOS'] = np.where(
                df_calc['Sales'] > 0,
                (df_calc['Spend'] / df_calc['Sales']) * 100,
                0
            )
            print("   ✅ Calculated ACOS")
        
        # Hitung CTR jika tidak ada
        if 'CTR' not in df_calc.columns and 'Impressions' in df_calc.columns and 'Clicks' in df_calc.columns:
            df_calc['CTR'] = np.where(
                df_calc['Impressions'] > 0,
                df_calc['Clicks'] / df_calc['Impressions'],
                0
            )
            print("   ✅ Calculated CTR")
        
        # Hitung Conversion Rate jika tidak ada
        if 'Conversion_Rate' not in df_calc.columns and 'Clicks' in df_calc.columns and 'Orders' in df_calc.columns:
            df_calc['Conversion_Rate'] = np.where(
                df_calc['Clicks'] > 0,
                df_calc['Orders'] / df_calc['Clicks'],
                0
            )
            print("   ✅ Calculated Conversion Rate")
        
        # Hitung CPC
        if 'Clicks' in df_calc.columns and 'Spend' in df_calc.columns:
            df_calc['CPC'] = np.where(
                df_calc['Clicks'] > 0,
                df_calc['Spend'] / df_calc['Clicks'],
                0
            )
            print("   ✅ Calculated CPC")
        
        # Hitung Profit
        if 'Sales' in df_calc.columns and 'Spend' in df_calc.columns:
            df_calc['Profit'] = df_calc['Sales'] - df_calc['Spend']
            df_calc['Profit_Margin'] = np.where(
                df_calc['Sales'] > 0,
                (df_calc['Profit'] / df_calc['Sales']) * 100,
                0
            )
            print("   ✅ Calculated Profit & Margin")
        
        return df_calc
    
    def get_campaign_summary(self, df):
        """Ringkasan performa per campaign"""
        if 'Campaign' not in df.columns:
            return pd.DataFrame()
        
        # Group by campaign
        summary = df.groupby('Campaign').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Orders': 'sum',
            'Sales': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        # Calculate metrics
        summary['CTR'] = np.where(
            summary['Impressions'] > 0,
            summary['Clicks'] / summary['Impressions'],
            0
        )
        
        summary['ROAS'] = np.where(
            summary['Spend'] > 0,
            summary['Sales'] / summary['Spend'],
            0
        )
        
        summary['CPC'] = np.where(
            summary['Clicks'] > 0,
            summary['Spend'] / summary['Clicks'],
            0
        )
        
        summary['Conversion_Rate'] = np.where(
            summary['Clicks'] > 0,
            summary['Orders'] / summary['Clicks'],
            0
        )
        
        summary['ACOS'] = np.where(
            summary['Sales'] > 0,
            (summary['Spend'] / summary['Sales']) * 100,
            0
        )
        
        summary['Profit'] = summary['Sales'] - summary['Spend']
        
        # Determine campaign status
        def get_status(row):
            if row['Spend'] == 0:
                return 'TIDAK AKTIF'
            elif row['ROAS'] < 0.5:
                return 'BONCOS ⚠️'
            elif row['ROAS'] < 1:
                return 'RUGI ❌'
            elif row['ROAS'] < 1.2:
                return 'BREAK EVEN ⚖️'
            elif row['ROAS'] < 2:
                return 'UNTUNG ✅'
            else:
                return 'UNTUNG TINGGI 🚀'
        
        summary['Status'] = summary.apply(get_status, axis=1)
        
        return summary
    
    def get_daily_summary(self, df):
        """Ringkasan performa harian"""
        if 'Tanggal' not in df.columns:
            return pd.DataFrame()
        
        # Group by date
        daily = df.groupby(df['Tanggal'].dt.date).agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Orders': 'sum',
            'Sales': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        # Calculate daily metrics
        daily['CTR'] = np.where(
            daily['Impressions'] > 0,
            daily['Clicks'] / daily['Impressions'],
            0
        )
        
        daily['ROAS'] = np.where(
            daily['Spend'] > 0,
            daily['Sales'] / daily['Spend'],
            0
        )
        
        daily['CPC'] = np.where(
            daily['Clicks'] > 0,
            daily['Spend'] / daily['Clicks'],
            0
        )
        
        return daily