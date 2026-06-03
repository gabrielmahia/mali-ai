import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Mali AI — Jenga Utajiri Wako", page_icon="📈", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0e08;color:#e8f5e9}
.mali-card{background:#0d1f0d;border:1px solid #1b5e20;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#2e7d32;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = """Wewe ni mshauri wa fedha na uwekezaji Kenya. Jibu kwa Kiswahili rahisi.
MUHIMU: Kila wakati sema hii si ushauri wa fedha rasmi — ni elimu tu.
Toa maelezo ya jumla kuhusu: NSE, Hazina bonds, SACCOs, akiba, na uwekezaji wa busara.
Sisitiza hatari za uwekezaji wowote. Usipendekeze hisa maalum."""

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 📈 Mali AI")
st.markdown("**Jenga Utajiri Wako Kenya — Elimu ya Fedha kwa Kiswahili**")
st.caption("⚠️ Habari za elimu tu. Si ushauri wa uwekezaji rasmi. Shauriana na mshauri wa fedha aliyeidhinishwa.")

tab1,tab2,tab3,tab4 = st.tabs(["📊 NSE & Hisa","🏦 Akiba & SACCO","🇰🇪 Hazina Bonds","💡 Mwanzo wa Uwekezaji"])

with tab1:
    nse_q = st.selectbox("Swali la NSE:", [
        "NSE ni nini na inafanya kazi vipi Kenya?",
        "Jinsi ya kununua hisa NSE kwa mara ya kwanza",
        "Hatari za kununua hisa ni zipi?",
        "Dividends — maana yake na jinsi ya kupokea",
        "Index fund vs hisa moja — nini bora kwa mwanzo?",
        "Jinsi ya kufuatilia hisa zangu",
    ])
    if st.button("📊 Niambie NSE", key="nse_btn"):
        with st.spinner("..."): result = ask(nse_q)
        st.markdown(f'<div class="mali-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    income = st.number_input("Mshahara wako wa mwezi (KES):", value=30000, step=5000)
    savings_q = st.selectbox("Swali lako:", [
        "Ninapaswa kuweka akiba ngapi kwa mwezi?",
        "SACCO bora Kenya — jinsi ya kujiunga",
        "Tofauti kati ya SACCO na benki",
        "M-Shwari, KCB M-Pesa, Fuliza — nini bora?",
        "Jinsi ya kuvunja mzunguko wa kukopwa",
    ])
    if st.button("🏦 Niambie", key="sav_btn"):
        with st.spinner("..."): result = ask(f"Mtu ana mshahara wa KES {income:,}/mwezi. {savings_q} Toa ushauri wa vitendo na wa kiwango chake cha mapato.")
        st.markdown(f'<div class="mali-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    bond_q = st.selectbox("Swali la Hazina Bonds:", [
        "Hazina bonds ni nini — jinsi inavyofanya kazi",
        "Jinsi ya kununua Kenya Government Bond",
        "Infrastructure bonds — zinatofautianaje na bonds nyingine?",
        "Ni kiasi gani kidogo ninachoweza kuwekeza?",
        "Hatari za Hazina bonds Kenya ni zipi?",
    ])
    if st.button("🇰🇪 Habari za Bonds", key="bond_btn"):
        with st.spinner("..."): result = ask(bond_q + " Kenya National Treasury. Toa habari ya kisasa.")
        st.markdown(f'<div class="mali-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab4:
    age = st.selectbox("Umri wako:", ["18-25","26-35","36-45","46-55","55+"])
    goal = st.selectbox("Lengo lako:", ["Akiba ya dharura (emergency fund)","Kununua nyumba","Elimu ya watoto","Kustaafu vizuri","Kuanzisha biashara"])
    if st.button("💡 Plan Yangu ya Mali", key="plan_btn"):
        with st.spinner("..."): result = ask(f"Mtu wa umri {age} Kenya ana lengo: {goal}. Toa mpango rahisi wa hatua kwa hatua wa kufikia lengo hili. Toa muda, kiasi kinachohitajika kwa mwezi, na njia za uwekezaji zinazofaa.")
        st.markdown(f'<div class="mali-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("📈 Mali AI v1.0 | NSE: nse.co.ke | Capital Markets: cma.or.ke | Si ushauri rasmi | CC BY-NC-ND 4.0")
