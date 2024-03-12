mkdir -p ~/.streamlit/

echo "\
[theme]
base="light"
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
