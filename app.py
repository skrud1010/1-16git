import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 한글 폰트 설정 (환경에 따라 다름)
def set_korean_font():
    if platform.system() == 'Darwin': # 맥
        plt.rc('font', family='AppleGothic')
    elif platform.system() == 'Windows': # 윈도우
        plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.set_page_config(page_title="국세청 근로소득 분석", layout="wide")
st.title("📂 국세청 근로소득 데이터 분석기")

# =============================
# 데이터 불러오기
# =============================
file_path = "data/국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try:
    # 1️⃣ CSV 파일 읽기
    # 데이터에 콤마(,)가 포함된 숫자가 있을 수 있으므로 thousands=',' 옵션을 추가하면 편리합니다.
    df = pd.read_csv(file_path, encoding="cp949", thousands=',')
    st.success("✅ 데이터를 성공적으로 불러왔습니다!")

    # =============================
    # 데이터 미리 보기 및 정보
    # =============================
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 데이터 요약")
        st.write(f"전체 행 수: {df.shape[0]} | 전체 열 수: {df.shape[1]}")
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
        
        # 2️⃣ Selectbox 수정: options 인자 전달
        selected_col = st.selectbox("분석할 항목을 선택하세요:", options=numeric_cols)

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col], kde=True, ax=ax, color='skyblue')
        plt.title(f"[{selected_col}] 분포도")
        plt.xlabel(selected_col)
        plt.ylabel("빈도수")
        
        st.pyplot(fig)

        # 상세 데이터 표
        with st.expander("선택한 항목 상세 데이터 보기"):
            st.write(df[[selected_col]].sort_values(by=selected_col, ascending=False))

except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다. 경로를 확인해주세요: {file_path}")
except Exception as e:
    st.error(f"❌ 오류 발생: {e}")