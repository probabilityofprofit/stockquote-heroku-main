mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]\n\
primaryColor = '#eb4034'\n\
backgroundColor = '#021d24'\n\
secondaryBackgroundColor = '#B9F1C0'\n\
textColor = '#FFFFFF'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml
