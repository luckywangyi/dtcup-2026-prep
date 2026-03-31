# Day 5：5G信令流程（真题高频模块）

> 来源：GitHub真题(第九~十二届) + CSDN仿真笔记

## 一、系统消息体系 [高频考点]

### MIB vs SIB1

| | MIB | SIB1 |
|---|-----|------|
| 承载信道 | PBCH（在SSB中） | PDSCH |
| 广播方式 | **周期广播** | **周期广播** |
| 主要内容 | SFN、SCS配置、**如何获取SIB1** | RACH配置、TDD配置、其他SIB调度 |

> **反复出现的真题**：MIB一个最重要作用是通知UE如何获取哪个消息？→ **B. SIB1** [第九届A组、B组均考]

> **真题多选**：5G系统中哪些系统消息一定是周期广播？→ **AD: MIB和SIB1** [第十届A组]

> **真题多选**：5G NR系统中最小系统消息包括？→ **BD: MIB和SIB1** [第九届A组]

### MIB包含内容 [真题多选-第十届A组]

> **真题多选**：MIB消息中包含哪些内容？→ **AB**
> - A. 系统帧号 ✓
> - B. SIB1的PDCCH CORESET配置 ✓
> - ~~C. 小区ID~~ ✗（由PSS/SSS获取）
> - ~~D. PHICH配置~~ ✗（LTE概念）

### SIB2内容 [真题多选-第九届A组]

> **真题多选**：SIB2主要包含？→ **BCD**
> - B. 小区重选系统内异频相关信息 ✓
> - C. 小区异系统重选公共消息 ✓
> - D. 小区重选系统内同频公共信息 ✓
> - ~~A. 同频小区专用重选消息~~ ✗

### OSI广播方式 [真题-第十届A组]

> **真题原题**：OSI是采用周期广播还是订阅是通过哪条系统消息通知UE的？→ **B. SIB1** [第十届A组]

---

## 二、随机接入流程（RACH）[高频考点]

### 四步竞争随机接入

```
UE                        gNB
 |== Msg1: Preamble ===→  |  (PRACH)
 |←= Msg2: RAR =========  |  (PDSCH, 含TA+TC-RNTI+UL Grant)
 |== Msg3: RRC Setup Req →|  (PUSCH)
 |←= Msg4: 竞争解决 =====  |  (PDSCH)
```

### 竞争 vs 非竞争随机接入 [真题多选-反复考]

| 场景 | 随机接入类型 |
|------|-------------|
| **初始接入（IDLE态）** | **竞争** |
| **无线链路失败后初始接入** | **竞争** |
| **上行失步+无SR资源** | **竞争** |
| **切换** | **非竞争** |
| **波束失败恢复** | **非竞争** |

> **真题多选**：哪种情形下只能进行基于竞争的随机接入？→ **ACD** [第九届A组]
> - A. 无线链路失败后进行初始接入 ✓
> - C. 由Idle状态进行初始接入 ✓
> - D. Active下上行数据到达无上行同步无SR资源 ✓
> - ~~B. 切换时进行随机接入~~ ✗（切换可以非竞争）

> **真题多选**：非竞争随机接入的场景？→ **ACD: 波束失败恢复、切换等** [第十届A组]

> **真题判断**：切换过程的随机接入可以采用非竞争也可以采用竞争方式 → **正确** [第十届A组]

---

## 三、RRC状态 [高频考点]

### 三种RRC状态 [真题多选-反复考]

| 状态 | 说明 |
|------|------|
| **RRC_IDLE** | 空闲态，无连接 |
| **RRC_INACTIVE** | 非活跃态（5G新增），保留上下文 |
| **RRC_CONNECTED** | 连接态 |

> **真题多选**：5G NR中RRC状态包括？→ **RRC CONNECTED, RRC IDLE, RRC INACTIVE**
> ~~RM DEREGISTERED / RM REGISTERED~~ 是NAS层状态，不是RRC状态 [第九届A/B组反复考]

### RRC INACTIVE恢复 [反复出现的真题]

> **真题原题（几乎每届都考）**：RRC INACTIVE状态如果要恢复业务，则会触发哪条信令？
> → **RRC resume request** [第九届A组、B组、第十届A组均考]

### RRC重建触发原因 [真题多选-第九届B组]

> **真题多选**：5G RRC连接重建触发原因？→ **全选ABCD**
> - A. 切换失败 ✓
> - B. 重配失败 ✓
> - C. 完保失败 ✓
> - D. 基站检测RLF ✓

### RRC重建时基站行为 [真题-第九届A组]

> **真题原题**：RRC重建流程，若UE上下文不能被恢复但有资源，基站会触发？→ **A. RRC Setup** [第九届A组]
> **真题原题**：若基站拒绝UE重建和新建？→ **D. RRC Reject** [第九届B组]

---

## 四、NAS注册与初始接入信令 [真题考点]

### 基站到核心网第一条消息

> **反复出现的真题**：在5G NR网络中终端初始接入过程中，基站向核心网发的第一条信息是？
> → **B. Initial UE Message** [第九届A/B组均考]

### NSA场景信令 [真题-第九届A组]

> **真题原题**：5G NR NSA中，哪个信令可以携带SCG Add或PSCell Change相关SCG配置？
> → **LTE侧的RRCConnectionReconfiguration** [第九届A/B组、第十届A组均考]

### NSA场景测量上报 [真题-第十届A组]

> **真题原题**：NSA场景下SRB3未建立时，SCG测量结果UE通过什么消息上报？
> → **A. UL Information Transfer MRDC** [第十届A组]

---

## 五、5G寻呼 [真题多选-第十届A组]

> **真题多选**：关于5G寻呼说法正确的？→ **ABC**
> - A. PO是一套PDCCH监听机会，由多个子帧或OFDM符号组成 ✓
> - B. 一个PF里可有多个PO ✓
> - C. 一个PO的长度等于一个波束扫描周期 ✓
> - ~~D. 在每个波束上发送的Paging消息不一样~~ ✗

> **真题判断**：UE在RRC IDLE态和RRC INACTIVE态的寻呼标识为P-RNTI → **错误** [第九届A组]

---

## 六、EN-DC场景SRB [真题多选-第九届B组]

> **真题多选**：5G EN-DC下可以建立哪些SRB类型？→ **全选ABCD: SRB0/SRB1/SRB2/SRB3**

---

## 七、QoS Flow与DRB [真题多选-第九届B组]

> **真题多选**：关于QoS Flow与DRB关系正确的是？→ **ABC**
> - A. 多个QoS Flow映射一个DRB ✓
> - B. DRB保证QoS Flow空口质量 ✓
> - C. 一个QoS Flow映射一个DRB ✓
> - ~~D. 一个QoS Flow可以映射多个DRB~~ ✗

---

## 八、5G缩短时延的技术 [真题多选-第九届B组]

> **真题多选**：哪些关键技术起到了缩短时延的作用？→ **全选ABCD**
> - A. RRC-inactive状态 ✓（快速恢复）
> - B. MEC网络架构 ✓（边缘计算）
> - C. 自包含帧结构 ✓（同时隙反馈）
> - D. Shorter-TTI ✓（更短传输时间间隔）

---

## 九、T300定时器 [真题多选-第十届A组]

> **真题多选**：NR中T300定时器说法正确的？→ **CD**
> - C. 在接收到RRC Setup或RRC Reject消息后停止 ✓
> - D. 在发送RRC Setup Request时启动 ✓

---

## 今日真题自测（15题）

1. MIB最重要作用是通知UE获取什么？（SIB1）
2. MIB和SIB1是否都周期广播？（是）
3. MIB包含小区ID吗？（不包含，由PSS/SSS获取）
4. RRC INACTIVE恢复用什么信令？（RRC resume request）
5. 5G有几种RRC状态？（3种：IDLE/INACTIVE/CONNECTED）
6. 初始接入用竞争还是非竞争随机接入？（竞争）
7. 切换时用什么随机接入？（可竞争可非竞争）
8. 基站向核心网发的第一条消息？（Initial UE Message）
9. NSA中携带SCG配置的信令？（LTE侧RRCConnectionReconfiguration）
10. RRC连接建立建的是SRB几？（SRB1）
11. 最小系统消息包括？（MIB和SIB1）
12. 一个QoS Flow能映射多个DRB吗？（不能）
13. RRC重建可以因为什么触发？（切换失败/重配失败/完保失败/RLF）
14. 5G缩短时延的技术？（RRC-inactive/MEC/自包含帧/Shorter-TTI）
15. T300定时器什么时候启动？（发送RRC Setup Request时）
