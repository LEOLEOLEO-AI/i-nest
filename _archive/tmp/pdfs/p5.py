
# ═════════════════════ Ch6: 联系方式 ═════════════════════
story.append(h2("六、联系方式"))
story.append(body(
    'iNEST探索团队正在开放招收博士研究生、博士后和访问学者。'
    '我们也欢迎跨机构的联合研究合作，涵盖理论、仿真、工程、应用等各个层面。',
    "bni"))
story.append(make_callout(
    '<font face="' + FONT_SANS + '"><b>署名</b>：iNEST探索团队</font><br/>'
    '<font face="' + FONT_SANS + '"><b>研究方向</b>：物理复杂网络智能涌现——'
    '软件定义互连（SDI）与晶上系统（SDSoW）</font>'
))
story.append(body('具体联系方式请关注相关学术平台获取团队信息。', "bni"))
story.append(sp(4*mm))
story.append(HRFlowable(CONTENT_W))

# Footer
story.append(Paragraph(
    '<font face="' + FONT_SANS + '"><b>"这不是在已有路线上做更好，这是开辟一条新路线。"</b></font>',
    S["footer"]))
story.append(Paragraph("来和我们一起，把这条路走出来。", S["footer"]))
story.append(Paragraph(
    '因为有些事情，只靠一群人中的一个人是做不成的——它需要一群人，而且必须是"对的人"。',
    S["footer"]))
story.append(Paragraph("如果你觉得自己可能就是对的人，请联系我们。", S["footer"]))
story.append(sp(3*mm))
story.append(Paragraph("iNEST探索团队 · 2026年6月", S["footer"]))

# ═════════════════════ BUILD ═════════════════════
print("Building PDF with " + str(len(story)) + " flowables...")
doc.build(story)
size_kb = os.path.getsize(OUTPUT_PATH) / 1024
print("PDF generated: " + OUTPUT_PATH)
print("Size: " + str(int(size_kb)) + " KB")