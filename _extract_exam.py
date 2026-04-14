# -*- coding: utf-8 -*-
"""Extract exam blocks from 真题-按知识点分类.md for outline notes."""
import re
from pathlib import Path

text = Path("真题题库/真题-按知识点分类.md").read_text(encoding="utf-8")
blocks = re.split(r"(?=\*\*\[来源：)", text)


def strip_subsection_tail(b: str) -> str:
    """Remove trailing ### 单选题/多选题/判断题 and following content (split artifact)."""
    m = re.search(r"\n### (单选题|多选题|判断题)\s*\n", b)
    if m:
        return b[: m.start()].rstrip()
    return b.strip()


def classify_type(b: str) -> str:
    if re.search(r"\n- \*\*[A-D]\.\*\*", b):
        m = re.search(r"【答案】([A-Z]+)", b)
        if m and len(m.group(1)) > 1:
            return "多选题"
        return "单选题"
    return "判断题"


def reformat_block(b: str) -> str | None:
    b = strip_subsection_tail(b)
    if not b.startswith("**[来源"):
        return None
    typ = classify_type(b)
    m = re.match(
        r"\*\*\[来源：([^\]]+)\]\*\*\s*(?:\d+\.\s*)?(.*)", b, re.S
    )
    if not m:
        return None
    src_inner, body = m.group(1), m.group(2).strip()
    header = f"**[来源：{src_inner}] {typ}**"
    if typ == "判断题":
        if "【答案】" in body:
            stem, _, ans = body.partition("【答案】")
            ans = "【答案】" + ans.strip()
            stem = stem.strip()
            stem = re.sub(r"^\d+\.\s*", "", stem)
            return f"{header}\n{stem}\n\n{ans}"
        return f"{header}\n{body}"
    body = re.sub(r"^\d+\.\s*", "", body, count=1)
    return f"{header}\n{body}"


def dedupe(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    out = []
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def section_slice(start_marker: str, end_marker: str | None) -> list[str]:
    lines = text.splitlines(keepends=True)
    start_i = end_i = None
    for i, ln in enumerate(lines):
        if ln.strip() == start_marker:
            start_i = i
        if end_marker and ln.strip() == end_marker and start_i is not None:
            end_i = i
            break
    if start_i is None:
        return []
    chunk = "".join(lines[start_i : end_i if end_i else len(lines)])
    sub_blocks = re.split(r"(?=\*\*\[来源：)", chunk)
    out = []
    for b in sub_blocks[1:]:
        b = b.strip()
        if b.startswith("**[来源"):
            r = reformat_block(b)
            if r:
                out.append(r)
    return dedupe(out)


def match_02(b: str) -> bool:
    if "不是IPD的主流程" in b:
        return True
    if "集成产品开发模式把产品策划和产品立项都看作为投资行为" in b:
        return True
    if "集成产品开发模式在项目管理上的重大变革" in b:
        return True
    if "集成产品开发模式把项目管理分为了哪些方面" in b:
        return True
    if "技术评审" in b or "决策评审" in b or "规格书评审" in b:
        return True
    if "IPMT" in b or "IPD" in b or "PDT" in b:
        return True
    return False


def keep_03_from_09(b: str) -> bool:
    """Economics / cost accounting from section 09 only."""
    if "电话系统呼叫" in b:
        return False
    if "集成产品开发模式把产品策划和产品立项都看作为投资行为" in b:
        return False
    if "IPMT流程第二阶段的输出成果是什么" in b or "IPMT流程第二阶段的输出成果是" in b:
        return False
    if "IPMT是指" in b:
        return False
    if "IPMT职责不包括" in b:
        return False
    if "新产品开发的启动和终结" in b:
        return False
    if "在IPD模式的流程中，哪个阶段开始产品正式立项" in b:
        return False
    if "将新产品开发作为技术型决策，而非投资性决策" in b:
        return False
    if "产品开发评审主要有什么评审" in b:
        return False
    if "公司决策评审不包含" in b:
        return False
    if "PDT计划阶段的主要工作内容不包括" in b:
        return False
    if "PDT团队的作用包括哪些方面" in b:
        return False
    incl = [
        "成本",
        "会计",
        "定价",
        "损益",
        "临界点",
        "工程经济学",
        "资源的合理利用",
        "投资回报率",
        "产品具有双重属性",
        "技术创新方式",
        "若通过专利检索",
        "黑箱",
        "集成产品开发模式中引入了平台",
        "优化成本是经济决策",
        "技术重用",
        "作业成本法认为",
        "产品变动成本管理",
        "管理会计理论中生产模式",
        "不属于作业成本法优点",
        "变动成本法的优点",
        "作业成本法的优点",
        "管理会计主要是对产品进行财务管理",
        "降低产品变动成本是财务部门",
        "产品变动成本是与产品紧密联系",
        "完全成本法按经济用途将成本分为",
        "同产品生产有关的消耗都应计入产品成本",
        "完全成本法的理论依据",
        "产品策划阶段最重要的工作",
    ]
    return any(x in b for x in incl)


def collect_blocks(predicate) -> list[str]:
    out = []
    for b in blocks[1:]:
        b = strip_subsection_tail(b.strip())
        if not b.startswith("**[来源"):
            continue
        if not predicate(b):
            continue
        r = reformat_block(b)
        if r:
            out.append(r)
    return dedupe(out)


KW01 = [
    "产品开发",
    "生命周期",
    "测试验证",
    "市场调研",
    "产品策划",
    "产品规划",
    "产品设计",
    "黑箱",
    "产品平台",
    "系统级平台",
    "客户需求",
    "产品全成本",
    "开发成本",
    "原始创新",
    "集成创新",
    "改进创新",
    "技术创新方式",
    "商业机会",
    "专利检索",
    "专利避让",
    "双重属性",
    "技术属性",
    "经济属性",
    "管理报表的使用者是企业外部",
    "不能只追求技术先进性",
    "产品设计开发流程中如果发现自己的核心技术",
    "交叉许可",
    "专利应对",
    "面向产品全生命周期的管理与服务优化",
    "产品设计反馈优化场景",
]


def match_01(b: str) -> bool:
    if not any(k in b for k in KW01):
        return False
    # drop pure wireless false positives
    bad = [
        "PC5-U协议栈",
        "Uu口控制面协议",
        "QoS流到DRB映射",
        "NR层二子层",
        "5G SA场景下，Uu口",
    ]
    if any(x in b for x in bad):
        return False
    return True


STRONG_05 = [
    "覆盖",
    "干扰",
    "切换",
    "RSRP",
    "RSRQ",
    "SINR",
    "路测",
    "A3",
    "链路预算",
    "巡检",
    "运维",
    "告警",
    "KPI",
    "越区",
    "弱覆盖",
    "导频污染",
    "重叠覆盖",
    "过覆盖",
    "异频测量",
    "A2",
    "机器学习",
    "集成学习",
    "随机森林",
    "Bagging",
    "网络优化",
    "智能网络优化",
    "训练集",
    "验证集",
    "测试集",
    "NodeBSpider",
    "uem5000",
    "资源调度",
    "邻区漏配",
    "SSB软调",
    "硬调方位角",
    "硬调方位角和下倾角",
    "mod3",
    "mod 3",
    "mod（ ）",
    "MR弱覆盖",
    "覆盖率优化",
    "AI赋能5G",
    "机器翻译",
    "异常检测",
    "流量预测",
    "PCI mod",
    "SS-SINR",
    "EPS Fallback",
    "Xn链路切换",
]


def match_05(b: str) -> bool:
    return any(k in b for k in STRONG_05)


KW04_EXTRA = [
    "BBU",
    "AAU",
    "方位角",
    "下倾角",
    "PCI",
    "组网",
    "GPS",
    "光模块",
    "天线",
    "安装",
    "RRU",
    "NCGI",
    "HBPOF",
    "HSCTD",
    "EMB6216",
    "EMB6116",
    "单模",
    "集束光纤",
    "DCPD",
    "室分",
    "皮站",
    "飞站",
    "前传",
    "本地小区建立",
    "商用基站必须添加的路由",
    "NSA组网",
    "SA组网随机接入",
    "子帧配比",
    "SSB波束",
    "700M组网",
    "2.6G组网",
    "3.5G组网",
    "100M带宽组网",
    "最大支持的 PRB",
    "PRB为",
    "单小区最大支持",
    "Option 3",
    "Option 2",
]


def match_04_extra(b: str) -> bool:
    if not any(k in b for k in KW04_EXTRA):
        return False
    # avoid pure optimization / handover unless install-related
    if match_05(b) and not any(
        k in b
        for k in [
            "BBU",
            "AAU",
            "安装",
            "GPS",
            "PCI取值范围",
            "NCGI",
            "方位角规划",
            "子帧配比",
            "SSB",
            "组网采用",
            "EMB",
            "HBPOF",
            "HSCTD",
            "室分",
            "皮站",
        ]
    ):
        return False
    return True


KW_ISAC = [
    "激光雷达",
    "毫米波雷达",
    "车联网是实现自动驾驶的必要条件",
    "智能网联汽车环境感知传感器",
    "车联网中，环境感知主要包括",
    "关于摄像头、激光雷达、毫米波雷达",
    "毫米波雷达是一种重要的ADAS传感器",
    "关于激光雷达说法正确的是",
    "SLAM",
    "Lidar SLAM",
    "VisualSLAM",
    "6G将具备的感知功能",
    "数字李生",
]

KW_SAT = [
    "卫星",
    "NTN",
    "星地",
    "LEO",
    "GEO",
    "天通",
    "轨道",
    "静止卫星",
    "地球站",
    "超低轨道",
    "C-6G",
    "Mate60",
    "Mate 60",
    "Mate60Pro",
    "卫星通话",
    "卫星移动通信",
    "卫星互联网",
    "数字卫星通信",
    "卫星电话",
    "多普勒频移",
    "多径效应和多普勒",
]

KW_V2X = [
    "V2X",
    "C-V2X",
    "C−V2X",
    "PC5",
    "RSU",
    "OBU",
    "车联网",
    "车路协同",
    "V2V",
    "V2I",
    "V2P",
    "BSM",
    "LTE-V2X",
    "NR-V2X",
    "DSRC",
    "协同服务类应用",
    "智慧交通系统",
    "车用通信系统",
    "17 个一期应用",
    "5905",
    "5925",
]

KW_COMP = [
    "MEC",
    "边缘计算",
    "移动边缘计算",
    "数字孪生",
    "算力",
    "资源与算力层",
    "支持边缘计算",
    "工业互联网平台",
    "边缘计算：适用于",
]


def build_intro() -> str:
    return (
        "## 相关真题\n\n"
        "> 以下真题摘自 `真题题库/真题-按知识点分类.md`，含完整选项与标准答案。\n\n"
    )


def merge_lists(*lists: list[str]) -> list[str]:
    return dedupe([x for lst in lists for x in lst])


def main():
    out_dir = Path("_exam_extract")
    out_dir.mkdir(exist_ok=True)

    b01 = collect_blocks(match_01)
    b02 = collect_blocks(match_02)

    lines = text.splitlines(keepends=True)
    si = ei = None
    for i, ln in enumerate(lines):
        if ln.strip() == "## 09-工程概论基础":
            si = i
        if ln.strip() == "## 其他-通信基础" and si is not None:
            ei = i
            break
    if si is None:
        raise SystemExit("missing ## 09-工程概论基础")
    chunk09 = "".join(lines[si : ei if ei else len(lines)])
    for b in re.split(r"(?=\*\*\[来源：)", chunk09)[1:]:
        b = strip_subsection_tail(b.strip())
        if b.startswith("**[来源") and keep_03_from_09(b):
            r = reformat_block(b)
            if r:
                b03.append(r)
    b03 = dedupe(b03)

    s07 = section_slice("## 07-5G基站产品及解决方案", "## 08-人工智能与机器学习")
    s05_head = section_slice("## 05-5G网络节能技术", "## 06-5G接入网协议与信令")
    s05_aa = [x for x in s05_head if "AAU" in x and "功耗" in x]
    b04_extra = collect_blocks(match_04_extra)
    b04 = merge_lists(s07, s05_aa, b04_extra)

    b05 = collect_blocks(match_05)
    s08 = section_slice("## 08-人工智能与机器学习", "## 09-工程概论基础")
    b08_opt = [
        x
        for x in s08
        if any(
            k in x
            for k in [
                "5G",
                "网络",
                "优化",
                "集成学习",
                "随机森林",
                "决策树",
                "机器学习",
                "训练",
                "验证",
                "测试集",
                "AI",
            ]
        )
    ]
    b05 = merge_lists(b05, b08_opt)
    s07_maint = [
        x
        for x in s07
        if any(
            k in x
            for k in ["巡检", "日常维护", "告警分析", "指标监控", "AC校准", "网络运维"]
        )
    ]
    b05 = merge_lists(b05, s07_maint)

    bisac = collect_blocks(lambda b: any(k in b for k in KW_ISAC))
    bsat = collect_blocks(lambda b: any(k in b for k in KW_SAT))
    bv2 = collect_blocks(lambda b: any(k in b for k in KW_V2X))
    bcomp = collect_blocks(lambda b: any(k in b for k in KW_COMP))

    outputs = {
        "01-产品开发全生命周期.md": b01,
        "02-工程项目管理.md": b02,
        "03-经济决策分析.md": b03,
        "04-产品设计及规划部署.md": b04,
        "05-网络运维及优化.md": b05,
        "01-通感一体化技术应用.md": bisac,
        "02-星地融合技术应用.md": bsat,
        "03-C-V2X技术应用.md": bv2,
        "04-通算一体化技术应用.md": bcomp,
    }

    base = Path("大纲对照-本科A组")
    for fname, lst in outputs.items():
        body = build_intro() + "\n\n---\n\n".join(lst) + "\n"
        (out_dir / fname.replace(".md", "_body.md")).write_text(body, encoding="utf-8")
        # patch target file
        if "通感" in fname or "星地" in fname or "C-V2X" in fname or fname.startswith(
            "04-通算"
        ):
            sub = base / "三-创新应用(20%)" / fname
        else:
            sub = base / "二-工程思维(40%)" / fname
        if not sub.exists():
            print("missing", sub)
            continue
        doc = sub.read_text(encoding="utf-8")
        start = doc.index("## 相关真题")
        end = doc.index("## 参考资源")
        new_doc = doc[:start] + body + "\n" + doc[end:]
        sub.write_text(new_doc, encoding="utf-8")
        print(fname, len(lst))

    print("patched ok")


if __name__ == "__main__":
    main()
