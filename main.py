import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

# 제목 및 설명
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

# 데이터 불러오기 함수
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르 처리 (여러 개가 있으면 첫 번째 장르만 추출)
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
# 그래프 1. 장르별 영화 편수 (도넛 그래프)
# ==================================================

st.subheader("그래프 1. 장르별 영화 편수")

# 장르별 편수 집계
genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="영화 편수")
)

# 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

# 마우스 호버 툴팁 설정 (편수 및 비율)
fig1.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "장르: %{label}<br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    legend_title_text="장르"
)

st.plotly_chart(
    fig1,
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

treemap_df = df[["genre", "movieNm", "total_audi"]].copy()
treemap_df["total_audi"] = pd.to_numeric(treemap_df["total_audi"], errors="coerce").fillna(0)
treemap_df["movieNm"] = treemap_df["movieNm"].fillna("영화명 미상").astype(str)

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객 트리맵",
    color="genre"
)

fig2.update_traces(
    hovertemplate=(
        "영화명: %{label}<br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(margin=dict(t=50, l=10, r=10, b=10))

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph2_note"
)


# ==================================================
# 그래프 3. 영화별 총 관객 수 분포 (히스토그램)
# ==================================================

st.divider()

st.subheader("그래프 3. 영화별 총 관객 수 분포")

st.caption(
    "영화별 total_audi(총 관객)가 "
    "어느 구간에 많이 몰려 있는지 보여 주는 히스토그램입니다."
)

hist_df = df[["movieNm", "total_audi"]].copy()
hist_df["total_audi"] = pd.to_numeric(hist_df["total_audi"], errors="coerce")
hist_df = hist_df.dropna(subset=["total_audi"])

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={"total_audi": "총 관객 수", "count": "영화 편수"}
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

st.plotly_chart(fig3, use_container_width=True)

# 안내 문구 계산 및 출력
max_audience_row = hist_df.loc[hist_df["total_audi"].idxmax()]
max_movie_name = max_audience_row["movieNm"]
max_audience = max_audience_row["total_audi"]

hist_counts, bin_edges = pd.cut(
    hist_df["total_audi"],
    bins=20,
    include_lowest=True,
    retbins=True
)
most_common_bin = hist_counts.value_counts().idxmax()

st.markdown("**이 그래프로 알 수 있는 것**")

st.info(
    f"대부분의 영화는 총 관객 약 "
    f"{most_common_bin.left:,.0f}명 ~ {most_common_bin.right:,.0f}명 "
    f"구간에 몰려 있습니다."
)

st.info(
    f"가장 관객이 많은 영화는 "
    f"**{max_movie_name}**이며, "
    f"총 관객은 **{max_audience:,.0f}명**입니다."
)

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph3_note"
)


# ==================================================
# 그래프 4. 개봉일 스크린수와 총 관객의 관계 (산점도)
# ==================================================

st.divider()

st.subheader("그래프 4. 개봉일 스크린수와 총 관객의 관계")

st.caption(
    "개봉일 스크린수와 총 관객 사이의 관계를 "
    "장르별 색으로 구분한 산점도입니다."
)

scatter_df = df[["movieNm", "genre", "first_scrn", "total_audi"]].copy()
scatter_df["first_scrn"] = pd.to_numeric(scatter_df["first_scrn"], errors="coerce")
scatter_df["total_audi"] = pd.to_numeric(scatter_df["total_audi"], errors="coerce")
scatter_df = scatter_df.dropna(subset=["movieNm", "genre", "first_scrn", "total_audi"])

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

fig4.update_traces(
    hovertemplate=(
        "영화명: %{hovertext}<br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(size=10, opacity=0.75)
)

fig4.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph4_note"
)


# ==================================================
# 그래프 5. 개봉일 스크린수, 첫 주 관객, 총 관객의 관계 (버블 차트)
# ==================================================

st.divider()

st.subheader("그래프 5. 개봉일 스크린수, 첫 주 관객, 총 관객의 관계")

st.caption(
    "개봉일 스크린수(X축)와 총 관객 수(Y축)에 더해, "
    "원의 크기로 '첫 주 관객 수'를 함께 보여 주는 버블 차트입니다."
)

bubble_df = df[["movieNm", "genre", "first_scrn", "first_week_audi", "total_audi"]].copy()
for col in ["first_scrn", "first_week_audi", "total_audi"]:
    bubble_df[col] = pd.to_numeric(bubble_df[col], errors="coerce")

bubble_df = bubble_df.dropna(subset=["movieNm", "genre", "first_scrn", "first_week_audi", "total_audi"])
bubble_df = bubble_df[bubble_df["first_week_audi"] > 0]

fig5 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
    title="개봉일 스크린수, 첫 주 관객, 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르"
    }
)

fig5.update_traces(
    hovertemplate=(
        "영화명: %{hovertext}<br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(opacity=0.7)
)

fig5.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph5_note"
)


# ==================================================
# 그래프 6. 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ==================================================

st.divider()

st.subheader("그래프 6. 제작 국가 및 장르별 영화 편수")

st.caption(
    "안쪽 고리는 제작 국가(nation), 바깥쪽 고리는 장르(genre)를 나타내며, "
    "조각의 크기는 해당 조건에 속한 영화 편수를 의미합니다."
)

sunburst_df = df[["nation", "genre"]].copy()
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("국가 미상")
    .astype(str)
    .str.strip()
    .replace("", "국가 미상")
)

sunburst_counts = sunburst_df.groupby(["nation", "genre"]).size().reset_index(name="count")

fig6 = px.sunburst(
    sunburst_counts,
    path=["nation", "genre"],
    values="count",
    title="제작 국가 및 장르별 영화 편수",
    color="nation"
)

fig6.update_traces(
    hovertemplate=(
        "구분: %{label}<br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percentParent:.1%}"
        "<extra></extra>"
    )
)

fig6.update_layout(margin=dict(t=50, l=10, r=10, b=10))

st.plotly_chart(fig6, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph6_note"
)


# ==================================================
# 그래프 7. 10위권에 오래 머문 영화는 총 관객도 많은가
# ==================================================

st.divider()

st.subheader("그래프 7. 10위권에 오래 머문 영화는 총 관객도 많은가")

st.caption(
    "10위권에 머문 날수(X축)와 총 관객 수(Y축)의 관계를 보여 주는 산점도입니다."
)

scatter_top10_df = df[["movieNm", "genre", "days_in_top10", "total_audi"]].copy()
scatter_top10_df["days_in_top10"] = pd.to_numeric(scatter_top10_df["days_in_top10"], errors="coerce")
scatter_top10_df["total_audi"] = pd.to_numeric(scatter_top10_df["total_audi"], errors="coerce")
scatter_top10_df = scatter_top10_df.dropna(subset=["movieNm", "days_in_top10", "total_audi"])

fig7 = px.scatter(
    scatter_top10_df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        "days_in_top10": "10위권에 머문 날수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    }
)

fig7.update_traces(
    hovertemplate=(
        "영화명: %{hovertext}<br>"
        "10위권 유지 기간: %{x:,.0f}일<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(size=10, opacity=0.75)
)

fig7.update_layout(
    xaxis_title="10위권에 머문 날수",
    yaxis_title="총 관객 수",
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph7_note"
)


# ==================================================
# 그래프 8. 총 관객 수가 높은 영화는 개봉 첫 주 관객 수도 많은가
# ==================================================

st.divider()

st.subheader("그래프 8. 총 관객 수가 높은 영화는 개봉 첫 주 관객 수도 많은가")

st.caption(
    "첫 주 관객 수(X축)와 총 관객 수(Y축)의 관계를 보여 주는 산점도입니다. "
    "점에 마우스를 올리면 개별 영화명과 관객 수 정보를 확인할 수 있습니다."
)

first_week_df = df[["movieNm", "genre", "first_week_audi", "total_audi"]].copy()
first_week_df["first_week_audi"] = pd.to_numeric(first_week_df["first_week_audi"], errors="coerce")
first_week_df["total_audi"] = pd.to_numeric(first_week_df["total_audi"], errors="coerce")
first_week_df = first_week_df.dropna(subset=["movieNm", "first_week_audi", "total_audi"])

fig8 = px.scatter(
    first_week_df,
    x="first_week_audi",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="총 관객 수가 높은 영화는 개봉 첫 주 관객 수도 많은가",
    labels={
        "first_week_audi": "첫 주 관객 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    }
)

fig8.update_traces(
    hovertemplate=(
        "영화명: %{hovertext}<br>"
        "첫 주 관객: %{x:,.0f}명<br>"
        "총 관객 수: %{y:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(size=9, opacity=0.75)
)

fig8.update_layout(
    xaxis_title="첫 주 관객 수",
    yaxis_title="총 관객 수",
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig8, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="이 그래프에서 알 수 있는 내용을 한 문장으로 적어 보세요.",
    label_visibility="collapsed",
    key="graph8_note"
)
# ==================================================
