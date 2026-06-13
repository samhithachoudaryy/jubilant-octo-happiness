```python
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="News Dashboard", layout="wide")

st.title("📰 News Dashboard")

# Sidebar
st.sidebar.header("Filters")

api_key = st.sidebar.text_input("NewsAPI Key", type="password")

keyword = st.sidebar.text_input("Keyword Search")

country = st.sidebar.selectbox(
    "Country",
    {
        "India": "in",
        "USA": "us",
        "UK": "gb",
        "Australia": "au"
    }
)

num_articles = st.sidebar.slider(
    "Number of Articles",
    5,
    50,
    10
)

# Fetch News
def get_news(api_key, keyword, country, page_size):

    if keyword.strip():
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": keyword,
            "pageSize": page_size,
            "language": "en",
            "apiKey": api_key
        }
    else:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": country,
            "pageSize": page_size,
            "apiKey": api_key
        }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    st.error(f"API Error: {response.text}")
    return None


if st.button("Get News"):

    if not api_key:
        st.warning("Please enter your API key")
        st.stop()

    data = get_news(
        api_key,
        keyword,
        country,
        num_articles
    )

    if data and data.get("articles"):

        articles = data["articles"]

        records = []

        for article in articles:

            title = article.get("title", "")
            source = article.get("source", {}).get("name", "")
            url = article.get("url", "")
            desc = article.get("description", "")

            records.append({
                "Title": title,
                "Source": source,
                "URL": url
            })

            st.subheader(title)
            st.write(f"**Source:** {source}")

            if desc:
                st.write(desc)

            st.markdown(f"[Read Article]({url})")

            st.divider()

        df = pd.DataFrame(records)

        st.subheader("Results Table")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No news found.")
```
