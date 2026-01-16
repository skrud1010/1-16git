import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.font_manager as fm
import os

# -----------------------------------------------------------------------------------
# 한글 폰트 설정 (더 강력한 버전)
# -----------------------------------------------------------------------------------
system_name = platform.system()

if system_name == 'Windows':
    # 윈도우
    plt.rc('font', family='Malgun Gothic') 
elif system_name == 'Darwin':
    # 맥
    plt.rc('font', family='AppleGothic') 
else:
    # 리눅스 (Streamlit Cloud)
    # 폰트 파일 경로 지정
    path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    
    # 해당 경로에 폰트 파일이 있는지 확인
    if os.path.exists(path):
        # 1. 폰트 매니저에 폰트 추가 (이게 핵심!)
        fm.fontManager.addfont(path)
        
        # 2. 추가된 폰트의 이름을 가져와서 설정
        font_name = fm.FontProperties(fname=path).get_name()
        plt.rc('font', family=font_name)
    else:
        # 폰트가 설치되지 않았을 경우 에러 메시지 출력 (디버깅용)
        st.error("⚠️ 한글 폰트 파일이 없습니다. packages.txt를 확인해주세요.")

plt.rc('axes', unicode_minus=False) # 마이너스 기호 깨짐 방지
st.title("📂 국세청 근로소득 데이터 분석기")

# =============================
# 데이터 불러오기 (이미지의 load_data 로직 반영)
# =============================
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

def load_data(path):
    encodings = ['utf-8-sig', 'cp949', 'euc-kr', 'utf-8']
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, thousands=',')
            df.columns = df.columns.str.strip() # 컬럼명 공백 제거
            return df, enc
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    return None, None

try:
    df, used_encoding = load_data(file_path)

    if df is not None:
        st.success(f"✅ 데이터를 성공적으로 불러왔습니다! (인코딩: {used_encoding})")

        # 상단 요약 정보
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 데이터 요약")
            st.dataframe(df.head(10))
        with col2:
            st.subheader("📋 기초 통계")
            st.write(df.describe())

        # 시각화 섹션
        st.divider()
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

        if numeric_cols:
            st.subheader("📈 데이터 분포 시각화")
            selected_col = st.selectbox("분석할 항목을 선택하세요:", options=numeric_cols)

            # 그래프 생성
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df[selected_col], kde=True, ax=ax, color='skyblue')
            
            # 그래프 내 한글 적용 확인용 설정
            ax.set_title(f"[{selected_col}] 분포도", fontsize=16)
            ax.set_xlabel(selected_col)
            ax.set_ylabel("빈도수")
            
            st.pyplot(fig)
            
            with st.expander("상세 데이터 보기"):
                st.write(df[[selected_col]].sort_values(by=selected_col, ascending=False))
        else:
            st.warning("분석할 숫자형 데이터가 없습니다.")
            
    else:
        st.error(f"❌ 파일을 불러올 수 없습니다. 경로를 확인하세요: {file_path}")

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")