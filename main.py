
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

# ==================================================
# 그래프 3. 총 관객 수의 분포
# ==================================================

st.divider()

st.subheader("그래프 3. 영화별 총 관객 수 분포")

st.caption(
    "영화별 total_audi(총 관객)가 "
    "어느 구간에 많이 몰려 있는지 보여 주는 히스토그램입니다."
)


# 총 관객 수를 숫자로 변환
hist_df = df[["movieNm", "total_audi"]].copy()

hist_df["total_audi"] = pd.to_numeric(
    hist_df["total_audi"],
    errors="coerce"
)

hist_df = hist_df.dropna(subset=["total_audi"])


# 히스토그램 그리기
fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)


fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)


fig3.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=50, l=10, r=10, b=10)
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


# ==================================================
# 그래프 3 아래 설명 문구
# ==================================================

# 가장 관객이 많은 영화 찾기
max_audience_row = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

max_movie_name = max_audience_row["movieNm"]
max_audience = max_audience_row["total_audi"]


# 가장 많은 영화가 속한 관객 구간 찾기
hist_counts, bin_edges = pd.cut(
    hist_df["total_audi"],
    bins=20,
    include_lowest=True,
    retbins=True
)

most_common_bin = hist_counts.value_counts().idxmax()

bin_start = most_common_bin.left
bin_end = most_common_bin.right


st.markdown("**이 그래프로 알 수 있는 것**")

st.info(
    f"대부분의 영화는 총 관객 약 "
    f"{bin_start:,.0f}명 ~ {bin_end:,.0f}명 "
    f"구간에 몰려 있습니다."
)

st.info(
    f"가장 관객이 많은 영화는 "
    f"**{max_movie_name}**이며, "
    f"총 관객은 **{max_audience:,.0f}명**입니다."
)


# 직접 작성할 수 있는 설명 자리
st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph3_note"
)

# ==================================================
# 그래프 4. 개봉일 스크린수와 총 관객의 관계
# ==================================================

st.divider()

st.subheader("그래프 4. 개봉일 스크린수와 총 관객의 관계")

st.caption(
    "개봉일 스크린수와 총 관객 사이의 관계를 "
    "장르별 색으로 구분한 산점도입니다."
)


# 산점도용 데이터
scatter_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi"]
].copy()


# 숫자로 변환
scatter_df["first_scrn"] = pd.to_numeric(
    scatter_df["first_scrn"],
    errors="coerce"
)

scatter_df["total_audi"] = pd.to_numeric(
    scatter_df["total_audi"],
    errors="coerce"
)


# 결측값 제거
scatter_df = scatter_df.dropna(
    subset=["movieNm", "genre", "first_scrn", "total_audi"]
)


# 산점도 그리기
fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    }
)


# 마우스를 올렸을 때 영화명 표시
fig4.update_traces(
    hovertemplate=(
        "영화명: %{hovertext}<br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(
        size=10,
        opacity=0.75
    )
)


fig4.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    margin=dict(t=50, l=10, r=10, b=10)
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# 그래프 설명 작성 자리
st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph4_note"
)
