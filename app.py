import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.font_manager as fm
import os

# =============================
# 폰트 설정 함수 (로컬 & 서버 공용)
# =============================
def set_korean_font():
    # 1. Streamlit Cloud(Linux) 환경을 위한 나눔 폰트 경로 설정
    linux_font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    
    if os.path.exists(linux_font_path):
        # 서버 환경: 설치된 나눔고딕 사용
        font_prop = fm.FontProperties(fname=linux_font_path)
        plt.rc('font', family=font_prop.get_name())
    else:
        # 로컬 환경: 윈도우 또는 맥 폰트 설정
        if platform.system() == 'Darwin': # 맥
            plt.rc('font', family='AppleGothic')
        elif platform.system() == 'Windows': # 윈도우
            plt.rc('font', family='Malgun Gothic')
            
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# 앱 기본 설정
st.set_page_config(page_title="국세청 근로소득 분석", layout="wide")
st.title("📂 국세청 근로소득 데이터 분석기")

# =============================
# 데이터 불러오기
# =============================
file_path = "data/국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try:
    # CSV 파일 읽기 (콤마 제거 포함)
    df = pd.read_csv(file_path, encoding="cp949", thousands=',')
    st.success("✅ 데이터를 성공적으로 불러왔습니다!")

    # =============================
    # 데이터 미리 보기 및 정보
    # =============================
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 데이터 요약")
        st.write(f"전체 행 수: **{df.shape[0]}** | 전체 열 수: **{df.shape[1]}**")
        st.dataframe(df.head(10))

    with col2:
        st.subheader("📋 데이터 기초 통계")
        st.write(df.describe())

    # =============================
    # 숫자형 컬럼 추출 및 시각화
    # =============================
    st.divider()
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if not numeric_cols:
        st.warning("⚠️ 분석할 수 있는 숫자형 데이터가 없습니다.")
    else:
        st.subheader("📈 데이터 분포 시각화")
        
        selected_col = st.selectbox("분석할 항목을 선택하세요:", options=numeric_cols)

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col], kde=True, ax=ax, color='skyblue')
        
        # 제목 및 라벨 설정
        ax.set_title(f"[{selected_col}] 분포도", fontsize=15)
        ax.set_xlabel(selected_col)
        ax.set_ylabel("빈도수")
        
        # 화면 출력
        st.pyplot(fig)

        # 상세 데이터 표
        with st.expander(f"📌 {selected_col} 상세 데이터 보기 (내림차순)"):
            st.write(df[[selected_col]].sort_values(by=selected_col, ascending=False))

except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다. 경로를 확인해주세요: {file_path}")
except Exception as e:
    st.error(f"❌ 오류 발생: {e}")