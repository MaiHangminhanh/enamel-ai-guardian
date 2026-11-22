
import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO

# ==================================================
# ENAMEL-AI GUARDIAN
# Web App giáo dục bảo vệ men răng học đường
# Python + Streamlit + Pandas
# ==================================================

st.set_page_config(
    page_title="Enamel-AI Guardian",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GIAO DIỆN
st.markdown("""
<style>
.stApp {
    background-color: #f3f9ff;
}
h1, h2, h3 {
    color: #075985;
}
[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# PHẦN 1. CƠ SỞ DỮ LIỆU 50 LOẠI ĐỒ UỐNG
# Giá trị pH minh họa từ tài liệu người dùng cung cấp.
# Chưa được xác minh bằng đo đạc thực nghiệm.
# ==================================================

DATA = """
Tên đồ uống|pH|Nhóm
Coca-Cola truyền thống|2.52|Nước ngọt và tăng lực
Coca-Cola Zero / Light|2.95|Nước ngọt và tăng lực
Pepsi|2.53|Nước ngọt và tăng lực
Pepsi Black|2.98|Nước ngọt và tăng lực
7Up|3.20|Nước ngọt và tăng lực
Sprite|3.29|Nước ngọt và tăng lực
Mirinda Cam / Fanta Cam|2.82|Nước ngọt và tăng lực
Mirinda Soda Kem|3.15|Nước ngọt và tăng lực
Mountain Dew|3.22|Nước ngọt và tăng lực
Red Bull|3.30|Nước ngọt và tăng lực
Sting Dâu|2.89|Nước ngọt và tăng lực
Monster Energy|3.48|Nước ngọt và tăng lực
Wake-up 247|3.25|Nước ngọt và tăng lực
Revive|3.45|Nước ngọt và tăng lực
Nước khoáng có ga vị chanh|3.85|Nước ngọt và tăng lực
Nước chanh / Trà chanh|2.30|Trà và nước ép
Nước quất / Trà tắc|2.43|Trà và nước ép
Trà đào cam sả|3.30|Trà và nước ép
Nước ép cam|3.50|Trà và nước ép
Nước ép bưởi|3.20|Trà và nước ép
Nước ép dứa|3.40|Trà và nước ép
Nước ép táo đóng hộp|3.40|Trà và nước ép
Nước ép cóc / Xoài xanh|2.95|Trà và nước ép
Trà dâu tằm / Trà mãng cầu|3.35|Trà và nước ép
Trà mận / Nước mơ|2.80|Trà và nước ép
Nước me đá|2.80|Trà và nước ép
Nước chanh dây|2.70|Trà và nước ép
Trà xanh C2|3.05|Trà và nước ép
Trà xanh Không Độ|2.95|Trà và nước ép
Trà Oolong Tea+|3.80|Trà và nước ép
Trà sữa trân châu|6.00|Trà sữa và cà phê
Trà sữa matcha|5.90|Trà sữa và cà phê
Trà sữa socola|5.75|Trà sữa và cà phê
Cà phê đen không đường|5.10|Trà sữa và cà phê
Cà phê sữa đá|6.00|Trà sữa và cà phê
Cà phê hòa tan|5.20|Trà sữa và cà phê
Nước tăng lực cà phê|3.80|Trà sữa và cà phê
Cacao|6.30|Trà sữa và cà phê
Sữa chua uống|3.70|Sữa và đồ lên men
Sữa chua ăn có đường|4.10|Sữa và đồ lên men
Sữa tươi có đường|6.65|Sữa và đồ lên men
Sữa tươi không đường|6.75|Sữa và đồ lên men
Sữa đậu nành|6.50|Sữa và đồ lên men
Sữa hạt óc chó / Hạnh nhân|6.40|Sữa và đồ lên men
Nước dừa tươi|5.30|Sữa và đồ lên men
Trà Kombucha|3.00|Sữa và đồ lên men
Nước khoáng kiềm|8.75|Nước uống khác
Nước lọc tinh khiết|7.00|Nước uống khác
Nước đun sôi để nguội|7.00|Nước uống khác
Trà xanh tươi không đường|6.35|Nước uống khác
"""

@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(DATA.strip()), sep="|")
    df["pH"] = pd.to_numeric(df["pH"])
    return df

df = load_data()

# ==================================================
# PHẦN 2. HÀM PHÂN LOẠI VÀ CHẤM ĐIỂM
# ==================================================

def classify_ph(ph):
    if ph < 3.0:
        return "Mức 1 - Rất axit"
    elif ph < 4.5:
        return "Mức 2 - Axit cao"
    elif ph <= 5.5:
        return "Mức 3 - Axit vừa"
    else:
        return "Mức 4 - Ít axit theo pH"

def explain_ph(ph):
    if ph < 3.0:
        return (
            "Đồ uống có pH rất thấp. Nếu tiếp xúc "
            "thường xuyên hoặc kéo dài, axit có thể "
            "góp phần gây xói mòn men răng."
        )
    elif ph < 4.5:
        return (
            "Đồ uống có tính axit rõ rệt. "
            "Nên giảm tần suất sử dụng và "
            "hạn chế thời gian tiếp xúc với răng."
        )
    elif ph <= 5.5:
        return (
            "Đồ uống có tính axit. Nguy cơ thực tế "
            "còn phụ thuộc thành phần, lượng uống "
            "và thói quen vệ sinh răng miệng."
        )
    else:
        return (
            "pH không quá thấp. Tuy nhiên điều này "
            "không đồng nghĩa đồ uống hoàn toàn "
            "an toàn cho răng, nhất là khi chứa đường."
        )

def score_exposure(ph, minutes, straw, rinsed):
    # Điểm quy ước phục vụ giáo dục,
    # không phải thang điểm nha khoa chuẩn.
    score = 0

    if ph < 3.5:
        score += 4
    elif ph <= 5.5:
        score += 2

    if minutes >= 30:
        score += 3

    if not straw:
        score += 2

    if rinsed:
        score -= 3
    else:
        score += 2

    return max(0, min(10, score))

def risk_label(score):
    if score <= 3:
        return "Thấp trong mô hình"
    elif score <= 6:
        return "Trung bình trong mô hình"
    return "Cao trong mô hình"

def suggestions(ph, minutes, rinsed):
    advice = []
    if ph <= 5.5:
        advice.append(
            "Giảm tần suất dùng đồ uống axit; "
            "ưu tiên nước lọc khi khát."
        )
    if minutes >= 30:
        advice.append(
            "Không nhâm nhi đồ uống axit "
            "kéo dài trong buổi học."
        )
    if not rinsed:
        advice.append(
            "Súc miệng bằng nước sạch sau khi "
            "uống đồ uống có tính axit."
        )
    if not advice:
        advice.append(
            "Duy trì vệ sinh răng miệng với "
            "kem đánh răng chứa fluoride."
        )
    advice.append(
        "Không chải răng ngay sau khi uống "
        "đồ uống axit; có thể chờ khoảng 1 giờ."
    )
    return advice

# ==================================================
# PHẦN 3. LƯU NHẬT KÝ TRONG PHIÊN SỬ DỤNG
# ==================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==================================================
# PHẦN 4. THANH BÊN
# ==================================================

with st.sidebar:
    st.title("🦷 ENAMEL-AI")
    st.write("GUARDIAN")
    st.caption("Lá chắn bảo vệ men răng học đường")

    st.divider()

    st.info(
        "Ứng dụng học tập về đồ uống axit "
        "và sức khỏe men răng."
    )

    st.metric("Số loại đồ uống", len(df))
    st.metric(
        "Số lượt ghi nhật ký",
        len(st.session_state.history)
    )

    st.divider()

    st.warning(
        "Dữ liệu pH là giá trị tham khảo "
        "chưa được kiểm chứng thực nghiệm. "
        "Điểm nguy cơ là mô hình giáo dục, "
        "không thay thế tư vấn nha khoa."
    )

# ==================================================
# PHẦN 5. TIÊU ĐỀ CHÍNH
# ==================================================

st.title("🦷 ENAMEL-AI GUARDIAN")
st.subheader("Lá chắn bảo vệ men răng học đường")

st.write(
    "Khám phá mối liên hệ giữa độ pH của "
    "đồ uống, thói quen sử dụng và nguy cơ "
    "xói mòn men răng."
)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔎 Tra cứu đồ uống",
    "🧪 Phân tích pH",
    "📒 Nhật ký uống",
    "🛡️ Bảo vệ men răng",
    "📊 Báo cáo và dữ liệu"
])

# ==================================================
# TAB 1. TRA CỨU 50 LOẠI ĐỒ UỐNG
# ==================================================

with tab1:
    st.header("🔎 Tra cứu đồ uống học đường")

    keyword = st.text_input(
        "Tìm tên đồ uống:",
        placeholder="Ví dụ: Coca-Cola, Sting, trà sữa..."
    )

    filtered = df[
        df["Tên đồ uống"].str.contains(
            keyword,
            case=False,
            regex=False,
            na=False
        )
    ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    drink = st.selectbox(
        "Chọn đồ uống để xem chi tiết:",
        df["Tên đồ uống"].tolist()
    )

    item = df[df["Tên đồ uống"] == drink].iloc[0]
    ph = float(item["pH"])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("pH tham khảo", f"{ph:.2f}")
    with c2:
        st.metric("Nhóm", item["Nhóm"])

    st.info(classify_ph(ph))
    st.write(explain_ph(ph))

    st.caption(
        "Không kết luận một sản phẩm cụ thể "
        "có đúng pH này nếu chưa đo mẫu thực tế."
    )

# ==================================================
# TAB 2. PHÂN TÍCH ĐỘ pH
# ==================================================

with tab2:
    st.header("🧪 Phòng thí nghiệm pH ảo")

    custom_ph = st.slider(
        "Điều chỉnh giá trị pH:",
        min_value=0.0,
        max_value=14.0,
        value=3.5,
        step=0.1
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("pH đang chọn", f"{custom_ph:.1f}")
    col2.metric("Mốc tham khảo", "5.5")
    col3.metric(
        "Môi trường",
        "Axit" if custom_ph < 7
        else "Trung tính" if custom_ph == 7
        else "Kiềm"
    )

    ph_chart = pd.DataFrame({
        "Mẫu": ["Giá trị đang chọn", "Mốc 5.5"],
        "pH": [custom_ph, 5.5]
    }).set_index("Mẫu")

    st.bar_chart(ph_chart)

    st.subheader("Kết quả phân tích")
    st.info(classify_ph(custom_ph))
    st.write(explain_ph(custom_ph))

    with st.expander("Giải thích khoa học"):
        st.write(
            "Men răng chứa khoáng chất chủ yếu "
            "ở dạng hydroxyapatite. Trong môi trường "
            "axit, cân bằng hòa tan khoáng có thể "
            "dịch chuyển theo hướng mất khoáng."
        )
        st.write(
            "Ion canxi (Ca²⁺) và phosphate "
            "tham gia cân bằng khoáng hóa. "
            "Nước bọt có vai trò làm sạch, đệm axit "
            "và hỗ trợ quá trình tái khoáng."
        )
        st.write(
            "Ngưỡng pH tới hạn thay đổi theo điều kiện "
            "trong miệng. Không nên dùng duy nhất "
            "giá trị 5.5 để đánh giá mọi đồ uống."
        )

# ==================================================
# TAB 3. NHẬT KÝ UỐNG VÀ CHẤM ĐIỂM
# ==================================================

with tab3:
    st.header("📒 Nhật ký đồ uống trong ngày")

    st.write(
        "Ghi lại thói quen uống để tìm hiểu "
        "những hành vi có thể làm tăng hoặc giảm "
        "thời gian răng tiếp xúc với axit."
    )

    with st.form("diary_form"):
        drink_name = st.selectbox(
            "Hôm nay bạn uống gì?",
            df["Tên đồ uống"].tolist()
        )

        duration = st.slider(
            "Thời gian uống / nhâm nhi (phút):",
            1, 120, 10
        )

        straw = st.checkbox(
            "Tôi có sử dụng ống hút"
        )

        rinsed = st.checkbox(
            "Tôi có súc miệng bằng nước sạch"
        )

        submitted = st.form_submit_button(
            "✅ Phân tích và lưu vào nhật ký"
        )

    if submitted:
        row = df[
            df["Tên đồ uống"] == drink_name
        ].iloc[0]

        selected_ph = float(row["pH"])

        point = score_exposure(
            selected_ph,
            duration,
            straw,
            rinsed
        )

        record = {
            "Thời gian": datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            ),
            "Đồ uống": drink_name,
            "pH tham khảo": selected_ph,
            "Thời gian uống (phút)": duration,
            "Dùng ống hút": "Có" if straw else "Không",
            "Súc miệng": "Có" if rinsed else "Không",
            "Điểm minh họa": point
        }

        st.session_state.history.append(record)

        st.success("Đã ghi nhật ký thành công!")
        st.metric("Điểm lượt uống", f"{point}/10")
        st.info(risk_label(point))

        st.write("### Gợi ý cải thiện")
        for tip in suggestions(
            selected_ph,
            duration,
            rinsed
        ):
            st.write("✅ " + tip)

    if st.session_state.history:
        st.subheader("Các lượt uống đã ghi")

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        # Điểm tổng hợp minh họa:
        # tổng điểm các lượt, giới hạn 10.
        total = min(
            10,
            int(history_df["Điểm minh họa"].sum())
        )

        st.metric(
            "Điểm phơi nhiễm tổng hợp",
            f"{total}/10"
        )

        st.info(risk_label(total))

        st.caption(
            "Tổng điểm bị chặn tại 10, vì vậy "
            "có thể bão hòa khi có nhiều lượt uống. "
            "Không dùng điểm này để suy ra "
            "xác suất sâu răng hoặc mòn men răng."
        )

        if st.button("🗑️ Xóa toàn bộ nhật ký"):
            st.session_state.history = []
            st.rerun()

# ==================================================
# TAB 4. QUY TẮC 3 NÊN - 3 KHÔNG
# ==================================================

with tab4:
    st.header("🛡️ Quy tắc 3 NÊN - 3 KHÔNG")

    left, right = st.columns(2)

    with left:
        st.success("✅ BA ĐIỀU NÊN")
        st.write(
            "1. Ưu tiên nước lọc và súc miệng "
            "bằng nước sạch sau đồ uống axit."
        )
        st.write(
            "2. Nếu dùng ống hút, đặt ống "
            "hướng về phía sau răng cửa để "
            "giảm tiếp xúc trực tiếp."
        )
        st.write(
            "3. Duy trì vệ sinh răng miệng "
            "bằng kem đánh răng chứa fluoride; "
            "có thể nhai kẹo cao su không đường "
            "nếu phù hợp."
        )

    with right:
        st.error("❌ BA ĐIỀU KHÔNG")
        st.write(
            "1. Không ngậm hoặc nhâm nhi "
            "đồ uống có tính axit quá lâu."
        )
        st.write(
            "2. Không chải răng ngay sau "
            "khi uống đồ uống axit; "
            "có thể chờ khoảng 1 giờ."
        )
        st.write(
            "3. Không thường xuyên uống "
            "đồ uống chua hoặc có đường "
            "trước khi đi ngủ."
        )

    st.divider()

    st.subheader("🎯 Thử thách kiến thức")

    answer = st.radio(
        "Sau khi uống nước chanh, "
        "hành động nào hợp lý nhất?",
        [
            "Đánh răng ngay lập tức",
            "Súc miệng bằng nước sạch",
            "Ngậm nước chanh thêm",
            "Uống thêm nước ngọt có ga"
        ],
        index=None
    )

    if st.button("Kiểm tra đáp án"):
        if answer is None:
            st.warning("Hãy chọn một đáp án.")
        elif answer == "Súc miệng bằng nước sạch":
            st.success(
                "Chính xác! Nước sạch giúp "
                "rửa trôi axit còn lại trong miệng."
            )
        else:
            st.error(
                "Chưa đúng. Nên súc miệng "
                "bằng nước sạch sau đồ uống axit."
            )

# ==================================================
# TAB 5. THỐNG KÊ VÀ XUẤT BÁO CÁO
# ==================================================

with tab5:
    st.header("📊 Dữ liệu và báo cáo")

    st.subheader("Phân bố pH của 50 đồ uống")

    chart_df = df.sort_values("pH").set_index(
        "Tên đồ uống"
    )

    st.bar_chart(chart_df["pH"])

    st.subheader("Bảng dữ liệu tham khảo")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Tải danh sách 50 đồ uống (CSV)",
        data=csv_data,
        file_name="du_lieu_50_do_uong.csv",
        mime="text/csv"
    )

    if st.session_state.history:
        st.subheader("Xuất nhật ký học tập")

        report_df = pd.DataFrame(
            st.session_state.history
        )

        report_csv = report_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="⬇️ Tải nhật ký uống (CSV)",
            data=report_csv,
            file_name="nhat_ky_enamel_ai.csv",
            mime="text/csv"
        )

    st.divider()
    st.subheader("Nguồn tham khảo")

    st.markdown(
        "[American Dental Association - "
        "Dental Erosion]"
        "(https://www.ada.org/resources/"
        "ada-library/oral-health-topics/"
        "dental-erosion)"
    )

    st.markdown(
        "[ADA MouthHealthy - Dietary Acids]"
        "(https://www.mouthhealthy.org/"
        "all-topics-a-z/dietary-acids-and-your-teeth/)"
    )

    st.warning(
        "Các pH trong bảng do tài liệu dự án "
        "cung cấp, không được xác nhận bởi "
        "các nguồn tham khảo trên. "
        "Cần đo đạc và dẫn nguồn riêng "
        "trước khi công bố kết quả nghiên cứu."
    )

# ==================================================
# CHÂN TRANG
# ==================================================

st.divider()

st.caption(
    "ENAMEL-AI GUARDIAN | "
    "Dự án giáo dục khoa học bảo vệ men răng | "
    "Phiên bản minh họa 1.0"
)

st.caption(
    "Ứng dụng chỉ phục vụ học tập và nghiên cứu "
    "giáo dục. Không chẩn đoán bệnh hoặc "
    "thay thế việc khám nha khoa."
)
