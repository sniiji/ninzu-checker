import streamlit as st
import re

def extract_people_count(text):
    pattern = r'([0-9一二三四五六七八九十]+)[人名]'
    return re.findall(pattern, text)

def normalize_number(n):
    kanji_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
    }
    try:
        return int(n)
    except ValueError:
        return sum(kanji_map.get(c, 0) for c in n)

def load_names_from_file(uploaded_file):
    content = uploaded_file.read().decode('utf-8')
    return [line.strip() for line in content.splitlines() if line.strip()]

def compare_with_names(title, intro, body, names):
    sections = {
        "タイトル": extract_people_count(title),
        "紹介文": extract_people_count(intro),
        "本文": extract_people_count(body)
    }

    normalized = {k: [normalize_number(v) for v in vlist] for k, vlist in sections.items()}
    actual_count = len(set(names))

    st.subheader("🔍 抽出された人数表現")
    for k, v in normalized.items():
        st.write(f"{k}: {v if v else '記載なし'}")

    st.subheader("👥 登場人物リスト")
    st.write(names)
    st.write(f"→ 実際の人数: {actual_count}")

    st.subheader("📊 整合性チェック")
    for k, v in normalized.items():
        if v and v[0] != actual_count:
            st.error(f"{k} に記載された人数（{v[0]}）と人名数（{actual_count}）が一致しません！")
        else:
            st.success(f"{k} は人名数と一致しています")

st.title("人数整合性チェッカー")

title_text = st.text_area("タイトルを入力", height=50)
intro_text = st.text_area("紹介文を入力", height=100)
body_text = st.text_area("本文を入力", height=150)
uploaded_file = st.file_uploader("人名リストファイル（.txt）をアップロード", type="txt")

if st.button("チェックする"):
    if uploaded_file:
        name_list = load_names_from_file(uploaded_file)
        compare_with_names(title_text, intro_text, body_text, name_list)
    else:
        st.warning("人名リストファイルをアップロードしてください。")