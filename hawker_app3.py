# -*- coding: utf-8 -*-
import streamlit as st
import altair as alt
import os
from datetime import datetime, date

DATA_FILE = "sales_data.txt"
PAYMENT_TYPES = ["Cash", "PayNow", "PayLah", "PayWave"]
APP_PASSWORD = "1234"

LANG = {
    "English": {
        "title": "🍜 Hawker Cash Register",
        "caption": "A simple digital receipt & sales tracker for small hawker stalls",
        "menu_new": "🧾 New Sale",
        "menu_daily": "📅 Daily Report",
        "menu_monthly": "📆 Monthly Report",
        "lock": "🔒 Lock System",
        "login_title": "🔐 Staff Login Required",
        "pin_prompt": "Enter PIN to unlock cash register (Default: 1234)",
        "login_btn": "Login",
        "login_success": "Login successful!",
        "login_error": "Incorrect PIN. Please try again.",
        "new_sale_header": "🧾 New Sale",
        "date": "📅 Date",
        "amount": "💵 Sale Amount ($)",
        "tendered": "💰 Amount Rendered by Customer ($)",
        "payment_type": "💳 Payment Type",
        "submit_btn": "✅ Record Sale",
        "amount_error": "⚠️ Amount rendered is less than the sale amount. Please check and try again.",
        "success_msg": "🎉 Sale recorded successfully!",
        "sale_amt": "💵 **Sale Amount:** $",
        "render_amt": "💰 **Amount Rendered:** $",
        "change_due": "🪙 **Change Due:** $",
        "pay_type": "💳 **Payment Type:** ",
        "undo_header": "⚠️ Quick Correction: Undo Last Sale",
        "undo_btn": "❌ Undo Last Transaction",
        "undo_success": "Successfully deleted the last transaction!",
        "undo_fail": "Failed to undo.",
        "no_undo": "No transactions to undo.",
        "recent_header": "🕒 Recent Transactions (Live Stream)",
        "no_live": "No transactions yet today.",
        "daily_header": "📅 Daily Transaction Report",
        "select_date": "Select a date",
        "target_header": "🎯 Daily Target Tracker",
        "target_input": "Set Today's Revenue Goal ($)",
        "progress": "Progress: \\${:.2f} / \\${:.2f} ({:.1f}%)",
        "goal_achieved": "🎉 Congratulations! You have reached today's revenue goal!",
        "no_daily": "😴 No transactions recorded for this date.",
        "trans_list": "🧾 Transaction Listing for ",
        "daily_total": "💰 **Total Sales for the Day: $",
        "download_daily": "📥 Download Daily Report as CSV",
        "breakdown": "📊 Breakdown by Payment Type (Optional Report)",
        "monthly_header": "📆 Monthly Sales Report",
        "year": "Year",
        "month": "Month",
        "no_monthly": "😴 No transactions recorded for this month.",
        "monthly_summary": "📈 Summarised Sales by Day for ",
        "monthly_total": "💰 **Total Sales for the Month: $",
        "download_monthly": "📥 Download Monthly Report as CSV",
        "monthly_breakdown": "📊 Breakdown by Payment Type for the Month (Optional Report)"
    },
    "中文": {
        "title": "🍜 熟食中心收银系统",
        "caption": "一个专为小型熟食摊位设计的小型数码收银与销售跟踪系统",
        "menu_new": "🧾 新增交易",
        "menu_daily": "📅 日报表",
        "menu_monthly": "📆 月报表",
        "lock": "🔒 锁定系统",
        "login_title": "🔐 员工登录验证",
        "pin_prompt": "请输入PIN码解锁收银台 (默认: 1234)",
        "login_btn": "登录",
        "login_success": "登录成功！",
        "login_error": "PIN码错误，请重试。",
        "new_sale_header": "🧾 新增交易",
        "date": "📅 日期",
        "amount": "💵 销售金额 ($)",
        "tendered": "💰 顾客实付金额 ($)",
        "payment_type": "💳 支付方式",
        "submit_btn": "✅ 记录交易",
        "amount_error": "⚠️ 实付金额小于销售金额，请核对后重试。",
        "success_msg": "🎉 交易记录成功！",
        "sale_amt": "💵 **销售金额：** $",
        "render_amt": "💰 **实付金额：** $",
        "change_due": "🪙 **找零：** $",
        "pay_type": "💳 **支付方式：** ",
        "undo_header": "⚠️ 快捷纠错：撤销上一笔交易",
        "undo_btn": "❌ 撤销上一笔交易",
        "undo_success": "成功删除上一笔交易！",
        "undo_fail": "撤销失败。",
        "no_undo": "暂无交易可撤销。",
        "recent_header": "🕒 最近交易流水 (实时)",
        "no_live": "今天暂无交易记录。",
        "daily_header": "📅 每日交易报表",
        "select_date": "选择日期",
        "target_header": "🎯 每日营业额目标追踪",
        "target_input": "设定今日营业额目标 ($)",
        "progress": "进度：\\${:.2f} / \\${:.2f} ({:.1f}%)",
        "goal_achieved": "🎉 恭喜！您已达成今日营业额目标！",
        "no_daily": "😴 该日期暂无交易记录。",
        "trans_list": "🧾 交易明细列表：",
        "daily_total": "💰 **今日总销售额：$",
        "download_daily": "📥 下载当日报表 CSV",
        "breakdown": "📊 按支付方式分类统计",
        "monthly_header": "📆 每月销售报表",
        "year": "年份",
        "month": "月份",
        "no_monthly": "😴 该月份暂无交易记录。",
        "monthly_summary": "📈 每日销售汇总：",
        "monthly_total": "💰 **本月总销售额：$",
        "download_monthly": "📥 下载当月报表 CSV",
        "monthly_breakdown": "📊 本月按支付方式分类统计"
    }
}

def render_payment_bar_chart(payment_summary):
    records = []
    for pt in PAYMENT_TYPES:
        records.append({"Payment Type": pt, "Total ($)": payment_summary.get(pt, 0.0)})

    chart = alt.Chart(alt.Data(values=records)).mark_bar(color="#1f77b4").encode(
        x=alt.X("Payment Type:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
        y=alt.Y("Total ($):Q"),
        tooltip=[alt.Tooltip("Payment Type:N"), alt.Tooltip("Total ($):Q")],
    )
    st.altair_chart(chart, use_container_width=True)

def ensure_data_file(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("date,time,amount,tendered,change,payment_type\n")

def save_transaction(filename, record_date, record_time, amount, tendered, change, payment_type):
    line = record_date + "," + record_time + "," + str(amount) + "," + str(tendered) + "," + str(change) + "," + payment_type + "\n"
    with open(filename, "a") as f:
        f.write(line)

def delete_last_transaction(filename):
    if not os.path.exists(filename):
        return False
    with open(filename, "r") as f:
        lines = f.readlines()
    if len(lines) <= 1:
        return False
    with open(filename, "w") as f:
        f.writelines(lines[:-1])
    return True

def load_all_transactions(filename):
    transactions = []
    ensure_data_file(filename)
    with open(filename, "r") as f:
        lines = f.readlines()

    first_line = True
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if first_line:
            first_line = False
            continue
        parts = line.split(",")
        if len(parts) != 6:
            continue
        record_date = parts[0]
        record_time = parts[1]
        amount = float(parts[2])
        tendered = float(parts[3])
        change = float(parts[4])
        payment_type = parts[5]
        transactions.append([record_date, record_time, amount, tendered, change, payment_type])

    return transactions

def get_transactions_by_date(transactions, target_date):
    result = []
    for t in transactions:
        if t[0] == target_date:
            result.append(t)
    return result

def get_daily_total(day_transactions):
    total = 0.0
    for t in day_transactions:
        total = total + t[2]
    return total

def get_monthly_daily_summary(transactions, year_month):
    daily_totals = {}
    for t in transactions:
        record_date = t[0]
        if record_date[0:7] == year_month:
            if record_date in daily_totals:
                daily_totals[record_date] = daily_totals[record_date] + t[2]
            else:
                daily_totals[record_date] = t[2]

    summary = []
    for d in sorted(daily_totals.keys()):
        summary.append([d, daily_totals[d]])
    return summary

def get_payment_summary(transaction_list):
    summary = {}
    for pt in PAYMENT_TYPES:
        summary[pt] = 0.0
    for t in transaction_list:
        pt = t[5]
        if pt in summary:
            summary[pt] = summary[pt] + t[2]
        else:
            summary[pt] = t[2]
    return summary

st.set_page_config(page_title="Hawker Cash Register", page_icon="🍜")

lang_choice = st.sidebar.selectbox("🌐 Language / 语言", ["English", "中文"])
t = LANG[lang_choice]

st.title(t["title"])
st.caption(t["caption"])

ensure_data_file(DATA_FILE)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.subheader(t["login_title"])
    pwd_input = st.text_input(t["pin_prompt"], type="password")
    if st.button(t["login_btn"]):
        if pwd_input == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.success(t["login_success"])
            st.rerun()
        else:
            st.error(t["login_error"])
    st.stop()

if st.sidebar.button(t["lock"]):
    st.session_state["authenticated"] = False
    st.rerun()

_existing_count = len(load_all_transactions(DATA_FILE))
st.sidebar.caption("💾 " + str(_existing_count) + " transaction(s) saved in " + DATA_FILE)

menu = st.sidebar.radio("📋 Menu", [t["menu_new"], t["menu_daily"], t["menu_monthly"]])

if menu == t["menu_new"]:
    st.header(t["new_sale_header"])

    with st.form("new_sale_form", clear_on_submit=True):
        sale_date = st.date_input(t["date"], value=date.today())
        amount = st.number_input(t["amount"], min_value=0.0, step=0.5, format="%.2f")
        tendered = st.number_input(t["tendered"], min_value=0.0, step=0.5, format="%.2f")
        payment_type = st.selectbox(t["payment_type"], PAYMENT_TYPES)
        submitted = st.form_submit_button(t["submit_btn"])

    if submitted:
        if tendered < amount:
            st.error(t["amount_error"])
        else:
            change = round(tendered - amount, 2)
            now = datetime.now()
            record_date = sale_date.strftime("%Y-%m-%d")
            record_time = now.strftime("%H:%M:%S")

            save_transaction(DATA_FILE, record_date, record_time, round(amount, 2), round(tendered, 2), change, payment_type)

            st.success(t["success_msg"])
            st.write(t["sale_amt"] + format(amount, ".2f"))
            st.write(t["render_amt"] + format(tendered, ".2f"))
            st.write(t["change_due"] + format(change, ".2f"))
            st.write(t["pay_type"] + payment_type)

    st.divider()
    st.subheader(t["undo_header"])
    all_trans_for_undo = load_all_transactions(DATA_FILE)
    if len(all_trans_for_undo) > 0:
        last_t = all_trans_for_undo[-1]
        st.write(f"Last: {last_t[0]} {last_t[1]} | Amount: **${last_t[2]:.2f}** | Type: `{last_t[5]}`")
        if st.button(t["undo_btn"]):
            if delete_last_transaction(DATA_FILE):
                st.success(t["undo_success"])
                st.rerun()
            else:
                st.error(t["undo_fail"])
    else:
        st.info(t["no_undo"])

    st.divider()
    st.subheader(t["recent_header"])
    all_transactions_live = load_all_transactions(DATA_FILE)
    if len(all_transactions_live) == 0:
        st.info(t["no_live"])
    else:
        recent_5 = all_transactions_live[-5:][::-1]
        live_table = []
        for tr in recent_5:
            live_table.append({
                "Date": tr[0],
                "Time": tr[1],
                "Amount ($)": format(tr[2], ".2f"),
                "Payment": tr[5]
            })
        st.table(live_table)

elif menu == t["menu_daily"]:
    st.header(t["daily_header"])

    report_date = st.date_input(t["select_date"], value=date.today())
    report_date_str = report_date.strftime("%Y-%m-%d")

    all_transactions = load_all_transactions(DATA_FILE)
    day_transactions = get_transactions_by_date(all_transactions, report_date_str)

    st.subheader(t["target_header"])
    daily_goal = st.number_input(t["target_input"], min_value=10.0, value=100.0, step=50.0)
    daily_total_val = get_daily_total(day_transactions)
    
    progress_val = min(daily_total_val / daily_goal, 1.0) if daily_goal > 0 else 0.0
    st.progress(progress_val, text=t["progress"].format(daily_total_val, daily_goal, progress_val * 100))
    if daily_total_val >= daily_goal:
        st.success(t["goal_achieved"])

    if len(day_transactions) == 0:
        st.info(t["no_daily"])
    else:
        st.subheader(t["trans_list"] + report_date_str)

        table_data = []
        for tr in day_transactions:
            table_data.append({
                "Time": tr[1],
                "Amount ($)": format(tr[2], ".2f"),
                "Tendered ($)": format(tr[3], ".2f"),
                "Change ($)": format(tr[4], ".2f"),
                "Payment Type": tr[5],
            })
        st.table(table_data)

        daily_total = get_daily_total(day_transactions)
        st.write(t["daily_total"] + format(daily_total, ".2f") + "**")

        csv_lines = ["date,time,amount,tendered,change,payment_type"]
        for tr in day_transactions:
            csv_lines.append(f"{tr[0]},{tr[1]},{tr[2]},{tr[3]},{tr[4]},{tr[5]}")
        csv_data_str = "\n".join(csv_lines)
        
        st.download_button(
            label=t["download_daily"],
            data=csv_data_str,
            file_name=f"daily_report_{report_date_str}.csv",
            mime="text/csv"
        )

        st.subheader(t["breakdown"])
        payment_summary = get_payment_summary(day_transactions)

        summary_table = []
        for pt in PAYMENT_TYPES:
            summary_table.append({"Payment Type": pt, "Total ($)": format(payment_summary[pt], ".2f")})
        st.table(summary_table)

        render_payment_bar_chart(payment_summary)

elif menu == t["menu_monthly"]:
    st.header(t["monthly_header"])

    year = st.number_input(t["year"], min_value=2020, max_value=2100, value=date.today().year, step=1)
    month = st.number_input(t["month"], min_value=1, max_value=12, value=date.today().month, step=1)
    year_month_str = str(int(year)) + "-" + str(int(month)).zfill(2)

    all_transactions = load_all_transactions(DATA_FILE)
    monthly_summary = get_monthly_daily_summary(all_transactions, year_month_str)

    if len(monthly_summary) == 0:
        st.info(t["no_monthly"])
    else:
        st.subheader(t["monthly_summary"] + year_month_str)

        table_data = []
        chart_data = {}
        month_total = 0.0
        for row in monthly_summary:
            table_data.append({"Date": row[0], "Total Sales ($)": format(row[1], ".2f")})
            chart_data[row[0]] = row[1]
            month_total = month_total + row[1]
        st.table(table_data)
        st.line_chart(chart_data)

        st.write(t["monthly_total"] + format(month_total, ".2f") + "**")

        month_transactions_for_export = []
        for tr in all_transactions:
            if tr[0][0:7] == year_month_str:
                month_transactions_for_export.append(tr)

        month_csv_lines = ["date,time,amount,tendered,change,payment_type"]
        for tr in month_transactions_for_export:
            month_csv_lines.append(f"{tr[0]},{tr[1]},{tr[2]},{tr[3]},{tr[4]},{tr[5]}")
        month_csv_data_str = "\n".join(month_csv_lines)

        st.download_button(
            label=t["download_monthly"],
            data=month_csv_data_str,
            file_name=f"monthly_report_{year_month_str}.csv",
            mime="text/csv"
        )

        st.subheader(t["monthly_breakdown"])
        month_transactions = []
        for tr in all_transactions:
            if tr[0][0:7] == year_month_str:
                month_transactions.append(tr)

        payment_summary = get_payment_summary(month_transactions)
        summary_table = []
        for pt in PAYMENT_TYPES:
            summary_table.append({"Payment Type": pt, "Total ($)": format(payment_summary[pt], ".2f")})
        st.table(summary_table)
        render_payment_bar_chart(payment_summary)