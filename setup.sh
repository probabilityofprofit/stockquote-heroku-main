mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[ui]\n\
hide_top_bar = true\n\
\n\
[client]\n\
toolbarMode = \"minimal\"\n\
\n\
[theme]\n\
primaryColor=\"#2214c7\"\n\
backgroundColor=\"#ffffff\"\n\
secondaryBackgroundColor=\"#e8eef9\"\n\
textColor=\"#000000\"\n\
font=\"sans serif\"\n\
" > ~/.streamlit/config.toml
