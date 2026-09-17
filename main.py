
import streamlit as st
import pandas as pd
import plotly.express as px


# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

# 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.caption(
    "1년간 박스오피스 10위권에 든 영화 중 "
    "해당 기간에 개봉한 영화들의 데이터"
)


# 데이터 주소
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)


# 데이터 불러오기
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv(DATA_URL)

    # 여러 장르가 있으면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("장르 미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
        .replace("", "장르 미상")
    )

    return df


try:
    df = load_data()

except Exception:
    st.error(
        "데이터를 불러오지 못했습니다. "
        "인터넷 연결과 데이터 주소를 확인해 주세요."
    )
    st.stop()


# ==================================================
# 그래프 1. 장르별 영화 편수
# ==================================================

st.subheader("그래프 1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="영화 편수")
)


# 플롯리 도넛 그래프
fig = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "장르: %{label}<br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    legend_title_text="장르"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# 그래프 설명 작성 자리
st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph1_note"
)

# ==================================================
# 그래프 2. 장르별 영화 트리맵
# ==================================================

st.divider()

st.subheader("그래프 2. 장르 안에 들어 있는 영화")

st.caption(
    "장르 안에 영화가 들어 있는 트리맵입니다. "
    "칸의 크기는 총 관객 수를 나타냅니다."
)


# 트리맵용 데이터
treemap_df = df[["genre", "movieNm", "total_audi"]].copy()

# 총 관객 수를 숫자로 변환
treemap_df["total_audi"] = pd.to_numeric(
    treemap_df["total_audi"],
    errors="coerce"
).fillna(0)


# 영화명이 비어 있는 경우 처리
treemap_df["movieNm"] = (
    treemap_df["movieNm"]
    .fillna("영화명 미상")
    .astype(str)
)


# 트리맵 그리기
fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객 트리맵",
    color="genre"
)


# 마우스를 올렸을 때 표시할 내용
fig2.update_traces(
    hovertemplate=(
        "영화명: %{label}<br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)


fig2.update_layout(
    margin=dict(t=50, l=10, r=10, b=10)
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# 그래프 설명 작성 자리
st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph2_note"
)
