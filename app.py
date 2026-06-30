# # CD "ORUN\발주 프로그램\pro_app"
# # git add .
# # git commit -m "수정 멘트"
# # git push
# # 수정된거 확인하려면 git status  ->  modified: app.py 뜨면 잘 수정된거


# import streamlit as st
# import pandas as pd

# st.set_page_config(
#     page_title="오런 재고 소진 대시보드",
#     layout="wide"
# )

# # 기준날짜 직접 입력
# BASE_DATE = "2026-04-30"

# st.title("오런 재고 소진 대시보드")
# st.caption(f"기준날짜: {BASE_DATE}")

# df = pd.read_csv("./data/forecast_dashboard.csv")

# # 월 컬럼 자동 인식
# month_cols = [
#     c for c in df.columns
#     if isinstance(c, str) and len(c) == 7 and c[:4].isdigit() and c[4] == "-"
# ]

# # 숫자 변환
# for col in ["현재고"] + month_cols:
#     df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# # 사이드바
# st.sidebar.header("필터")

# supplier_list = ["전체"] + sorted(df["매입처명"].dropna().astype(str).unique().tolist())
# selected_supplier = st.sidebar.selectbox("매입처명", supplier_list)

# keyword = st.sidebar.text_input("상품명 검색")

# risk_only = st.sidebar.checkbox("품절예상 상품만 보기", value=False)

# start_month = st.sidebar.selectbox("조회 시작월", month_cols, index=0)

# start_idx = month_cols.index(start_month)
# available_months = month_cols[start_idx:]

# show_month_count = st.sidebar.slider(
#     "표시 개월 수",
#     min_value=1,
#     max_value=len(available_months),
#     value=min(6, len(available_months))
# )

# show_months = available_months[:show_month_count]

# filtered = df.copy()

# if selected_supplier != "전체":
#     filtered = filtered[filtered["매입처명"].astype(str) == selected_supplier]

# if keyword:
#     filtered = filtered[
#         filtered["상품명"].astype(str).str.contains(keyword, case=False, na=False)
#     ]

# if risk_only:
#     filtered = filtered[filtered["품절예상월"].notna()]

# filtered = filtered.sort_values(
#     ["품절예상월", "매입처명", "상품명"],
#     na_position="last"
# )

# # KPI
# col1, col2, col3, col4 = st.columns(4)

# col1.metric("조회 상품 수", f"{len(filtered):,}")
# col2.metric("품절예상 상품 수", f"{filtered['품절예상월'].notna().sum():,}")
# col3.metric("매입처 수", f"{filtered['매입처명'].nunique():,}")

# if len(filtered) > 0:
#     first_risk_month = filtered["품절예상월"].dropna().min()
# else:
#     first_risk_month = "-"

# col4.metric("가장 빠른 품절월", first_risk_month if pd.notna(first_risk_month) else "-")

# st.divider()

# # 표시 컬럼
# show_cols = [
#     "매입처명",
#     "상품명",
#     "현재고",
#     "품절예상월"
# ] + show_months

# display_df = filtered[show_cols].copy()

# # 음수 스타일
# def negative_style(value):
#     try:
#         value = float(value)
#         if value < 0:
#             return "color: red; font-weight: bold;"
#     except:
#         pass
#     return ""

# styled_df = (
#     display_df
#     .style
#     .bar(
#         subset=show_months,
#         align="zero"
#     )
#     .map(negative_style, subset=show_months)
#     .format({
#         "현재고": "{:,.0f}",
#         **{col: "{:,.0f}" for col in show_months}
#     })
# )

# st.subheader("상품별 예상 잔여재고")
# st.dataframe(
#     styled_df,
#     use_container_width=True,
#     height=750
# )

# # 다운로드
# csv = display_df.to_csv(index=False, encoding="utf-8-sig")

# st.download_button(
#     label="현재 조회 결과 CSV 다운로드",
#     data=csv,
#     file_name=f"오런_재고소진대시보드_{BASE_DATE}.csv",
#     mime="text/csv"
# )



import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="오런 재고 소진 대시보드 ver1",
    layout="wide"
)

BASE_DATE = "2026-06-30"

st.title("오런 재고 소진 대시보드")
st.caption(f"기준날짜: {BASE_DATE}")

# 데이터 불러오기
df = pd.read_csv("./data/forecast_dashboard.csv")
annual_sales_df = pd.read_csv("./data/annual_sales_df.csv")
monthly_sales_df = pd.read_csv("./data/monthly_sales_df.csv")

# 판매량 데이터 정리
monthly_sales_df["년월"] = pd.to_datetime(monthly_sales_df["년월"])
monthly_sales_df["수량"] = pd.to_numeric(monthly_sales_df["수량"], errors="coerce").fillna(0)

annual_sales_df["년도"] = annual_sales_df["년도"].astype(int)
annual_sales_df["수량"] = pd.to_numeric(annual_sales_df["수량"], errors="coerce").fillna(0)

tab1, tab2 = st.tabs(["재고 소진 대시보드", "상품별 판매량 추이"])

##############################################################################
# TAB 1. 재고 소진 대시보드
##############################################################################

with tab1:

    # 월 컬럼 자동 인식
    month_cols = [
        c for c in df.columns
        if isinstance(c, str) and len(c) == 7 and c[:4].isdigit() and c[4] == "-"
    ]

    # 숫자 변환
    for col in ["현재고"] + month_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 사이드바
    st.sidebar.header("필터")

    supplier_list = ["전체"] + sorted(df["매입처명"].dropna().astype(str).unique().tolist())
    selected_supplier = st.sidebar.selectbox("매입처명", supplier_list)

    keyword = st.sidebar.text_input("상품명 검색")

    risk_only = st.sidebar.checkbox("품절예상 상품만 보기", value=False)

    start_month = st.sidebar.selectbox("조회 시작월", month_cols, index=0)

    start_idx = month_cols.index(start_month)
    available_months = month_cols[start_idx:]

    show_month_count = st.sidebar.slider(
        "표시 개월 수",
        min_value=1,
        max_value=len(available_months),
        value=min(6, len(available_months))
    )

    show_months = available_months[:show_month_count]

    filtered = df.copy()

    if selected_supplier != "전체":
        filtered = filtered[filtered["매입처명"].astype(str) == selected_supplier]

    if keyword:
        filtered = filtered[
            filtered["상품명"].astype(str).str.contains(keyword, case=False, na=False)
        ]

    if risk_only:
        filtered = filtered[filtered["품절예상월"].notna()]

    filtered = filtered.sort_values(
        ["품절예상월", "매입처명", "상품명"],
        na_position="last"
    )

    # KPI
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("조회 상품 수", f"{len(filtered):,}")
    col2.metric("품절예상 상품 수", f"{filtered['품절예상월'].notna().sum():,}")
    col3.metric("매입처 수", f"{filtered['매입처명'].nunique():,}")

    if len(filtered) > 0:
        first_risk_month = filtered["품절예상월"].dropna().min()
    else:
        first_risk_month = "-"

    col4.metric("가장 빠른 품절월", first_risk_month if pd.notna(first_risk_month) else "-")

    st.divider()

    # 표시 컬럼
    show_cols = [
        "매입처명",
        "상품명",
        "현재고",
        "품절예상월"
    ] + show_months

    display_df = filtered[show_cols].copy()

    # 음수 스타일
    def negative_style(value):
        try:
            value = float(value)
            if value < 0:
                return "color: red; font-weight: bold;"
        except:
            pass
        return ""

    styled_df = (
        display_df
        .style
        .bar(
            subset=show_months,
            align="zero"
        )
        .map(negative_style, subset=show_months)
        .format({
            "현재고": "{:,.0f}",
            **{col: "{:,.0f}" for col in show_months}
        })
    )

    st.subheader("상품별 예상 잔여재고")
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=750
    )

    # 다운로드
    csv = display_df.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="현재 조회 결과 CSV 다운로드",
        data=csv,
        file_name=f"오런_재고소진대시보드_{BASE_DATE}.csv",
        mime="text/csv"
    )

##############################################################################
# TAB 2. 상품별 판매량 추이
##############################################################################

with tab2:

    st.subheader("상품별 판매량 추이")

    product_list = sorted(monthly_sales_df["상품명"].dropna().astype(str).unique().tolist())

    selected_products = st.multiselect(
        "상품 선택",
        product_list,
        default=product_list[:1]
    )

    view_type = st.radio(
        "조회 기준",
        ["월별", "연도별"],
        horizontal=True
    )

    if len(selected_products) == 0:
        st.warning("상품을 1개 이상 선택하세요.")

    else:

        if view_type == "월별":

            temp = monthly_sales_df[
                monthly_sales_df["상품명"].astype(str).isin(selected_products)
            ].copy()

            temp = temp.sort_values(["상품명", "년월"])

            min_month = temp["년월"].min()
            max_month = temp["년월"].max()

            start_date, end_date = st.date_input(
                "조회 기간",
                value=(min_month.date(), max_month.date()),
                min_value=min_month.date(),
                max_value=max_month.date()
            )

            temp = temp[
                (temp["년월"] >= pd.to_datetime(start_date)) &
                (temp["년월"] <= pd.to_datetime(end_date))
            ]

            temp["수량표시"] = temp["수량"].round(0).astype(int).astype(str)

            fig = px.line(
                temp,
                x="년월",
                y="수량",
                color="상품명",
                markers=True,
                text="수량표시"
            )

            fig.update_traces(
                marker=dict(size=11),
                textposition="top center",
                line=dict(width=3)
            )

            fig.update_layout(
                height=600,
                xaxis_title="년월",
                yaxis_title="판매량",
                hovermode="x unified",
                legend_title_text="상품명"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(
                temp,
                use_container_width=True
            )

        else:

            temp = annual_sales_df[
                annual_sales_df["상품명"].astype(str).isin(selected_products)
            ].copy()

            temp = temp.sort_values(["상품명", "년도"])

            year_list = sorted(temp["년도"].unique().tolist())

            start_year, end_year = st.select_slider(
                "조회 연도",
                options=year_list,
                value=(min(year_list), max(year_list))
            )

            temp = temp[
                (temp["년도"] >= start_year) &
                (temp["년도"] <= end_year)
            ]

            temp["수량표시"] = temp["수량"].round(0).astype(int).astype(str)
            temp["년도"] = temp["년도"].astype(str)
            fig = px.line(
                temp,
                x="년도",
                y="수량",
                color="상품명",
                markers=True,
                text="수량표시"
            )

            fig.update_traces(
                marker=dict(size=13),
                textposition="top center",
                line=dict(width=4)
            )

            fig.update_layout(
                height=600,
                xaxis_title="년도",
                yaxis_title="판매량",
                hovermode="x unified",
                legend_title_text="상품명",
                xaxis=dict(type="category")
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(
                temp,
                use_container_width=True
            )