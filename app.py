import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.font_manager as fm
import os

# =============================
# 글꼴 파일 경로 설정 (이미지 구조 반영)
# =============================
def set_korean_font():
    # 현재 실행 중인 app.py와 같은 폴더에 있는 NanumGothic.ttf 경로 탐색
    font_file = "NanumGothic.ttf"
    
    if os.path.exists(font_file):
        # 1. 파일이 있으면 직접 해당 폰트 등록
        font_prop = fm.FontProperties(fname=font_file)
        plt.rc('font', family=font_prop.get_name())
        # Streamlit용 폰트 정보 저장
        st.session_state['font_name'] = font_prop.get_name()
    else:
        # 2. 파일이 없을 경우 로컬 시스템 폰트 사용 (예외 처리)
        if platform.system() == 'Darwin':
            plt.rc('font', family='AppleGothic')
        elif platform.system() == 'Windows':
            plt.rc('font', family='Malgun Gothic')
            
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.set_page_config(page_title="국세청 근로소득 분석", layout="wide")
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