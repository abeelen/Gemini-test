import streamlit as st


AMNS_THEME_CSS = """
<style>
:root {
  --amns-primary: #007f7b;
  --amns-primary-soft: #d9efec;
  --amns-bg: #f7faf9;
  --amns-surface: #ffffff;
  --amns-surface-alt: #e7f0ee;
  --amns-text: #18201f;
  --amns-border: #c9ddda;
}

.stApp {
  background-color: var(--amns-bg);
}

.main .block-container {
  padding-top: 1.4rem;
  padding-bottom: 1.8rem;
}

h1, h2, h3 {
  color: var(--amns-text);
}

p, li, label, div[data-testid="stMarkdownContainer"] {
  color: var(--amns-text);
}

div[data-testid="stSidebar"] {
  background-color: var(--amns-surface-alt);
}

div[data-testid="stMetric"] {
  background-color: var(--amns-surface);
  border: 1px solid var(--amns-border);
  border-radius: 0.65rem;
  padding: 0.5rem 0.75rem;
}

.stButton > button {
  border-radius: 0.55rem;
  border: 1px solid var(--amns-primary);
  color: var(--amns-primary);
}

.amns-card {
  background-color: var(--amns-surface);
  border: 1px solid var(--amns-border);
  border-radius: 0.75rem;
  padding: 1rem 1.1rem;
  margin: 0.3rem 0 1rem 0;
}
</style>
"""


def apply_amns_theme():
    st.markdown(AMNS_THEME_CSS, unsafe_allow_html=True)
