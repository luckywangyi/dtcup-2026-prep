# -*- coding: utf-8 -*-
"""Parse 大唐杯 LaTeX exam files into structured data and Markdown outputs."""
import re
import os
from collections import defaultdict

TEX_DIR = r"C:\Users\wps\大唐杯备赛资料\真题原始tex"
OUT_DIR = r"C:\Users\wps\大唐杯备赛资料\真题题库"

FILES = [
    "ch0.tex", "ch01.tex", "ch02.tex", "ch1.tex", "ch2.tex", "ch3.tex",
    "ch4.tex", "ch5.tex", "ch6.tex", "ch7.tex", "ch8.tex", "ch9.tex",
]

CATEGORIES = [
    ("01-卫星网络架构及接口", [
        "NTN", "非地面网络", "星地", "天地一体", "馈电链路", "服务链路",
        "透明转发", "再生转发", "Bent-Pipe", "feeder", "ISL", "星间链路",
        "卫星网络", "卫星架构", "NTN网关", "卫星接口",
    ]),
    ("02-卫星产品分类及轨道", [
        "卫星", "LEO", "MEO", "GEO", "HAPS", "低轨", "中轨", "高轨", "同步轨道",
        "天通", "Mate60", "Mate 60", "卫星电话", "卫星通信", "卫星互联网",
        "卫星移动", "C频段", "L频段", "GPS定位", "北斗", "静止卫星", "赤道",
        "通信卫星", "地球站", "地面站", "卫星锁定", "数字卫星",
    ]),
    ("03-卫星通信空口技术", [
        "多普勒", "时延补偿", "星历", "GNSS", "波束切换", "NR NTN",
        "卫星空口", "超低轨", "6G超低",
    ]),
    ("04-通感技术应用及架构", [
        "通感", "ISAC", "感知", "雷达", "通感一体", "5G-A", "5G Advanced",
        "Release 18", "R18", "HMCPB", "HMCPC", "低空", "无人机探测",
    ]),
    ("05-5G网络节能技术", [
        "节能", "符号关断", "通道关断", "载波关断", "深度休眠", "极致休眠",
        "AAU功耗", "功耗", "SON", "自组织", "自配置", "自优化", "自愈",
    ]),
    ("06-5G接入网协议与信令", [
        "RRC", "SRB", "DRB", "随机接入", "SIB", "MIB", "寻呼", "Handover",
        "Initial UE", "重建", "INACTIVE", "INACTVE", "测量报告", "PRACH",
        "MSG4", "MSG3", "竞争", "T300", "Xn链路切换", "SN Status",
        "切换", "注册管理", "NAS", "N1", "系统消息", "OSI", "Type0-PDCCH",
        "Type1-PDCCH", "RRC连接建立", "RRC Setup", "RRC Reject", "resume",
        "SCG", "PSCell", "MRDC", "B1事件", "EPS Fallback", "Qoffsettemp",
        "AMF", "SMF", "UPF", "NG-C", "NG-U", "N11", "NSA", "SA组网", "独立组网",
        "非独立", "CU", "DU", "网络切片", "NRF", "核心网", "gNB", "EN-DC",
        "Option3", "Option7", "NFV", "软硬件解耦", "PDU会话", "QoS流", "DRB映射",
        "NCGI", "QoS flow", "NG口", "SCTP", "GTP", "UDN", "PCF", "UDR",
        "网络架构描述", "服务化", "毫米波", "FR1", "FR2", "子网掩码", "30位掩码",
        "IPV4",
        "帧结构", "时隙", "子帧", "SCS", "子载波", "OFDM", "PDSCH", "PDCCH",
        "PBCH", "PSS", "SSS", "PCI", "CORESET", "CCE", "REG", "DMRS", "DM-RS",
        "CSI-RS", "SSB", "SS/PBCH", "PRB", "BWP", "调制", "Polar", "QPSK",
        "256QAM", "1024QAM", "ZC序列", "无线帧", "CORESET0", "PUCCH", "SRS",
        "PTRS", "PCFICH", "栅格", "Raster", "OffsetToPointA", "RBG", "Format0",
        "长PRACH", "NZC", "半帧", "符号", "μ", "mu", "Normal CP", "扩展 CP",
        "Massive MIMO", "mMTC", "eMBB", "uRLLC", "新空口", "NR ", "NR中", "NR系统",
        "NR帧", "NR协议", "物理信道", "物理信号", "加密算法", "nea",
        "V2X", "C-V2X", "PC5", "BSM", "MEC", "车联网", "V2V", "V2I", "V2N",
        "V2P", "RSU", "OBU", "DSRC", "LTE-V2X", "NR-V2X", "路云", "车路",
        "弱势交通", "高精地图", "协同", "Mode1", "Mode2", "Mode3", "Mode4",
        "5905", "5925", "直连通信频率", "V2C",
        "覆盖", "干扰", "路测", "链路预算", "传播模型", "自由空间", "规划",
        "优化", "越区", "弱覆盖", "重叠覆盖", "功率控制",
        "阴影衰落", "快衰落", "慢衰落", "A3事件", "切换参数",
        "RSRP", "RSRQ", "SINR", "渗透率", "深度覆盖", "天线权值",
        "路损", "阴影效应", "密集城区",
    ]),
    ("07-5G基站产品及解决方案", [
        "大唐", "BBU", "AAU", "HBPOD", "HBPOF", "EMB61", "LMT", "uem5000",
        "GPS", "DCPD", "HDPSD", "HSCTD", "光模块", "光纤", "槽位", "接地",
        "电源线", "空面板", "理线架", "巡检", "OSP", "NodeBSpider", "LmtAgent",
        "板卡", "RRU", "64TR", "降质", "通道故障", "172.27",
        "升级", "/ata", "黄绿接地", "集束光纤", "物理ID列表", "方位角", "下倾角",
        "TDAU", "Pinsite", "Slsite", "室分", "皮站", "飞站",
    ]),
    ("08-人工智能与机器学习", [
        "决策树", "随机森林", "Bagging", "Boosting", "AdaBoost", "GBDT",
        "过拟合", "信息增益", "基尼", "集成学习", "机器学习", "数据收集",
        "数据清洗", "特征工程", "数据建模", "训练集", "验证集", "测试集",
        "Xgboost", "lightGBM", "pasting", "stacking", "Voting", "CART",
        "ID3", "C4.5", "梯度下降", "弱分类器", "强学习器", "cart树",
        "Gradient Boosting", "智能网络优化调参", "F1", "RMSE", "MSE", "R2",
        "模型评估", "神经网络", "深度学习", "CNN", "RNN", "LSTM",
        "AI", "人工智能", "物联网数据",
    ]),
    ("09-工程概论基础", [
        "IPMT", "IPD", "专利", "产品成本", "变动成本", "固定成本", "全成本",
        "损益", "交叉许可", "专利避让", "黑箱测试", "决策评审", "技术评审",
        "产品平台", "集成产品开发", "销售价格", "技术重用", "管理会计",
        "财务会计", "完全成本法", "临界点", "产品立项", "产品策划", "物料申请",
        "规格书评审", "IPD模式", "新产品规划建设", "新产品立项批准",
        "经济属性", "技术属性", "性价比", "创新", "原始创新", "集成创新",
        "安全规划", "防静电", "MPO", "上塔", "工程经济学", "作业成本",
        "IAM", "ACM", "CLF", "ANC", "电话系统", "蜂窝移动",
        "IP地址分", "电信网", "传输设备",
    ]),
    ("其他-通信基础", []),
]


def clean_latex(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    s = re.sub(r"%.*", "", s)
    s = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\kaishu\s*", "", s)
    s = re.sub(r"\\faIcon\{[^}]*\}\s*", "", s)
    s = re.sub(r"\\color\{[^}]*\}\s*", "", s)
    s = re.sub(r"\\;+", " ", s)
    s = re.sub(r"\\quad", " ", s)
    s = re.sub(r"\\qquad", "  ", s)
    s = re.sub(r"\$\s*\\mu\s*\$", "μ", s)
    s = re.sub(r"\$([^$]+)\$", r"\1", s)
    s = re.sub(r"\\_", "_", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def classify_question(stem: str) -> str:
    text = stem
    for cat, kws in CATEGORIES[:-1]:
        for kw in kws:
            if kw in text:
                return cat
    return CATEGORIES[-1][0]


def section_label(st: str) -> str:
    if "单选" in st:
        return "单选题"
    if "多选" in st:
        return "多选题"
    if "判断" in st:
        return "判断题"
    return "其他"


def parse_file(path: str):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    chapter_m = re.search(r"\\chapter\{([^}]+)\}", raw)
    exam_title = chapter_m.group(1).strip() if chapter_m else os.path.basename(path)

    section_starts = [(m.start(), section_label(m.group(1))) for m in re.finditer(r"\\section\{([^}]+)\}", raw)]

    def section_at(idx: int) -> str:
        cur = "其他"
        for pos, lab in section_starts:
            if pos < idx:
                cur = lab
            else:
                break
        return cur

    questions = []
    abs_pos = 0
    choice_re = re.compile(
        r"\\begin\{choice\}\{([^}]*)\}\s*\[\s*\](.*?)\\end\{choice\}", re.DOTALL
    )
    while True:
        m = choice_re.search(raw, abs_pos)
        if not m:
            break
        choice_idx = m.start()
        ans_raw = m.group(1).strip()
        body = m.group(2)
        abs_pos = m.end()

        section = section_at(choice_idx)

        tasks_m = re.search(
            r"\\begin\{tasks\}\([^)]*\)(.*?)\\end\{tasks\}", body, re.DOTALL
        )
        stem = body
        options = []
        if tasks_m:
            stem = body[: tasks_m.start()] + body[tasks_m.end() :]
            task_block = tasks_m.group(1)
            for tm in re.finditer(
                r"\\task\s*([^\n\\]*(?:\n(?![\\])[^\n\\]*)*)", task_block
            ):
                opt = clean_latex(tm.group(1))
                if opt:
                    options.append(opt)
            # 容错：\task 后无空格如 \task3.5G
            if not options:
                for tm in re.finditer(r"\\task([^\n\\]+)", task_block):
                    opt = clean_latex(tm.group(1))
                    if opt:
                        options.append(opt)

        stem = clean_latex(stem)
        answer = clean_latex(ans_raw)
        if answer in ("正确", "错误"):
            qtype = "判断"
        elif len(answer) > 1 or (answer and answer not in "ABCD"):
            qtype = "多选"
        else:
            qtype = "单选"

        cat = classify_question(stem + " " + " ".join(options))
        questions.append(
            {
                "exam": exam_title,
                "section": section,
                "qtype": qtype,
                "stem": stem,
                "options": options,
                "answer": answer,
                "category": cat,
            }
        )
    return exam_title, questions


def format_options_marked(opts, answer: str, qtype: str):
    labels = "ABCDEFGHIJKLMNOP"
    lines = []
    if qtype == "判断":
        mark = "✓ " if answer == "正确" else ""
        lines.append(f"【答案】{mark}{answer}")
        return "\n".join(lines)
    correct_set = set()
    if qtype == "单选" and answer and len(answer) == 1:
        correct_set.add(answer.upper())
    elif qtype == "多选":
        for c in re.sub(r"\s+", "", answer.upper()):
            if c in "ABCDEFGHI":
                correct_set.add(c)
    for i, o in enumerate(opts):
        lab = labels[i] if i < len(labels) else str(i + 1)
        mark = " ✓" if lab in correct_set else ""
        lines.append(f"- **{lab}.** {o}{mark}")
    if qtype == "多选":
        lines.append(f"【答案】{answer}")
    elif qtype == "单选":
        lines.append(f"【答案】{answer}")
    return "\n".join(lines)


def normalize_for_dup(s: str) -> str:
    s = s.replace("与", "和").replace("及", "和")
    s = re.sub(r"\s+", "", s)
    for ch in "，。、；：""''（）()":
        s = s.replace(ch, "")
    return s[:120]


def main():
    all_q = []
    by_exam = {}
    for fn in FILES:
        path = os.path.join(TEX_DIR, fn)
        if not os.path.isfile(path):
            continue
        title, qs = parse_file(path)
        by_exam[fn] = title
        all_q.extend(qs)

    # Per-category ordering for file1
    cat_order = [c[0] for c in CATEGORIES]
    by_cat = defaultdict(list)
    for q in all_q:
        by_cat[q["category"]].append(q)

    # Number within each category across all exams
    lines1 = ["# 大唐杯真题 — 按知识点分类\n", "本文档由 LaTeX 源文件自动解析生成。\n"]
    for cat in cat_order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines1.append(f"\n## {cat}\n")
        for sec_name in ("单选题", "多选题", "判断题"):
            sub = [q for q in items if q["section"] == sec_name]
            if not sub:
                continue
            lines1.append(f"\n### {sec_name}\n")
            for i, q in enumerate(sub, 1):
                src = q["exam"]
                lines1.append(
                    f"\n**[来源：{src}]** {i}. {q['stem']}\n"
                )
                lines1.append(format_options_marked(q["options"], q["answer"], q["qtype"]))
                lines1.append("")

    out1 = os.path.join(OUT_DIR, "真题-按知识点分类.md")
    with open(out1, "w", encoding="utf-8") as f:
        f.write("\n".join(lines1))

    # 题干规范化后完全相同的题目视为重复（避免跨卷选项顺序不同导致答案字母错位）
    stem_map = defaultdict(list)
    for q in all_q:
        key = normalize_for_dup(q["stem"])
        if len(key) >= 12:
            stem_map[key].append(q)

    deduped = []
    seen = set()
    for key, lst in stem_map.items():
        exams = {x["exam"] for x in lst}
        if len(exams) < 2:
            continue
        if key in seen:
            continue
        seen.add(key)
        # 取字典序最前的试卷中的原题，保证选项顺序与【答案】字母一致
        rep = sorted(lst, key=lambda x: x["exam"])[0]
        deduped.append((rep, sorted(exams)))

    deduped.sort(key=lambda x: -len(x[1]))

    lines2 = ["# 大唐杯真题 — 高频重复题\n", "下列题目在**多套试卷**中以相同或高度相似题干出现，建议优先记忆。\n"]
    for rep, exams in deduped[:200]:
        lines2.append(f"\n### 出现试卷：{'；'.join(exams)}\n")
        lines2.append(f"{rep['stem']}\n")
        lines2.append(format_options_marked(rep["options"], rep["answer"], rep["qtype"]))
        lines2.append("")

    out2 = os.path.join(OUT_DIR, "真题-高频重复题.md")
    with open(out2, "w", encoding="utf-8") as f:
        f.write("\n".join(lines2))

    # Multi-choice only with analysis
    multi = [q for q in all_q if q["qtype"] == "多选"]
    by_cat_m = defaultdict(list)
    for q in multi:
        by_cat_m[q["category"]].append(q)

    def analyze_multi(q):
        opts = q["options"]
        ans = re.sub(r"\s+", "", q["answer"].upper())
        correct = [c for c in ans if c in "ABCDEFGHI"]
        labels = "ABCDEFGHIJKLMNOP"[: len(opts)]
        wrong = [labels[i] for i in range(len(opts)) if labels[i] not in correct]
        ok_txt = "、".join(correct) if correct else ""
        bad_txt = "、".join(wrong) if wrong else ""
        return (
            f"官方标答为 **{q['answer'].strip()}**（选项 {ok_txt} 已用 ✓ 标出）。"
            f"多选题常见失分原因是漏选或误选近似表述：错误项 {bad_txt} 往往存在“张冠李戴”（网元/接口/参数）、"
            f"“绝对化措辞”或与 3GPP/工程规范不一致之处，复习时请回到教材原文逐条对照。"
        )

    lines3 = ["# 大唐杯真题 — 易错多选题（含简要辨析）\n", "按知识点模块归类；**✓** 表示官方答案中的正确选项。\n"]
    for cat in cat_order:
        items = by_cat_m.get(cat, [])
        if not items:
            continue
        lines3.append(f"\n## {cat}\n")
        for i, q in enumerate(items, 1):
            lines3.append(f"\n**[来源：{q['exam']}]** {i}. {q['stem']}\n")
            lines3.append(format_options_marked(q["options"], q["answer"], "多选"))
            lines3.append(f"\n**辨析：** {analyze_multi(q)}\n")

    out3 = os.path.join(OUT_DIR, "真题-易错多选题.md")
    with open(out3, "w", encoding="utf-8") as f:
        f.write("\n".join(lines3))

    print("Parsed questions:", len(all_q))
    print("Multi:", len(multi))
    print("Duplicate groups:", len(deduped))
    print("Written:", out1, out2, out3)


if __name__ == "__main__":
    main()
