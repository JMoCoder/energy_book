import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"

sp04 = {
  "id": "sp_04",
  "code": "SP4",
  "label": "TOPIC SP4",
  "title": "储能资产投后与运维监督",
  "subtitle": "月报解读·KPI审计·质保索赔·安全与保险风控",
  "color": "#0369A1",
  "gradient": "linear-gradient(135deg,#0369A1,#38BDF8)",
  "sections": 14,
  "words": 70000,
  "hours": 14,
  "chapters": [
    {
      "no": 1,
      "title": "运营数据解码与资产健康度（SoH）审计",
      "sections": [
        {
          "id": "sp4_1_1",
          "file": "sp4_1_1_SCADA_EMS运营月报解读.html",
          "title": "零基础看懂 SCADA / EMS 运营月报：数据采集流向与核心指标提取",
          "difficulty": "🟢",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_1_2",
          "file": "sp4_1_2_RTE系统综合效率损耗拆解.html",
          "title": "RTE（系统综合充放电效率）全链路损耗拆解：变压器、PCS、电池与辅助用电损耗分析",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_1_3",
          "file": "sp4_1_3_电池容量衰减对比质保承诺实务.html",
          "title": "电池容量衰减曲线（SoH）与质保承诺（Warranty）勾稽对比实务",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_1_4",
          "file": "sp4_1_4_DoD_EFCH与电池寿命耗损计算.html",
          "title": "充放电深度（DoD）、等效满充放次数（EFCH）与电池实际耗损计算",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_1_5",
          "file": "sp4_1_5_SOC漂移与电池健康度审计.html",
          "title": "资产健康度审计：SOC 漂移校准失效、单体电压/温差异常与隐患识别",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 2,
      "title": "第三方运维（O&M）与交易代理履约监督",
      "sections": [
        {
          "id": "sp4_2_1",
          "file": "sp4_2_1_运维SLA制定与停机扣罚机制.html",
          "title": "运维服务等级协议（SLA）制定：计划外停机、故障响应与等效可用率（EAF）考核",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_2_2",
          "file": "sp4_2_2_运维成本核算与备件库存审计.html",
          "title": "运维成本核算、备品备件（Spare Parts）库存审计与例行维护 SOP 复核",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_2_3",
          "file": "sp4_2_3_交易代理履约与收益分账审计.html",
          "title": "售电/交易代理团队履约监督：报价策略对赌、偏差考核责任分担与收益分账审计",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 3,
      "title": "设备质保索赔与厂商追责实务",
      "sections": [
        {
          "id": "sp4_3_1",
          "file": "sp4_3_1_电池与PCS质保索赔流程.html",
          "title": "电池与 PCS 硬件质保索赔流程、衰减检测争端与第三方检测机构引入",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_3_2",
          "file": "sp4_3_2_质保尾款扣留与性能保证追缴.html",
          "title": "质保尾款（Holdback）扣留条件、性能保证（Performance Guarantee）违约金追缴",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 4,
      "title": "安全风控检查与保险理赔实务",
      "sections": [
        {
          "id": "sp4_4_1",
          "file": "sp4_4_1_消防安防投后抽查标准.html",
          "title": "储能电站消防安防合规性审计：从预警系统到防爆泄压的投后现场抽查标准",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_4_2",
          "file": "sp4_4_2_储能资产保险配置精析.html",
          "title": "储能资产保险配置：财产险（CAR/EAR）、公众责任险与营业中断险（BI）条款精析",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp4_4_3",
          "file": "sp4_4_3_出险理赔与追偿全流程实务.html",
          "title": "出险理赔实务：现场勘查、定损争议解决与保险公司理赔全流程追偿",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    }
  ]
}

sp05 = {
  "id": "sp_05",
  "code": "SP5",
  "label": "TOPIC SP5",
  "title": "网储项目与基金测算实战",
  "subtitle": "底层项目测算·杠杆财务测算·基金分配模型·估值退出",
  "color": "#B91C1C",
  "gradient": "linear-gradient(135deg,#B91C1C,#F87171)",
  "sections": 17,
  "words": 85000,
  "hours": 17,
  "chapters": [
    {
      "no": 1,
      "title": "项目底层物理-经济测算（零基础起步）",
      "sections": [
        {
          "id": "sp5_1_1",
          "file": "sp5_1_1_物理指标向经济模型转化.html",
          "title": "零基础项目测算入门：如何将 MW / MWh 物理指标转化为资本与收入模型",
          "difficulty": "🟢",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_1_2",
          "file": "sp5_1_2_CAPEX投资成本全拆解.html",
          "title": "CAPEX 投资成本全拆解：电池舱、PCS、变压器、EPC 工程、征地与接入费明细",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_1_3",
          "file": "sp5_1_3_OPEX运营成本与补容预算精算.html",
          "title": "OPEX 运营成本精算：固定运维费、变动运维费、辅助用电、保险与电池补容（Augmentation）预算",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_1_4",
          "file": "sp5_1_4_多商业模式收益模型搭建.html",
          "title": "收益模型搭建：工商业时段差价套利、需量节省、独立储能容量租赁与现货收益计算",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_1_5",
          "file": "sp5_1_5_20年衰减与损耗下现金流推算.html",
          "title": "充放电衰减与 RTE 动态损耗下，20 年逐年收入/成本现金流推算",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 2,
      "title": "带杠杆的项目财务测算（Project Finance）",
      "sections": [
        {
          "id": "sp5_2_1",
          "file": "sp5_2_1_资本结构与债务杠杆测算.html",
          "title": "资本结构与债务杠杆：自筹比例、项目贷款利率、期限与还本付息方式（等额本息/本金）",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_2_2",
          "file": "sp5_2_2_DSCR与最大举债能力测算.html",
          "title": "偿债能力与风控：DSCR（偿债备付率）、LLCR（借款期间偿债备付率）与最大举债能力测算",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_2_3",
          "file": "sp5_2_3_三表联动测算模型搭建.html",
          "title": "资产负债表、损益表与现金流量表（三表联动）测算模型搭建",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_2_4",
          "file": "sp5_2_4_ProjectIRR与EquityIRR杠杆效应.html",
          "title": "Project IRR（项目全投资收益率）与 Equity IRR（资本金收益率）杠杆放大效应与勾稽关系",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_2_5",
          "file": "sp5_2_5_现金流瀑布划扣分层实操.html",
          "title": "项目现金流瀑布（Cash Flow Waterfall）：从营业收入到税后自由现金流（FCFE）的分层划扣",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 3,
      "title": "基金层收益分配与水瀑布测算（Fund Level Model）",
      "sections": [
        {
          "id": "sp5_3_1",
          "file": "sp5_3_1_基金架构设计与J曲线效应.html",
          "title": "基金架构设计：GP / LP 出资结构、认缴/实缴机制与 J 曲线效应（J-Curve Effect）",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_3_2",
          "file": "sp5_3_2_门槛收益率与追赶条款计算.html",
          "title": "门槛收益率（Hurdle Rate / Preferred Return）与追赶条款（Catch-up）计算逻辑",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_3_3",
          "file": "sp5_3_3_美式与欧式Carry水瀑布分配.html",
          "title": "业绩报酬（Carry）提成计算：美式 Waterfall（逐个项目分配）vs 欧洲式 Waterfall（整体基金分配）",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_3_4",
          "file": "sp5_3_4_FundIRR与MOIC动态模型.html",
          "title": "基金层关键指标测算：Fund IRR、MOIC（投资倍数）、DPI、TVPI 动态模型搭建",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 4,
      "title": "敏感性分析、资产估值与退出测算",
      "sections": [
        {
          "id": "sp5_4_1",
          "file": "sp5_4_1_单因素与双因素敏感性分析.html",
          "title": "单因素与双因素敏感性分析：电价差、RTE、衰减率、CAPEX 对 IRR 的冲击测算",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_4_2",
          "file": "sp5_4_2_存量电站DCF与PE估值实操.html",
          "title": "运营期存量电站估值模型：DCF 折现现金流法、市收益率法（P/E）与重置成本法实操",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_4_3",
          "file": "sp5_4_3_资产证券化ABS与REITs测算.html",
          "title": "资产证券化（ABS / 公募 REITs）估值与底层资产发行测算",
          "difficulty": "🔴",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp5_4_4",
          "file": "sp5_4_4_股权转让退出收益分配测算.html",
          "title": "股权转让退出（Trade Sale / Buyout）的收益分配与溢价测算",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    }
  ]
}

sp06 = {
  "id": "sp_06",
  "code": "SP6",
  "label": "TOPIC SP6",
  "title": "储能合规合同与风险管控",
  "subtitle": "核心合同防坑·政策变动应对·产权界定·争议维权",
  "color": "#4C1D95",
  "gradient": "linear-gradient(135deg,#4C1D95,#A78BFA)",
  "sections": 13,
  "words": 65000,
  "hours": 13,
  "chapters": [
    {
      "no": 1,
      "title": "核心商业合同防坑与关键条款精析",
      "sections": [
        {
          "id": "sp6_1_1",
          "file": "sp6_1_1_EMC合同节电量对赌与终止条款.html",
          "title": "EMC 能源管理合同精析：节电量/差价收益对赌、负荷变动保护与提前终止补偿机制",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_1_2",
          "file": "sp6_1_2_容量租赁协议租费与调度条款.html",
          "title": "容量租赁协议防坑指南：租赁费追缴、电网调度优先级保障与违约金追偿条款",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_1_3",
          "file": "sp6_1_3_EPC合同性能保证与违约追费.html",
          "title": "EPC 采购与施工合同：性能保证（Performance Guarantee）、延期赔偿（LDs）与质保留置金",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_1_4",
          "file": "sp6_1_4_OM运维与交易代理协议防坑.html",
          "title": "第三方 O&M 运维与交易代理协议：免责范围、最大赔付上限（Cap）与竞业禁止条款",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 2,
      "title": "政策规制变动与法律风险防护",
      "sections": [
        {
          "id": "sp6_2_1",
          "file": "sp6_2_1_法律与政策变动保护条款精析.html",
          "title": "电价机制调整与容量补偿退坡应对：合同中“法律与政策变动（Change in Law）”防守条款",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_2_2",
          "file": "sp6_2_2_规则突变下的合同救济与调价.html",
          "title": "配储强制政策变动、电力市场交易规则突变下的合同救济与调价机制",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_2_3",
          "file": "sp6_2_3_ESG与电池法案合规冲击.html",
          "title": "ESG、碳足迹（Carbon Footprint）与电池法案等新规对资产合规性的潜在冲击",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 3,
      "title": "土地/产权、网联与监管合规防线",
      "sections": [
        {
          "id": "sp6_3_1",
          "file": "sp6_3_1_土地与屋顶20年长租合规排查.html",
          "title": "屋顶/土地 20 年长租合规性：土地性质、产权瑕疵、优先受偿权与抵押风险排查",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_3_2",
          "file": "sp6_3_2_并网协议与许可法务合规审查.html",
          "title": "供电局并网协议、电力业务许可证与消纳承诺的法务合规审查",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_3_3",
          "file": "sp6_3_3_资产与收益权质押担保合规.html",
          "title": "资产质押、收益权质押与项目融资担保结构的合规性确认",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    },
    {
      "no": 4,
      "title": "典型争议解决、索赔与诉讼案例复盘",
      "sections": [
        {
          "id": "sp6_4_1",
          "file": "sp6_4_1_延期并网责任认定与违约金追偿.html",
          "title": "电站延期并网责任认定与违约金索赔实务",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_4_2",
          "file": "sp6_4_2_实际收益未达预测诉讼维权.html",
          "title": "实际收益未达预测值的诉讼维权与证据链收集",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        },
        {
          "id": "sp6_4_3",
          "file": "sp6_4_3_安全事故责任与代位求偿复盘.html",
          "title": "电站安全事故/热失控后的多方责任划分、保险代位求偿与仲裁案例复盘",
          "difficulty": "🟡",
          "words": 5000,
          "status": "planned"
        }
      ]
    }
  ]
}

def main():
    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc = json.load(f)

    # 移除现有的 sp_04, sp_05, sp_06 如果存在
    levels = [l for l in toc["levels"] if l["id"] not in ("sp_04", "sp_05", "sp_06")]
    levels.extend([sp04, sp05, sp06])
    toc["levels"] = levels

    # 重新计算 meta
    total_sections = 0
    total_words = 0
    total_hours = 0
    for level in levels:
        sec_count = 0
        w_count = 0
        h_count = level.get("hours", 0)
        for ch in level.get("chapters", []):
            for sec in ch.get("sections", []):
                sec_count += 1
                w_count += sec.get("words", 5000)
        level["sections"] = sec_count
        level["words"] = w_count
        total_sections += sec_count
        total_words += w_count
        total_hours += h_count

    toc["meta"]["version"] = "v3.6"
    toc["meta"]["lastUpdated"] = "2026-07-30"
    toc["meta"]["totalSections"] = total_sections
    toc["meta"]["totalWords"] = total_words
    toc["meta"]["totalHours"] = total_hours

    with open(TOC_PATH, "w", encoding="utf-8") as f:
        json.dump(toc, f, ensure_ascii=False, indent=2)

    print(f"Updated toc.json successfully! Total sections: {total_sections}, Total words: {total_words}, Total hours: {total_hours}")

if __name__ == "__main__":
    main()
