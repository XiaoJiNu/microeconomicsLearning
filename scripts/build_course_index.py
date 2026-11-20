"""Generate navigation from the real lesson files, so titles and links cannot drift."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1];C=R/'docs/course_20h'
unit_info=[
('选择与经济学模型','1–2','列清可行选择、机会成本与边际变化；辨析模型、证据和价值判断。','无专业先修；用直觉和简单四则运算开始。'),
('分工、贸易与供求','3–4','计算比较优势与互惠区间，解均衡并区分整条曲线和线上一点。','01的机会成本、其他条件不变与读图。'),
('弹性、管制与税负','5–6','从变化幅度判断反应程度，求价格管制与征税后的买卖双方结果。','02的需求、供给和均衡。'),
('交易福利、税收与贸易','7–9','计算剩余、税收收入和无谓损失，比较政策赢家和输家。','02的交易与均衡；03的税收楔子和弹性。'),
('外部性、公共物品与税制','10–12','识别遗漏的社会成本，比较协商、税费和公共治理。','03–04的税负、剩余、效率和分配。'),
('企业成本与竞争生产','13–14','计算成本和利润，判断产量、短期停产和长期退出。','01的边际与机会成本；02的供给；04的剩余。'),
('市场势力与策略','15–17','理解垄断定价、价格歧视、进入与博弈，而非只记市场类型。','06的成本与边际营收；04的福利分析。'),
('要素市场与收入分配','18–20','把产品需求连接到雇佣，解释工资差异与分配测量的限制。','06的生产边际量；07的市场条件；01的证据分析。'),
('消费者选择的机制','21','用预算和偏好解释最优选择，分解价格变化的收入与替代效应。','01的约束；02的需求；只需基础代数，推导就地解释。'),
('信息、集体选择与行为','22','辨析隐藏类型与行动、集体选择困难和行为偏差，完成综合迁移。','前九单元的选择、市场、成本与证据语言。')]
intro='''# 80个问题，建立微观经济学分析能力

这是一条按知识依赖组织的完整课程。每课正文、算例、即时题和推理答案均可直接阅读；不需要先找另一份大课或等待AI临时补正文。

**首次学习从[01-01](unit_01_economic_thinking/01_scarcity_opportunity_cost.md)开始。** 已有诊断，不必重做长诊断。每课核心学习预计10–15分钟；每单元8课按约2小时预留，10单元合计约20小时。时间只是预算，达到“会解释、会计算、能换条件判断”才继续；额外迁移题、分享准备和延迟复习按需增加。

使用[工作簿](workbook.md)记录自己的原始答案。遇到字母查[术语表](../../references/microeconomics_glossary_en_zh.md)，读图看[图形指南](visual_guide.md)。各单元第8课都有综合应用、评分依据及完整费曼分享稿。每天可把当前课的一分钟复述扩成约5分钟分享，不必等到单元结束。

目录由实际课文标题生成；同一概念先建立直觉，再用数字检验，最后处理变化条件。章节为曼昆第8版主题索引，详见[教材说明](../../references/textbook_guide.md)。
'''
parts=[intro];manifest={'version':'2026-09-05-problem-based','budget_minutes':1200,'budget_is_not_mastery':True,'units':[]}
for i,unit in enumerate(sorted(C.glob('unit_*'))):
 title,chapters,goal,prereq=unit_info[i];lessons=[]
 parts.append(f'## {i+1:02d}｜{title}\n\n教材主题：第{chapters}章。**学会：**{goal}\n\n**先修：**{prereq}\n\n[进入单元说明]({unit.name}/README.md)\n\n| 课 | 本课要回答的问题 |\n|---|---|')
 for f in sorted(unit.glob('[0-9][0-9]_*.md')):
  heading=next(x[2:].strip() for x in f.read_text().splitlines() if x.startswith('# '))
  title_only=re.sub(r'^\d+\s*[｜|：:、.．—-]\s*','',heading)
  n=int(f.name[:2]);parts.append(f'| {i+1:02d}-{n:02d} | [{title_only}]({unit.name}/{f.name}) |')
  lessons.append({'id':f'{i+1:02d}-{n:02d}','title':title_only,'path':str(f.relative_to(C)),'core_minutes_range':[10,15],'is_review':n==8})
 parts.append('')
 manifest['units'].append({'id':i+1,'title':title,'textbook_chapters':chapters,'budget_minutes':120,'goal':goal,'prerequisites':prereq,'lessons':lessons})
parts.append('''## 完成后怎样检查

每个单元至少能闭卷解释一个机制，完整完成其综合题，并给出一个条件改变后的判断。评分看推理与单位，不只看最终数字；看过答案后需要独立重做或换题验证。首次通过后进入待复习，安排隔天或更晚的变式题。

课程准备情况见[检查记录](BUILD_REPORT.md)，个人掌握情况只看[学习进度](../00_learning_system/progress.md)。第一轮之后按[能力路线](../../ROADMAP.md)回补具体薄弱处，而非机械重读全部内容。
''')
(C/'README.md').write_text('\n'.join(parts).rstrip()+'\n');(C/'course_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
