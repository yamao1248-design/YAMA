import streamlit as st

st.set_page_config(
    page_title="ネットワーク基礎入門：DNSとIPアドレス",
    page_icon="🌐",
    layout="wide",
)

# ------------------------------------------------------------------
# シナリオ設定（このレッスン全体を貫く1つのストーリー）
# ------------------------------------------------------------------
# 「あなたのPC」が「学習ポータルサイト」にアクセスする、という1本の流れを
# 全アクティビティで共有する。前のステップで登場した数字・用語を
# 後のステップで再利用することで、設問同士のつながりを持たせている。

DOMAIN = "www.school-portal.jp"
USER_IP = "192.168.11.10"
CIDR = "/20"
SERVER_IP = "203.0.113.55"

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


def mark_progress(step_key: str):
    """このステップに取り組んだことをsession_stateに記録し、サイドバーの進捗表示に反映する"""
    st.session_state.setdefault("progress", set())
    st.session_state["progress"].add(step_key)


# ------------------------------------------------------------------
# サイドバー：ナビゲーション ＋ シナリオの進み具合（設問間のつながりを可視化）
# ------------------------------------------------------------------

st.sidebar.title("🌐 ネットワーク基礎入門")
page = st.sidebar.radio(
    "セクションを選択",
    [
        "① 学習目標とシナリオ",
        "② アクティビティ1：DNSと名前解決",
        "③ アクティビティ2：サブネット & TCP/IP",
        "④ 理解度チェック",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("対象：ネットワーク基礎を学ぶ初学者\n所要時間：40〜50分")

st.sidebar.markdown("### 🔗 1つのシナリオでつながる5ステップ")
progress = st.session_state.get("progress", set())
flow_steps = [
    ("dns", "1. 宛先を特定する（DNS）"),
    ("iptype", f"2. 自分のIP（{USER_IP}）の種類"),
    ("subnet", f"3. {USER_IP}{CIDR} をサブネット計算"),
    ("layers", "4. 4階層モデルで送信"),
    ("order", "5. 実際の送受信の順番"),
]
for key, label in flow_steps:
    mark = "✅" if key in progress else "⬜"
    st.sidebar.markdown(f"{mark} {label}")
st.sidebar.caption("各ステップは同じ例（あなたのPC → 学習ポータルサイト）で続いています。")

# ------------------------------------------------------------------
# ① 学習目標とシナリオ
# ------------------------------------------------------------------

if page == "① 学習目標とシナリオ":
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

    st.divider()
    st.header("🧭 すべての設問は、この1つのシナリオでつながっています")
    st.info(f"""
**シナリオ**：あなたのPC（IPアドレス `{USER_IP}{CIDR}`）から、
学習ポータルサイト「**{DOMAIN}**」にアクセスしようとしています。
""")

    st.markdown("""
アクティビティ1〜理解度チェックまで、**同じ数字・同じドメイン名**が繰り返し登場します。
前のステップで調べたことが、次のステップの前提になる作りです。
""")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧩 4つのステップのつながり")
        st.markdown(f"""
        1. **DNS**：「{DOMAIN}」の宛先（IPアドレス）を調べる
           → *この結果が②のIPアドレスの話につながる*
        2. **IPアドレスの種類**：あなたのPC（`{USER_IP}`）とサーバーのIPを見分ける
           → *この`{USER_IP}`を③でそのまま使う*
        3. **サブネット計算**：`{USER_IP}{CIDR}` を計算する
           → *この結果が④のインターネット層の理解につながる*
        4. **TCP/IPの4階層**：実際にリクエストを送るときの流れ
           → *この順番が⑤のデータ送受信の並べ替えになる*
        5. **理解度チェック**：1〜4のつながりを踏まえて出題
        """)
    with col2:
        st.subheader("🗺️ 通信全体の流れ")
        st.code(f"""
あなたのPC（{USER_IP}）
   │  ① {DOMAIN} の宛先をDNSで調べる
   ▼
IPアドレスが判明（例：{SERVER_IP}）
   │  ② 自分のIPの種類・所属ネットワークを確認
   ▼
サブネット計算（{USER_IP}{CIDR}）
   │  ③ 4階層モデルでパケットを組み立てる
   ▼
ルーター経由で宛先へ送信
        """, language=None)

    st.success("👉 左のサイドバーから「アクティビティ1」に進みましょう。")

# ------------------------------------------------------------------
# ② アクティビティ1：DNSと名前解決
# ------------------------------------------------------------------

elif page == "② アクティビティ1：DNSと名前解決":
    st.title("🧩 アクティビティ1：DNSと名前解決")
    st.caption(f"シナリオ：あなたのPC（{USER_IP}）が「{DOMAIN}」にアクセスします。")

    st.subheader("Step 1｜通信の起点：宛先の特定")
    st.markdown(f"""
通信を開始する際、最初に行われる最重要ステップは「①　　　」です。

ネットワーク上のコンピュータは②　　　ではなく、③　　　によって相互を④　　　します。

赤字（①〜④）の部分を埋めてください。

*（この後のStep 2で、実際に「{DOMAIN}」というドメイン名がどうやって
「③」の形に変換されるかを見ていきます。）*
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
        st.markdown("→ 次のStep 2では、①〜④で確認した考え方を使って、"
                    f"実際に「{DOMAIN}」がIPアドレスに変換される様子を見ます。")

    st.divider()

    st.subheader("Step 2｜DNSの役割：人間とコンピュータの橋渡し")
    st.markdown(f"""
Step 1で確認した通り、コンピュータは②で答えた「ドメイン名」ではなく、
③で答えた「数値化されたアドレス」を使って通信します。

では、人間が入力する「**{DOMAIN}**」のようなドメイン名は、
どうやって③の形（IPアドレス）に変わるのでしょうか？

ドメイン名をコンピュータ用の「IPアドレス」に変換する **⑤　　　** が必要となります。

この仕組みがあることで、人間は複雑な数字を覚えることなく、直感的な名前で
サービスへアクセスすることが可能になります。
""")

    st.text_input("⑤ ドメイン名をIPアドレスに変換する仕組み", key="q5")
    if st.button("⑤ の答え合わせ", key="check5"):
        result = check_blank("q5", ["DNS", "DomainNameSystem", "DNS（DomainNameSystem）"], "⑤")
        if result:
            mark_progress("dns")
        st.info(f"つまり「{DOMAIN}」は、DNSによって例えば `{SERVER_IP}` のような"
                "IPアドレスに変換されてから通信が始まります。この番号は次のアクティビティでも登場します。")

    st.markdown("**考えてみよう：なぜ、人間は数字（IPアドレス）を覚える必要がないのでしょうか？**")
    st.text_area("あなたの考えを書いてみましょう", key="free1", height=100)
    if st.button("模範解答を見る", key="show_model_answer"):
        st.info("""
        **模範解答例：**
        DNSが自動的にドメイン名をIPアドレスに変換してくれるため。
        人間は「google.com」のような覚えやすい名前を入力するだけでよく、
        裏側でDNSサーバーが対応するIPアドレスを調べて通信先を特定してくれるから。
        """)

    st.divider()

    st.subheader("Step 3｜IPアドレスの種類（用語チェック）")
    st.markdown(f"""
Step 2で「{DOMAIN}」は `{SERVER_IP}` のようなIPアドレスに変換されることがわかりました。

一方、**あなたのPC自身**にも `{USER_IP}` というIPアドレスが割り振られています。

この2つのIPアドレスは、実は種類が異なります。次の問いに答えてください。
""")
    ans_global = st.radio(
        f"インターネット上で世界に一つだけの重複しない住所（{SERVER_IP} のような住所）を何と呼びますか？",
        ["グローバルIPアドレス", "プライベートIPアドレス", "サブネットマスク", "デフォルトゲートウェイ"],
        key="global_ip_q",
        index=None,
    )
    if ans_global is not None:
        if ans_global == "グローバルIPアドレス":
            st.success("✅ 正解！グローバルIPアドレスは世界に一つだけの重複しない住所です。")
            mark_progress("iptype")
        else:
            st.error("❌ 正解は「グローバルIPアドレス」です。プライベートIPアドレスはLAN内など限定的な範囲で使われます。")

        st.markdown(f"""
        では、あなたのPCの `{USER_IP}` はどちらでしょうか？
        `192.168.` から始まるアドレスは、実は**プライベートIPアドレス**（LAN内専用）です。
        つまり、あなたのPC → ルーター（プライベートIP同士のやり取り）→
        ルーターがグローバルIPに変換 → インターネット上のサーバー、という流れになります。

        次の**アクティビティ2**では、この `{USER_IP}{CIDR}` を使って
        サブネット（LANの範囲）を計算していきます。
        """)

# ------------------------------------------------------------------
# ③ アクティビティ2：サブネット & TCP/IP
# ------------------------------------------------------------------

elif page == "③ アクティビティ2：サブネット & TCP/IP":
    st.title("🧩 アクティビティ2：サブネットマスク & TCP/IP 4階層モデル")
    st.caption(f"つながり：アクティビティ1で登場した、あなたのPCのIPアドレス「{USER_IP}」を"
               "ここで使い、さらにデータ送信の流れへとつなげます。")

    st.subheader("Step 1｜サブネットマスクとCIDRの表を完成させよう")
    st.markdown(f"アクティビティ1のStep 3で確認した、あなたのPCのアドレス "
                f"**{USER_IP}{CIDR}** を例に計算してみましょう。")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**項目**")
        st.write("CIDR表記")
        st.write("サブネットマスク（10進法）")
        st.write("サブネットマスク（2進法）")
        st.write("割り振れるIP数")
    with col2:
        st.markdown("**あなたの回答**")
        st.text_input("CIDR表記（アクティビティ1と同じ値です）", value=CIDR, disabled=True, key="cidr_given")
        st.text_input("サブネットマスク（10進法）を入力", key="sub_dec")
        st.text_input("サブネットマスク（2進法）を入力", key="sub_bin")
        st.text_input("割り振れるIP数を入力", key="sub_count")

    if st.button("サブネット表の答え合わせ", key="check_subnet"):
        r1 = check_blank("sub_dec", ["255.255.240.0"], "サブネットマスク（10進法）")
        r2 = check_blank("sub_bin", ["11111111.11111111.11110000.00000000"], "サブネットマスク（2進法）")
        r3 = check_blank("sub_count", ["2の12乗", "4096", "4,096"], "割り振れるIP数")
        if r1 and r2 and r3:
            mark_progress("subnet")
        with st.expander("解説を見る"):
            st.markdown(f"""
            - `{CIDR}` はネットワーク部が20ビットであることを意味します。
            - 32ビット中20ビットがネットワーク部なので、残り **12ビット** がホスト部です。
            - ホスト部12ビット → 2の12乗 = **4,096個** のアドレスが割り振り可能です。
            - つまり `{USER_IP}` は、この4,096個のアドレスからなるLANに所属しています。
              このLANの出口（デフォルトゲートウェイ）を通って、Step 3で見る
              インターネットへの通信が行われます。
            """)

    st.divider()

    st.subheader("Step 2｜TCP/IP 4階層モデルの表を完成させよう")
    st.markdown(f"""
ここからは、あなたのPC（`{USER_IP}`）がアクティビティ1で調べた
「**{DOMAIN}**」へHTTPリクエストを送るときの流れを、4つの層に分けて考えます。

役割・機能はヒントとして表示しています。「郵便の例え」の部分を考えて埋めてみましょう。
""")

    layers = [
        {
            "層": "第4層",
            "名称": "アプリケーション層",
            "役割": f"Webページ（{DOMAIN}）を要求するHTTP形式を決定",
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
            "役割": f"送信元IP（{USER_IP}）・宛先IP（{SERVER_IP}）を特定し、最適な経路を選択",
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
        results = [check_blank(layer["key"], layer["answer"], f"{layer['層']}（{layer['名称']}）") for layer in layers]
        if all(results):
            mark_progress("layers")
        with st.expander("階層モデルの全体図"):
            st.code(f"""
┌──────────────────────────────┐
│        アプリケーション層     │  … {DOMAIN} へのHTTP要求
├──────────────────────────────┤
│        トランスポート層       │  … TCP（信頼性）、UDP（高速）
├──────────────────────────────┤
│        インターネット層       │  … {USER_IP} → {SERVER_IP} への経路選択
├──────────────────────────────┤
│  ネットワークインターフェース層 │  … LAN、Wi-Fi、物理伝送
└──────────────────────────────┘
            """, language=None)

    st.divider()

    st.subheader("Step 3｜データの流れを確認しよう")
    st.markdown(f"""
Step 2で埋めた4つの層は、実際には決まった順番で処理されます。

あなたのPC（`{USER_IP}`）が「{DOMAIN}」へリクエストを送るとき、
Step 2の4つの層がどの順番でヘッダを付与していくか、並べ替えてみましょう。
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
            mark_progress("order")
            st.info(f"この順で信号になったパケットは、{USER_IP} が所属するLANの外へ出るときに"
                    "デフォルトゲートウェイ（ルーター）を通り、Step 1で計算したネットワークの"
                    f"外側にあるサーバー（{SERVER_IP}）まで、経路を選択されながら届けられます。")
        elif None in user_order:
            st.warning("すべての選択肢を選んでから答え合わせをしてください。")
        else:
            st.error(f"❌ 正解は次の順番です：{' → '.join(correct_order)}")

# ------------------------------------------------------------------
# ④ 理解度チェック
# ------------------------------------------------------------------

elif page == "④ 理解度チェック":
    st.title("✅ 理解度チェック")
    st.markdown(f"""
ここまでの「あなたのPC（{USER_IP}）→ {DOMAIN}」というシナリオを振り返りながら、
5問すべてに答えてから「採点する」を押してください。**各問題は前の問題の続きになっています。**
""")

    quiz = [
        {
            "q": f"Q1. あなたのPCが「{DOMAIN}」にアクセスするとき、通信で実際に使われる「宛先」は次のうちどれですか？",
            "options": ["ドメイン名", "IPアドレス", "会社名", "メールアドレス"],
            "answer": "IPアドレス",
            "link": "→ アクティビティ1 Step 1（①〜④）の内容です。",
        },
        {
            "q": f"Q2. Q1で答えた「宛先」を得るために、「{DOMAIN}」というドメイン名を変換する仕組みは何ですか？",
            "options": ["HTTP", "DNS", "TCP", "LAN"],
            "answer": "DNS",
            "link": "→ Q1の答え（IPアドレス）を手に入れる手段が、この問題の答えです。",
        },
        {
            "q": f"Q3. Q2のDNSによって「{DOMAIN}」に対応づけられるアドレス（例：{SERVER_IP}）と、"
                 f"あなたのPCのアドレス（{USER_IP}）を比べたとき、{USER_IP} のようにLAN内など"
                 "限定的な範囲でのみ使用されるIPアドレスを何と呼びますか？",
            "options": ["グローバルIPアドレス", "プライベートIPアドレス", "パブリックIPアドレス", "ルートIPアドレス"],
            "answer": "プライベートIPアドレス",
            "link": f"→ アクティビティ1 Step 3で確認した、{USER_IP} の正体です。",
        },
        {
            "q": f"Q4. Q3の {USER_IP}{CIDR} を「ネットワーク部」と「ホスト部」に分けるために、"
                 "アクティビティ2 Step 1で使ったものは何ですか？",
            "options": ["サブネットマスク", "MACアドレス", "ポート番号", "URL"],
            "answer": "サブネットマスク",
            "link": "→ アクティビティ2 Step 1で計算したサブネット表とつながっています。",
        },
        {
            "q": f"Q5. Q4のサブネット計算をもとに、あなたのPC（{USER_IP}）から"
                 f"{DOMAIN}（{SERVER_IP}）へパケットを送るとき、TCP/IPの4階層のうち"
                 "送信元・宛先IPを特定し最適な経路を選択するのはどの層ですか？",
            "options": ["アプリケーション層", "トランスポート層", "インターネット層", "ネットワークIF層"],
            "answer": "インターネット層",
            "link": "→ アクティビティ2 Step 2・Step 3の4階層モデルの続きです。",
        },
    ]

    user_answers = []
    for i, item in enumerate(quiz):
        st.markdown(f"**{item['q']}**")
        st.caption(item["link"])
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
                st.success("🎉 満点です！DNS→IPアドレス→サブネット→TCP/IPという一連の流れを"
                            "しっかりつなげて理解できています。")
            elif score >= len(quiz) * 0.6:
                st.info("👍 よくできました。間違えた問題は、シナリオのどのステップに対応するか"
                        "下の解説で確認しましょう。")
            else:
                st.warning("📚 もう一度アクティビティ1・2を、同じシナリオの流れで復習してみましょう。")

            with st.expander("答え合わせと、シナリオ全体のつながりを見る"):
                for item, ans in zip(quiz, user_answers):
                    correct = ans == item["answer"]
                    mark = "✅" if correct else "❌"
                    st.markdown(f"{mark} **{item['q']}**")
                    st.markdown(f"あなたの回答：{ans}　／　正解：**{item['answer']}**")
                    st.caption(item["link"])
                    st.markdown("---")

                st.markdown("**🔗 一連の流れの振り返り**")
                st.code(f"""
{DOMAIN} へアクセス
  └─(Q1・Q2) DNSが名前解決 → {SERVER_IP}
       └─(Q3) {USER_IP} はプライベートIP、相手はグローバルIP
            └─(Q4) {USER_IP}{CIDR} をサブネットマスクで計算
                 └─(Q5) インターネット層がIPをもとに経路を選択
                      └─ ルーターを経由して {DOMAIN} へ到達
                """, language=None)