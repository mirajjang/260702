import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

from embedded_data import (
    BIRTH_RECENT_CSV,
    TFR_MILESTONES_CSV,
    REGIONAL_TFR_CSV,
    SIDO_AGE_CSV,
)

# ----------------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="대한민국 인구 데이터 교실 | 출생 반등의 비밀",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLOR_DECLINE = "#94A3B8"   # 회색빛 파랑 — 하락기
COLOR_REBOUND = "#F97316"   # 주황 — 반등기 강조
COLOR_MAIN = "#0F172A"      # 남색 텍스트/기본선
COLOR_BLUE = "#2563EB"
COLOR_TEAL = "#0D9488"
COLOR_LIGHT = "#F8FAFC"
FONT_FAMILY = "'Pretendard', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif"

PLOTLY_TEMPLATE = "plotly_white"


def base_layout(fig, title=None, height=460):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        font=dict(family=FONT_FAMILY, size=14, color=COLOR_MAIN),
        title=dict(text=title, font=dict(size=19, family=FONT_FAMILY)) if title else None,
        height=height,
        margin=dict(l=40, r=30, t=60 if title else 30, b=40),
        hoverlabel=dict(font_size=13, font_family=FONT_FAMILY),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig


# ----------------------------------------------------------------------------
# 데이터 로딩
# ----------------------------------------------------------------------------
@st.cache_data
def load_birth_recent():
    return pd.read_csv(io.StringIO(BIRTH_RECENT_CSV))


@st.cache_data
def load_tfr_milestones():
    df = pd.read_csv(io.StringIO(TFR_MILESTONES_CSV))
    df["event"] = df["event"].fillna("")
    return df


@st.cache_data
def load_regional_tfr():
    return pd.read_csv(io.StringIO(REGIONAL_TFR_CSV))


@st.cache_data
def load_sido_age():
    return pd.read_csv(io.StringIO(SIDO_AGE_CSV))


birth_recent = load_birth_recent()
tfr_milestones = load_tfr_milestones()
regional_tfr = load_regional_tfr()
sido_age = load_sido_age()

SIDO_LIST = sido_age[sido_age["sido"] != "전국"]["sido"].tolist()

# ----------------------------------------------------------------------------
# 커스텀 CSS
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        font-family: {FONT_FAMILY};
    }}
    .main-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {COLOR_MAIN};
        margin-bottom: 0.2rem;
    }}
    .sub-title {{
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }}
    .insight-box {{
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        border-left: 5px solid {COLOR_REBOUND};
        padding: 1rem 1.3rem;
        border-radius: 10px;
        margin: 0.8rem 0 1.2rem 0;
    }}
    .concept-box {{
        background: #F1F5F9;
        border-left: 5px solid {COLOR_BLUE};
        padding: 0.9rem 1.2rem;
        border-radius: 10px;
        margin: 0.6rem 0 1rem 0;
        font-size: 0.95rem;
    }}
    .metric-caption {{
        color: #64748B;
        font-size: 0.85rem;
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 1.7rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 사이드바
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 👶 인구 데이터 교실")
    st.caption("청소년을 위한 대한민국 인구 분석 가이드")
    st.markdown("---")
    page = st.radio(
        "탐구 순서를 골라보세요",
        [
            "🏠 시작하기",
            "📉 60년의 여정",
            "🔄 최근 반등 심층분석",
            "👶 진짜 데이터로 본 반등",
            "🗺️ 지역별 비교",
            "🧠 인사이트 & 생각해보기",
        ],
    )
    st.markdown("---")
    st.markdown(
        """
        **데이터 출처**
        - 통계청/국가데이터처 「출생·사망통계」
        - 행정안전부 「연령별 인구현황」 (2026.06 기준, 사용자 제공)

        본 대시보드는 교육 목적의 요약·재구성 자료이며,
        공식 수치는 통계청 KOSIS를 확인해 주세요.
        """
    )

st.markdown('<div class="main-title">🇰🇷 대한민국 인구 데이터로 배우는 저출산과 반등</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">인구 데이터 분석가처럼, 숫자 속에 숨은 이야기를 함께 찾아봐요.</div>',
    unsafe_allow_html=True,
)

# ============================================================================
# PAGE 1: 시작하기
# ============================================================================
if page == "🏠 시작하기":
    col1, col2, col3, col4 = st.columns(4)
    latest = birth_recent.iloc[-1]
    prev = birth_recent.iloc[-2]
    col1.metric("2025년 출생아 수", f"{latest['births']:,.0f}명", f"+{latest['births']-prev['births']:,.0f}명")
    col2.metric("2025년 합계출산율", f"{latest['tfr']:.2f}명", f"+{latest['tfr']-prev['tfr']:.2f}명")
    col3.metric("반등 연속 연차", "2년 연속", "2024년부터")
    col4.metric("전국 총인구(2026.06)", f"{sido_age[sido_age['sido']=='전국']['total_pop'].values[0]:,.0f}명")

    st.markdown(
        """
        <div class="insight-box">
        <b>🔎 오늘의 미션</b><br>
        대한민국의 합계출산율은 2015년부터 <b>9년 연속</b> 떨어지다가, 2024년과 2025년 <b>2년 연속 반등</b>했어요.
        "정말 반등이 시작된 걸까?", "왜 하필 지금일까?" 이 대시보드에서 실제 통계로 직접 확인해봐요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📖 먼저 알아야 할 핵심 용어")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="concept-box">
            <b>합계출산율 (TFR)</b><br>
            여성 한 명이 가임기간(15~49세) 동안
            낳을 것으로 예상되는 평균 자녀 수예요.
            숫자가 2.1명 정도는 되어야 인구가
            줄지도 늘지도 않는 '대체수준'이라고 해요.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="concept-box">
            <b>출생아 수</b><br>
            한 해 동안 실제로 태어난 아기의 수예요.
            합계출산율이 같아도 아이를 낳을 수 있는
            여성의 수(가임 인구)가 줄면
            출생아 수는 더 줄어들 수 있어요.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="concept-box">
            <b>인구 자연증가율</b><br>
            (출생아 수 − 사망자 수)를 인구로 나눈 값이에요.
            한국은 2020년부터 사망자가 출생아보다
            많아 '자연감소' 상태가 이어지고 있어요.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🗂️ 이 대시보드에서 만날 데이터")
    st.markdown(
        """
        1. **60년의 여정** — 1970년부터 2025년까지, 출생아 수와 합계출산율이 그려온 큰 그림
        2. **최근 반등 심층분석** — 2015~2025년을 확대해서, 반등의 시작과 이유를 살펴봐요
        3. **진짜 데이터로 본 반등** — 2026년 6월 실제 주민등록 인구 데이터에서 반등의 흔적을 찾아봐요
        4. **지역별 비교** — 서울과 지방, 인구 구조는 얼마나 다를까요?
        5. **인사이트 & 생각해보기** — 데이터를 바탕으로 스스로 질문을 던져봐요
        """
    )

# ============================================================================
# PAGE 2: 60년의 여정
# ============================================================================
elif page == "📉 60년의 여정":
    st.markdown("## 📉 1970~2025, 출생아 수와 합계출산율의 60년")
    st.markdown(
        """
        아래 그래프는 통계 작성이 시작된 1970년부터 2025년까지의 흐름이에요.
        점 위에 마우스를 올리면 그 해에 무슨 일이 있었는지 볼 수 있어요.
        """
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=tfr_milestones["year"],
            y=tfr_milestones["births"],
            name="출생아 수(명)",
            marker_color=[COLOR_REBOUND if y >= 2024 else COLOR_DECLINE for y in tfr_milestones["year"]],
            yaxis="y1",
            opacity=0.75,
            hovertemplate="%{x}년<br>출생아 수: %{y:,}명<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tfr_milestones["year"],
            y=tfr_milestones["tfr"],
            name="합계출산율(명)",
            yaxis="y2",
            mode="lines+markers+text",
            line=dict(color=COLOR_TEAL, width=3),
            marker=dict(size=9),
            text=tfr_milestones["event"],
            textposition="top center",
            textfont=dict(size=10, color="#334155"),
            hovertemplate="%{x}년<br>합계출산율: %{y:.2f}명<br>%{text}<extra></extra>",
        )
    )
    fig.update_layout(
        yaxis=dict(title="출생아 수(명)", side="left", showgrid=False),
        yaxis2=dict(title="합계출산율(명)", overlaying="y", side="right", showgrid=False, range=[0, 5]),
        xaxis=dict(title="연도", dtick=5),
    )
    fig = base_layout(fig, height=560)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 큰 그림에서 읽을 수 있는 것</b><br>
        1970년대에는 매년 100만 명 넘는 아기가 태어났어요(합계출산율 4명 이상).
        이후 산업화·경제성장과 함께 출산율은 꾸준히 낮아졌고, 2002년 '초저출산'(1.3명 미만)에 진입했어요.
        2015년 잠시 반등했지만 2016년부터 다시 8년 연속 급락해 2023년 0.72명으로 역대 최저를 찍었습니다.
        그리고 2024~2025년, 아주 오랜만에 <b>2년 연속 반등</b>이 나타났어요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("🧭 연도별 원자료 표로 보기"):
        show_df = tfr_milestones.rename(
            columns={"year": "연도", "births": "출생아 수", "tfr": "합계출산율", "event": "주요 사건"}
        )
        st.dataframe(show_df, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE 3: 최근 반등 심층분석
# ============================================================================
elif page == "🔄 최근 반등 심층분석":
    st.markdown("## 🔄 2015~2025년, 반등의 시작을 확대해서 보기")

    fig = go.Figure()
    colors = [COLOR_REBOUND if y >= 2024 else COLOR_DECLINE for y in birth_recent["year"]]
    fig.add_trace(
        go.Bar(
            x=birth_recent["year"],
            y=birth_recent["births"],
            name="출생아 수(명)",
            marker_color=colors,
            hovertemplate="%{x}년<br>출생아 수: %{y:,}명<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=birth_recent["year"],
            y=birth_recent["tfr"] * 100000,
            name="합계출산율(우측 눈금, ×10만 환산)",
            mode="lines+markers",
            line=dict(color=COLOR_TEAL, width=3, dash="dot"),
            marker=dict(size=8),
            customdata=birth_recent["tfr"],
            hovertemplate="%{x}년<br>합계출산율: %{customdata:.3f}명<extra></extra>",
        )
    )
    fig.update_layout(xaxis=dict(dtick=1, title="연도"), yaxis=dict(title="출생아 수(명)"))
    fig = base_layout(fig, title="9년 연속 하락 → 2년 연속 반등", height=480)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 💍 혼인 건수도 함께 늘었어요")
        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
                x=birth_recent["year"],
                y=birth_recent["marriages"],
                mode="lines+markers",
                fill="tozeroy",
                line=dict(color=COLOR_BLUE, width=3),
                fillcolor="rgba(37,99,235,0.12)",
                hovertemplate="%{x}년<br>혼인 건수: %{y:,}건<extra></extra>",
            )
        )
        fig2.update_layout(xaxis=dict(dtick=1), yaxis=dict(title="혼인 건수(건)"))
        fig2 = base_layout(fig2, height=380)
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("한국은 출생의 약 96%가 혼인 출생이에요. 혼인이 늘면 2년 정도의 시차를 두고 출생아 수도 늘어나는 경향이 있어요.")

    with c2:
        st.markdown("### 📊 반등 전후 비교")
        row_2023 = birth_recent[birth_recent["year"] == 2023].iloc[0]
        row_2025 = birth_recent[birth_recent["year"] == 2025].iloc[0]
        compare_df = pd.DataFrame(
            {
                "지표": ["출생아 수", "합계출산율", "혼인 건수"],
                "2023년(저점)": [row_2023["births"], row_2023["tfr"], row_2023["marriages"]],
                "2025년": [row_2025["births"], row_2025["tfr"], row_2025["marriages"]],
            }
        )
        compare_df["증감률"] = (
            (compare_df["2025년"] - compare_df["2023년(저점)"]) / compare_df["2023년(저점)"] * 100
        ).round(1).astype(str) + "%"
        st.dataframe(compare_df, use_container_width=True, hide_index=True)
        st.markdown(
            """
            <div class="insight-box">
            <b>💡 전문가들이 꼽는 반등 이유</b><br>
            ① 코로나19로 미뤘던 결혼과 출산이 한꺼번에 이루어짐(펜트업 효과)<br>
            ② 30대 후반 여성의 출산율 상승(만혼 이후 출산 증가)<br>
            ③ 신생아 특례대출, 육아휴직 급여 인상 등 정책 효과<br>
            단, 코로나로 미뤄졌던 수요가 일시적으로 몰린 것인지, 구조적인 추세 전환인지는
            아직 <b>더 지켜봐야 한다</b>는 신중한 시각도 있어요.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 👩 연령대별 출산율 변화 — 누가 반등을 이끌었을까?")
    age_group_df = pd.DataFrame(
        {
            "연도": ["2024년", "2025년"],
            "30대 후반 출산율(해당 연령 여성 1000명당 출생아)": [46.0, 52.0],
        }
    )
    fig3 = px.bar(
        age_group_df,
        x="연도",
        y="30대 후반 출산율(해당 연령 여성 1000명당 출생아)",
        color="연도",
        color_discrete_sequence=[COLOR_DECLINE, COLOR_REBOUND],
    )
    fig3.update_traces(hovertemplate="%{x}<br>%{y:.1f}명<extra></extra>", showlegend=False)
    fig3 = base_layout(fig3, height=380)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(
        """
        <div class="concept-box">
        국가데이터처 발표에 따르면 2025년 <b>30대 후반 여성의 출산율은 통계 작성 이래 역대 최고</b>를 기록했어요(1000명당 46.0명 → 52.0명).
        연령별 출산율은 30대 초반이 여전히 가장 높은 수준을 유지한 가운데, 20대 이상 전 연령대에서 출산율이 올랐어요.
        30대 후반 증가폭이 가장 두드러졌다는 건, 결혼과 출산 시기가 늦어지는(만혼화) 흐름 속에서도
        '더 늦게라도 낳는' 경향이 강해지고 있다는 뜻으로 해석돼요.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================================
# PAGE 4: 진짜 데이터로 본 반등
# ============================================================================
elif page == "👶 진짜 데이터로 본 반등":
    st.markdown("## 👶 2026년 6월 실제 주민등록 인구 데이터에서 반등의 흔적 찾기")
    st.markdown(
        """
        지금까지는 통계청이 발표한 '출생통계'를 봤어요. 이번에는 **행정안전부의 2026년 6월 주민등록 인구현황**
        (전국 17개 시도, 나이 한 살 단위) 원자료를 직접 뜯어봐요. 나이 0~11세 인구를 보면,
        몇 년생이 많고 적은지 — 즉 그 해에 아기가 얼마나 태어났었는지를 오늘 기준으로 추정할 수 있어요.
        """
    )

    national = sido_age[sido_age["sido"] == "전국"].iloc[0]
    ages = list(range(0, 15))
    pop_by_age = [national[f"total_age_{a}"] for a in ages]
    birth_year = [2026 - a for a in ages]

    fig = go.Figure()
    bar_colors = [COLOR_REBOUND if a <= 1 else COLOR_DECLINE for a in ages]
    fig.add_trace(
        go.Bar(
            x=[f"{a}세<br>({y}년생 무렵)" for a, y in zip(ages, birth_year)],
            y=pop_by_age,
            marker_color=bar_colors,
            hovertemplate="%{x}<br>인구: %{y:,}명<extra></extra>",
        )
    )
    fig.update_layout(xaxis=dict(title="만 나이 (2026년 6월 기준)"), yaxis=dict(title="전국 인구(명)"))
    fig = base_layout(fig, title="0~14세 인구, 나이 한 살 단위로 보기", height=480)
    st.plotly_chart(fig, use_container_width=True)

    trough_age = min(ages, key=lambda a: national[f"total_age_{a}"])
    trough_pop = national[f"total_age_{trough_age}"]
    age0_pop = national["total_age_0"]
    age1_pop = national["total_age_1"]

    st.markdown(
        f"""
        <div class="insight-box">
        <b>🔎 데이터가 보여주는 것</b><br>
        인구가 가장 적은 나이는 <b>{trough_age}세</b>({trough_pop:,}명)예요.
        그런데 그보다 어린 <b>1세({age1_pop:,}명)</b>와 <b>0세({age0_pop:,}명)</b>는 오히려 인구가 다시 늘어나
        막대그래프가 '<b>V자</b>' 모양을 그리고 있어요.
        이 V자 반등이 바로, 통계청이 발표한 2024~2025년 출생아 수 반등이 실제 인구 데이터에도
        고스란히 새겨져 있다는 증거예요. 숫자는 다른 곳에서 왔지만, 이야기는 똑같이 맞아떨어지죠!
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 👫 남녀로 나눠서 보기")
    male_by_age = [national[f"male_age_{a}"] for a in ages]
    female_by_age = [national[f"female_age_{a}"] for a in ages]
    fig4 = go.Figure()
    fig4.add_trace(
        go.Scatter(
            x=ages, y=male_by_age, name="남성", mode="lines+markers",
            line=dict(color=COLOR_BLUE, width=3),
            hovertemplate="%{x}세<br>남성: %{y:,}명<extra></extra>",
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=ages, y=female_by_age, name="여성", mode="lines+markers",
            line=dict(color="#DB2777", width=3),
            hovertemplate="%{x}세<br>여성: %{y:,}명<extra></extra>",
        )
    )
    fig4.update_layout(xaxis=dict(title="만 나이", dtick=1), yaxis=dict(title="인구(명)"))
    fig4 = base_layout(fig4, height=400)
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("자연적으로 남아가 여아보다 조금 더 많이 태어나요(출생성비 105~107 정도가 정상 범위). 그래프에서도 대부분 연령에서 남성 인구가 여성보다 살짝 많은 걸 볼 수 있어요.")

    st.markdown("### 🏔️ 전국 인구 피라미드 (2026년 6월)")
    st.markdown("나이를 5세 단위로 묶어 만든 인구 피라미드예요. 아래로 갈수록 어린 세대, 위로 갈수록 고령 세대예요.")

    def age_group_label(a):
        if a >= 100:
            return "100+"
        low = (a // 5) * 5
        return f"{low}-{low+4}"

    all_ages = list(range(0, 101))
    pyramid_rows = []
    for a in all_ages:
        m = national.get(f"male_age_{a}", 0)
        f = national.get(f"female_age_{a}", 0)
        pyramid_rows.append({"age": a, "group": age_group_label(a), "male": m, "female": f})
    pyr_df = pd.DataFrame(pyramid_rows).groupby("group", sort=False).sum(numeric_only=True).reset_index()
    order = [f"{i}-{i+4}" for i in range(0, 100, 5)] + ["100+"]
    pyr_df["group"] = pd.Categorical(pyr_df["group"], categories=order, ordered=True)
    pyr_df = pyr_df.sort_values("group")

    fig5 = go.Figure()
    fig5.add_trace(
        go.Bar(
            y=pyr_df["group"], x=-pyr_df["male"], name="남성", orientation="h",
            marker_color=COLOR_BLUE,
            hovertemplate="%{y}세<br>남성: %{customdata:,}명<extra></extra>",
            customdata=pyr_df["male"],
        )
    )
    fig5.add_trace(
        go.Bar(
            y=pyr_df["group"], x=pyr_df["female"], name="여성", orientation="h",
            marker_color="#DB2777",
            hovertemplate="%{y}세<br>여성: %{x:,}명<extra></extra>",
        )
    )
    fig5.update_layout(
        barmode="relative",
        xaxis=dict(title="인구(명)", tickvals=[-2000000, -1000000, 0, 1000000, 2000000],
                    ticktext=["200만", "100만", "0", "100만", "200만"]),
        yaxis=dict(title="연령대"),
    )
    fig5 = base_layout(fig5, height=650)
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("허리가 볼록한 '항아리형' 피라미드는 저출산·고령화 사회의 전형적인 모습이에요. 40~50대(1970~80년대생 에코붐 세대 자녀 포함)가 가장 두꺼운 층을 이루고 있어요.")

# ============================================================================
# PAGE 5: 지역별 비교
# ============================================================================
elif page == "🗺️ 지역별 비교":
    st.markdown("## 🗺️ 서울 vs 지방, 인구 구조는 얼마나 다를까?")

    st.markdown("### 📈 2025년 합계출산율 — 확인된 상위·하위 지역")
    st.caption("국가데이터처가 공식 발표한 수치 중 명시적으로 확인된 지역만 표시했어요(전남·세종·충북 상위, 부산·서울 하위).")
    reg_sorted = regional_tfr.sort_values("tfr_2025", ascending=True)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=reg_sorted["tfr_2025"],
            y=reg_sorted["sido"],
            orientation="h",
            marker_color=[COLOR_REBOUND if v == reg_sorted["tfr_2025"].max() else
                          (COLOR_MAIN if v == reg_sorted["tfr_2025"].min() else COLOR_TEAL)
                          for v in reg_sorted["tfr_2025"]],
            text=reg_sorted["note"],
            textposition="outside",
            hovertemplate="%{y}<br>2025년 합계출산율: %{x:.2f}명<br>%{text}<extra></extra>",
        )
    )
    fig.add_vline(x=0.80, line_dash="dash", line_color="#94A3B8", annotation_text="전국 평균(0.80명)")
    fig.update_layout(xaxis=dict(title="합계출산율(명)", range=[0, 1.3]), yaxis=dict(title=""))
    fig = base_layout(fig, height=380)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("전남(1.10명)이 가장 높고 서울(0.63명)이 가장 낮아요. 두 지역의 차이는 약 1.7배예요. 대도시일수록 집값·경쟁·양육 비용 부담이 커 출산율이 낮은 경향이 있어요.")

    st.markdown("### 👶 실제 인구 데이터로 본 시도별 '어린 인구' 비중")
    st.caption("2026년 6월 행정안전부 주민등록 인구 원자료 기준 — 0세 인구가 총인구에서 차지하는 비율(‰, 천 명당)이에요. 값이 높을수록 최근 그 지역에서 아기가 상대적으로 더 많이 태어났다는 뜻이에요.")

    reg_rows = []
    for _, r in sido_age[sido_age["sido"] != "전국"].iterrows():
        ratio = r["total_age_0"] / r["total_pop"] * 1000
        reg_rows.append({"sido": r["sido"], "0세_인구비율": ratio, "0세_인구": r["total_age_0"]})
    reg_real_df = pd.DataFrame(reg_rows).sort_values("0세_인구비율", ascending=True)

    fig1b = go.Figure()
    fig1b.add_trace(
        go.Bar(
            x=reg_real_df["0세_인구비율"],
            y=reg_real_df["sido"],
            orientation="h",
            marker_color=COLOR_TEAL,
            customdata=reg_real_df["0세_인구"],
            hovertemplate="%{y}<br>0세 인구 비율: %{x:.2f}‰<br>0세 인구: %{customdata:,}명<extra></extra>",
        )
    )
    fig1b.update_layout(xaxis=dict(title="0세 인구 비율(천 명당)"), yaxis=dict(title=""))
    fig1b = base_layout(fig1b, height=520)
    st.plotly_chart(fig1b, use_container_width=True)

    st.markdown("### 🔍 시도별 인구 자세히 보기")
    selected_sido = st.selectbox("궁금한 지역을 선택해보세요", SIDO_LIST, index=SIDO_LIST.index("서울특별시") if "서울특별시" in SIDO_LIST else 0)

    row = sido_age[sido_age["sido"] == selected_sido].iloc[0]
    national = sido_age[sido_age["sido"] == "전국"].iloc[0]

    working_age = sum(row[f"total_age_{a}"] for a in range(15, 65))
    young = sum(row[f"total_age_{a}"] for a in range(0, 15))
    old = sum(row[f"total_age_{a}"] for a in range(65, 101))
    total = row["total_pop"]
    aging_index = round(old / young * 100, 1) if young > 0 else None

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("총인구", f"{total:,.0f}명")
    c2.metric("유소년(0~14세) 비중", f"{young/total*100:.1f}%")
    c3.metric("고령(65세+) 비중", f"{old/total*100:.1f}%")
    c4.metric("고령화 지수", f"{aging_index}", help="유소년 인구 100명당 고령 인구 수. 100이 넘으면 고령 인구가 더 많다는 뜻이에요.")

    ages = list(range(0, 101))

    def make_group(a):
        if a >= 100:
            return "100+"
        low = (a // 5) * 5
        return f"{low}-{low+4}"

    rows = []
    for a in ages:
        rows.append({"group": make_group(a), "male": row[f"male_age_{a}"], "female": row[f"female_age_{a}"]})
    gdf = pd.DataFrame(rows).groupby("group", sort=False).sum(numeric_only=True).reset_index()
    order = [f"{i}-{i+4}" for i in range(0, 100, 5)] + ["100+"]
    gdf["group"] = pd.Categorical(gdf["group"], categories=order, ordered=True)
    gdf = gdf.sort_values("group")

    fig6 = go.Figure()
    fig6.add_trace(go.Bar(y=gdf["group"], x=-gdf["male"], name="남성", orientation="h", marker_color=COLOR_BLUE,
                           customdata=gdf["male"], hovertemplate="%{y}세<br>남성: %{customdata:,}명<extra></extra>"))
    fig6.add_trace(go.Bar(y=gdf["group"], x=gdf["female"], name="여성", orientation="h", marker_color="#DB2777",
                           hovertemplate="%{y}세<br>여성: %{x:,}명<extra></extra>"))
    fig6.update_layout(barmode="relative", xaxis=dict(title="인구(명)"), yaxis=dict(title="연령대"))
    fig6 = base_layout(fig6, title=f"{selected_sido} 인구 피라미드 (2026.06)", height=600)
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("### ⚖️ 전국 평균과 비교하기")
    nat_young = sum(national[f"total_age_{a}"] for a in range(0, 15))
    nat_old = sum(national[f"total_age_{a}"] for a in range(65, 101))
    nat_total = national["total_pop"]
    comp_df = pd.DataFrame(
        {
            "구분": ["유소년 비중(%)", "고령 비중(%)"],
            selected_sido: [round(young/total*100, 1), round(old/total*100, 1)],
            "전국 평균": [round(nat_young/nat_total*100, 1), round(nat_old/nat_total*100, 1)],
        }
    )
    fig7 = px.bar(
        comp_df.melt(id_vars="구분", var_name="지역", value_name="비중"),
        x="구분", y="비중", color="지역", barmode="group",
        color_discrete_sequence=[COLOR_REBOUND, COLOR_DECLINE],
    )
    fig7 = base_layout(fig7, height=380)
    st.plotly_chart(fig7, use_container_width=True)

# ============================================================================
# PAGE 6: 인사이트 & 생각해보기
# ============================================================================
elif page == "🧠 인사이트 & 생각해보기":
    st.markdown("## 🧠 데이터로 생각을 넓혀봐요")

    st.markdown(
        """
        <div class="insight-box">
        <b>📌 오늘 배운 3가지 핵심 인사이트</b><br><br>
        <b>1. 반등은 '숫자'와 '진짜 인구' 양쪽에서 모두 확인돼요.</b><br>
        통계청의 출생통계(2024년 +3.6%, 2025년 +6.8%)와, 행정안전부의 실제 주민등록 인구
        (0~2세 사이의 'V자' 반등)가 서로 다른 자료인데도 같은 이야기를 하고 있어요.<br><br>
        <b>2. 반등을 이끈 건 '더 많은 사람'이 아니라 '조금 더 낳는 사람들'이에요.</b><br>
        30대 후반 여성의 출산율 상승이 가장 컸어요. 결혼과 출산이 늦어지는 흐름(만혼화) 속에서도,
        결혼한 사람들이 자녀를 갖는 비율은 오히려 조금씩 늘고 있어요.<br><br>
        <b>3. 지역 차이가 매우 커요.</b><br>
        전남(1.10명)과 서울(0.63명)의 격차는 거의 1.7배예요. 저출산은 전국 공통 현상이지만,
        원인과 해법은 지역마다 다를 수 있어요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🤔 스스로에게 던져볼 질문들")
    with st.expander("Q1. 이 반등은 '추세 전환'일까, '일시적 되돌림'일까?"):
        st.markdown(
            """
            코로나19로 미뤄졌던 결혼·출산이 2022~2025년에 몰려서 나타난 '펜트업 효과'라면,
            이 효과가 소진되는 순간 다시 감소세로 돌아갈 수 있어요.
            반면 신혼부부 소득 상승, 정책 지원 확대, '결혼하면 아이를 갖겠다'는 인식 변화가
            계속된다면 구조적인 전환일 수도 있어요. **여러분은 앞으로 3년의 데이터에서 무엇을 확인하면
            이 질문에 답할 수 있을까요?**
            """
        )
    with st.expander("Q2. 왜 서울의 합계출산율이 가장 낮을까?"):
        st.markdown(
            """
            주택 가격, 사교육비, 출퇴근 거리, 일-가정 양립 어려움 등 여러 가설이 있어요.
            같은 수도권이라도 세종(1.06명)은 서울보다 훨씬 높죠. **주거 형태나 직장까지의
            거리 같은 변수를 추가로 조사한다면, 어떤 데이터를 더 찾아봐야 할까요?**
            """
        )
    with st.expander("Q3. 출생아 수가 늘어도 총인구는 왜 계속 줄어들까?"):
        st.markdown(
            """
            2025년에도 사망자 수가 출생아 수보다 많아 인구는 자연감소했어요(자연증가율 -2.1명/천 명).
            고령 인구 비중이 늘고 있기 때문에, 출생아 수가 어느 정도 반등하더라도
            총인구 감소를 바로 멈추기는 어려워요. **'인구 감소를 멈추려면 합계출산율이
            얼마나, 얼마나 오래 올라야 할까?' 를 어떻게 추정해볼 수 있을까요?**
            """
        )

    st.markdown("### 🧪 미니 퀴즈로 점검하기")
    q1 = st.radio(
        "1. 합계출산율이 몇 명 정도여야 인구가 늘지도 줄지도 않는 '대체수준'일까요?",
        ["1.0명", "1.5명", "2.1명", "3.0명"],
        index=None,
    )
    if q1:
        st.success("정답: 2.1명! 사망 등을 고려하면 여성 한 명이 평균 2.1명은 낳아야 인구가 유지돼요.") if q1 == "2.1명" else st.error("아쉬워요! 정답은 2.1명이에요.")

    q2 = st.radio(
        "2. 2026년 6월 실제 인구 데이터에서, 인구가 가장 적었던 나이대는 몇 세 무렵이었나요?",
        ["0세", "2세", "5세", "10세"],
        index=None,
    )
    if q2:
        st.success("정답: 2세! 2023~2024년생이 가장 적었고, 그보다 어린 0~1세부터 다시 늘기 시작했어요.") if q2 == "2세" else st.error("아쉬워요! 실제 데이터에서 저점은 2세 부근이었어요.")

    st.markdown("---")
    st.caption("📚 이 대시보드는 통계청·국가데이터처의 출생통계 발표자료와 행정안전부의 「연령별 인구현황」(2026년 6월) 원자료를 바탕으로 제작한 교육용 자료입니다. 최신 공식 수치는 KOSIS 국가통계포털(kosis.kr)에서 확인해 주세요.")
