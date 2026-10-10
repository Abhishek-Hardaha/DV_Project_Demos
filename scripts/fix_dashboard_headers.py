import glob

files = glob.glob('dashboards/d*.py')
updated = 0

old_sub = 'st.markdown("""\n    <div class="visuals-section-header" style="margin-top:1.5rem;">'
new_sub = 'render_html("""\n    <div class="visuals-section-header" style="margin-top:1.5rem;">'

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    if old_sub in c:
        # Also handle the closing of st.markdown
        c = c.replace(old_sub, new_sub)
        # In the KPI header, the end was """, unsafe_allow_html=True)
        # Let's inspect if there is """, unsafe_allow_html=True) right after this header
        idx = c.find(new_sub)
        end_idx = c.find('""", unsafe_allow_html=True)', idx)
        if end_idx != -1 and end_idx - idx < 300:
            c = c[:end_idx] + '""")' + c[end_idx + len('""", unsafe_allow_html=True)'):]
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(c)
        updated += 1

print(f"Updated {updated} / {len(files)} dashboard files.")
