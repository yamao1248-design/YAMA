import streamlit as st

st.set_page_config(
    page_title="ネットワーク基礎入門：DNSとIPアドレス",
    page_icon="🌐",
    layout="wide",
)

# ------------------------------------------------------------------
# 共通ユーティリティ
# ------------------------------------------------------------------

def normalize(text: str) -> str:
    """全角/半角・空白・大文字小文字のゆらぎを吸収して比較する"""
    if text is None:
        return ""
    table = str.maketrans("０１２３４５６７８９／", "0123456789/")
    return text.translate(table).strip().lower().replace(" ", "").replace("　", "")


def check_blank(user_key: str, correct_answers, label: str):
    """穴埋め1問をチェックして結果を表示する。correct_answersはリスト（複数正解可）でもOK"""
    user_val = st.session_state.get(user_key, "")
    if not user_val:
        return None
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    ok = any(normalize(user_val) == normalize(c) or normalize(c) in normalize(user_val)
             for c in correct_answers)
    if ok:
        st.success(f"✅ {label}：正解です！")
    else:
        st.error(f"❌ {label}：もう一度考えてみましょう。（ヒント: {correct_answers[0]}）")
    return ok


# ------------------------------------------------------------------
# サイドバー：ナビゲーション
# ------------------------------------------------------------------

st.sidebar.title("🌐 ネットワーク基礎入門")
page = st.sidebar.radio(
    "セクションを選択",
    [
        "① 学習目標",
        "② アクティビティ1：DNSと名前解決",
        "③ アクティビティ2：サブネット & TCP/IP",
        "④ 理解度チェック",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("対象：ネットワーク基礎を学ぶ初学者\n所要時間：40〜50分")

# ------------------------------------------------------------------
# ① 学習目標
# ------------------------------------------------------------------

if page == "① 学習目標":
    st.title("🌐 ネットワーク基礎入門：DNSとIPアドレス")
    st.header("📌 学習目標（このレッスンで身につく力）")

    st.markdown("""
このレッスンを終えると、以下のことができるようになります。

1. **通信の起点**：コンピュータ同士が通信する際、最初に「宛先の特定」が必要であり、
   それが**ドメイン名ではなくIPアドレス（数値）**によって行われることを説明できる。
2. **DNSの役割**：人間が使うドメイン名をコンピュータ用のIPアドレスに変換する
   **DNS（Domain Name System）**の仕組みを説明できる。
3. **IPアドレスとサブネット**：グローバルIP／プライベートIPの違いを理解し、
   CIDR表記からサブネットマスク（10進法・2進法）とネットワーク内で使えるIP数を計算できる。
4. **TCP/IP 4階層モデル**：アプリケーション層・トランスポート層・インターネット層・
   ネットワークインターフェース層それぞれの役割を、郵便のたとえを使って説明できる。
5. **データ伝送とルーティング**：パケットがカプセル化され、デフォルトゲートウェイや
   ルーターを経由して宛先まで届く流れを説明できる。
""")

    st.info("👉 左のサイドバーから「アクティビティ1」に進みましょう。")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧩 アクティビティ構成")
        st.markdown("""
        - **アクティビティ1**：DNSと名前解決の穴埋め問題
        - **アクティビティ2**：サブネット計算表 & TCP/IP 4階層表の穴埋め
        - **理解度チェック**：5問の確認クイズ
        """)
    with col2:
        st.subheader("🗺️ 全体像")
        st.code("""
┌──────────────────────────────┐
│   アプリケーション層   │ Web, メール
├──────────────────────────────┤
│   トランスポート層     │ TCP / UDP
├──────────────────────────────┤
│   インターネット層     │ IP, ルーティング
├──────────────────────────────┤
│ ネットワークIF層       │ LAN, Wi-Fi
└──────────────────────────────┘
        """, language=None)

# ------------------------------------------------------------------
# ② アクティビティ1：DNSと名前解決
# ------------------------------------------------------------------

elif page == "② アクティビティ1：DNSと名前解決":
    st.title("🧩 アクティビティ1：DNSと名前解決")

    st.subheader("Step 1｜通信の起点：宛先の特定")
    st.markdown("""
通信を開始する際、最初に行われる最重要ステップは「①　　　」です。

ネットワーク上のコンピュータは②　　　ではなく、③　　　によって相互を④　　　します。

赤字（①〜④）の部分を埋めてください。
""")

    c1, c2 = st.columns(2)
    with c1:
        st.text_input("① 最初に行われる最重要ステップ", key="q1")
        st.text_input("② コンピュータが使わないもの", key="q2")
    with c2:
        st.text_input("③ 実際に使われるもの", key="q3")
        st.text_input("④ ③によって行われること", key="q4")

    if st.button("① 〜 ④ の答え合わせ", key="check1"):
        check_blank("q1", ["宛先の特定"], "①")
        check_blank("q2", ["ドメイン名"], "②")
        check_blank("q3", ["数値化されたアドレス", "IPアドレス"], "③")
        check_blank("q4", ["識別"], "④")

    st.divider()

    st.subheader("Step 2｜DNSの役割：人間とコンピュータの橋渡し")
    st.markdown("""
人間が利用する「google.com」のようなドメイン名は、コンピュータにとっては理解不能な文字列です。

ドメイン名をコンピュータ用の「IPアドレス」に変換する **⑤　　　** が必要となります。

この仕組みがあることで、人間は複雑な数字を覚えることなく、直感的な名前で
サービスへアクセスすることが可能になります。
""")

    st.text_input("⑤ ドメイン名をIPアドレスに変換する仕組み", key="q5")
    if st.button("⑤ の答え合わせ", key="check5"):
        check_blank("q5", ["DNS", "DomainNameSystem", "DNS（DomainNameSystem）"], "⑤")

    st.markdown("**考えてみよう：なぜ、人間は数字（IPアドレス）を覚える必要がないのでしょうか？**")
    free_answer = st.text_area("あなたの考えを書いてみましょう", key="free1", height=100)
    if st.button("模範解答を見る", key="show_model_answer"):
        st.info("""
        **模範解答例：**
        DNSが自動的にドメイン名をIPアドレスに変換してくれるため。
        人間は「google.com」のような覚えやすい名前を入力するだけでよく、
        裏側でDNSサーバーが対応するIPアドレスを調べて通信先を特定してくれるから。
        """)

    st.divider()

    st.subheader("Step 3｜IPアドレスの種類（用語チェック）")
    st.markdown("インターネット上で世界に一つだけの重複しない住所を何と呼びますか？")
    ans_global = st.radio(
        "選択してください",
        ["グローバルIPアドレス", "プライベートIPアドレス", "サブネットマスク", "デフォルトゲートウェイ"],
        key="global_ip_q",
        index=None,
    )
    if ans_global is not None:
        if ans_global == "グローバルIPアドレス":
            st.success("✅ 正解！グローバルIPアドレスは世界に一つだけの重複しない住所です。")
        else:
            st.error("❌ 正解は「グローバルIPアドレス」です。プライベートIPアドレスはLAN内など限定的な範囲で使われます。")

# ------------------------------------------------------------------
# ③ アクティビティ2：サブネット & TCP/IP
# ------------------------------------------------------------------

elif page == "③ アクティビティ2：サブネット & TCP/IP":
    st.title("🧩 アクティビティ2：サブネットマスク & TCP/IP 4階層モデル")

    st.subheader("Step 1｜サブネットマスクとCIDRの表を完成させよう")
    st.markdown("例：**192.168.11.10 / 20** の場合")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**項目**")
        st.write("CIDR表記")
        st.write("サブネットマスク（10進法）")
        st.write("サブネットマスク（2進法）")
        st.write("割り振れるIP数")
    with col2:
        st.markdown("**あなたの回答**")
        st.text_input("CIDR表記（例が与えられています）", value="/20", disabled=True, key="cidr_given")
        st.text_input("サブネットマスク（10進法）を入力", key="sub_dec")
        st.text_input("サブネットマスク（2進法）を入力", key="sub_bin")
        st.text_input("割り振れるIP数を入力", key="sub_count")

    if st.button("サブネット表の答え合わせ", key="check_subnet"):
        check_blank("sub_dec", ["255.255.240.0"], "サブネットマスク（10進法）")
        check_blank("sub_bin", ["11111111.11111111.11110000.00000000"], "サブネットマスク（2進法）")
        check_blank("sub_count", ["2の12乗", "4096", "4,096"], "割り振れるIP数")
        with st.expander("解説を見る"):
            st.markdown("""
            - `/20` はネットワーク部が20ビットであることを意味します。
            - 32ビット中20ビットがネットワーク部なので、残り **12ビット** がホスト部です。
            - ホスト部12ビット → 2の12乗 = **4,096個** のアドレスが割り振り可能です
              （実際に端末へ割り当てられるのはネットワークアドレス・ブロードキャストアドレスを除いた数）。
            """)

    st.divider()

    st.subheader("Step 2｜TCP/IP 4階層モデルの表を完成させよう")
    st.markdown("役割・機能はヒントとして表示しています。「郵便の例え」の部分を考えて埋めてみましょう。")

    layers = [
        {
            "層": "第4層",
            "名称": "アプリケーション層",
            "役割": "Web(HTTP)やメール(SMTP)等、用途に応じた形式を決定",
            "key": "layer4",
            "answer": ["サービス種別", "メール", "メール(m)"],
        },
        {
            "層": "第3層",
            "名称": "トランスポート層",
            "役割": "信頼性（TCP）や高速性（UDP）を制御。再送確認等を行う",
            "key": "layer3",
            "answer": ["通信確認番号", "24"],
        },
        {
            "層": "第2層",
            "名称": "インターネット層",
            "役割": "送信元・宛先IPを特定し、最適な経路（ルーティング）を選択",
            "key": "layer2",
            "answer": ["郵便番号", "870-0938"],
        },
        {
            "層": "第1層",
            "名称": "ネットワークIF層",
            "役割": "データを電気信号(0,1)に変換。物理的な機器間の受け渡し",
            "key": "layer1",
            "answer": ["経路情報", "国道10号", "県道22号", "K10", "P22"],
        },
    ]

    for layer in layers:
        st.markdown(f"**{layer['層']}：{layer['名称']}**")
        st.caption(f"役割と機能：{layer['役割']}")
        st.text_input(
            f"郵便の例え（{layer['層']}）を入力",
            key=layer["key"],
        )
        st.markdown("")

    if st.button("TCP/IP表の答え合わせ", key="check_layers"):
        for layer in layers:
            check_blank(layer["key"], layer["answer"], f"{layer['層']}（{layer['名称']}）")
        with st.expander("階層モデルの全体図"):
            st.code("""
┌──────────────────────────────┐
│        アプリケーション層     │  … Web、メール、ファイル転送など
├──────────────────────────────┤
│        トランスポート層       │  … TCP（信頼性）、UDP（高速）
├──────────────────────────────┤
│        インターネット層       │  … IP（宛先指定）、ルーティング
├──────────────────────────────┤
│  ネットワークインターフェース層 │  … LAN、Wi-Fi、物理伝送
└──────────────────────────────┘
            """, language=None)

    st.divider()

    st.subheader("Step 3｜データの流れを確認しよう")
    st.markdown("""
パケットが送信側から受信側に届くまでの流れです。空欄に当てはまる層の名前を並べ替えてみましょう。
""")
    order_options = ["アプリケーション層", "トランスポート層", "インターネット層", "ネットワークIF層"]
    st.markdown("**送信側の処理順（上から下へ）**")
    o1 = st.selectbox("1番目に処理される層", order_options, key="order1", index=None, placeholder="選択してください")
    o2 = st.selectbox("2番目に処理される層", order_options, key="order2", index=None, placeholder="選択してください")
    o3 = st.selectbox("3番目に処理される層", order_options, key="order3", index=None, placeholder="選択してください")
    o4 = st.selectbox("4番目に処理される層", order_options, key="order4", index=None, placeholder="選択してください")

    if st.button("送信順の答え合わせ", key="check_order"):
        correct_order = ["アプリケーション層", "トランスポート層", "インターネット層", "ネットワークIF層"]
        user_order = [o1, o2, o3, o4]
        if user_order == correct_order:
            st.success("✅ 正解！データはアプリケーション層→トランスポート層→インターネット層→ネットワークIF層の順にカプセル化されます。")
        elif None in user_order:
            st.warning("すべての選択肢を選んでから答え合わせをしてください。")
        else:
            st.error(f"❌ 正解は次の順番です：{' → '.join(correct_order)}")

# ------------------------------------------------------------------
# ④ 理解度チェック
# ------------------------------------------------------------------

elif page == "④ 理解度チェック":
    st.title("✅ 理解度チェック")
    st.markdown("これまで学んだ内容の確認テストです。5問すべてに答えてから「採点する」を押してください。")

    quiz = [
        {
            "q": "Q1. ネットワーク上でコンピュータ同士が通信する際、実際に使われる「宛先」は次のうちどれですか？",
            "options": ["ドメイン名", "IPアドレス", "会社名", "メールアドレス"],
            "answer": "IPアドレス",
        },
        {
            "q": "Q2. ドメイン名をIPアドレスに変換する仕組みは何ですか？",
            "options": ["HTTP", "DNS", "TCP", "LAN"],
            "answer": "DNS",
        },
        {
            "q": "Q3. LAN内など限定的な範囲でのみ使用されるIPアドレスを何と呼びますか？",
            "options": ["グローバルIPアドレス", "プライベートIPアドレス", "パブリックIPアドレス", "ルートIPアドレス"],
            "answer": "プライベートIPアドレス",
        },
        {
            "q": "Q4. IPアドレスを「ネットワーク部」と「ホスト部」に分けるために使われるものは？",
            "options": ["サブネットマスク", "MACアドレス", "ポート番号", "URL"],
            "answer": "サブネットマスク",
        },
        {
            "q": "Q5. TCP/IPの4階層のうち、送信元・宛先IPを特定し最適な経路を選択するのはどの層ですか？",
            "options": ["アプリケーション層", "トランスポート層", "インターネット層", "ネットワークIF層"],
            "answer": "インターネット層",
        },
    ]

    user_answers = []
    for i, item in enumerate(quiz):
        st.markdown(f"**{item['q']}**")
        ans = st.radio("選択してください", item["options"], key=f"quiz_{i}", index=None, label_visibility="collapsed")
        user_answers.append(ans)
        st.markdown("")

    if st.button("採点する", type="primary"):
        if None in user_answers:
            st.warning("すべての問題に回答してから採点してください。")
        else:
            score = sum(1 for item, ans in zip(quiz, user_answers) if ans == item["answer"])
            st.subheader(f"結果：{score} / {len(quiz)} 問正解")
            st.progress(score / len(quiz))

            if score == len(quiz):
                st.balloons()
                st.success("🎉 満点です！ネットワーク基礎の内容をしっかり理解できています。")
            elif score >= len(quiz) * 0.6:
                st.info("👍 よくできました。間違えた問題は下の解説で復習しましょう。")
            else:
                st.warning("📚 もう一度アクティビティ1・2を復習してから再挑戦してみましょう。")

            with st.expander("答え合わせと解説を見る"):
                for i, (item, ans) in enumerate(zip(quiz, user_answers), start=1):
                    correct = ans == item["answer"]
                    mark = "✅" if correct else "❌"
                    st.markdown(f"{mark} **{item['q']}**")
                    st.markdown(f"あなたの回答：{ans}　／　正解：**{item['answer']}**")
                    st.markdown("---")