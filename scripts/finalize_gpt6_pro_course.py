#!/usr/bin/env python3
"""One-time, branch-scoped publisher for already authored course objects.

This script never updates main and refuses a forced or stale branch update.
It is removed from the published tree; the ordinary validator is retained.
"""
from __future__ import annotations
import base64
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

REPO = 'XiaoJiNu/microeconomicsLearning'
BRANCH = 'gpt6-pro'
BASELINE = '2b6ac7218b2e089ed4d302892c49323aae988edb'
AUTHORED_TREE = '48fec452dade38290974179a6b3ffe67f7d73306'
PREFIX = 'docs/course_gpt6_pro/'
TOKEN = os.environ.get('GITHUB_TOKEN')
if not TOKEN:
    raise SystemExit('GITHUB_TOKEN is required; no credentials are printed.')
if os.environ.get('GITHUB_REPOSITORY', REPO) != REPO:
    raise SystemExit('Refusing to run in another repository.')


def api(path: str, method: str = 'GET', payload: dict | None = None):
    url = 'https://api.github.com/repos/' + REPO + '/' + path
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'gpt6-pro-course-publisher'}
    if data is not None:
        headers['Content-Type'] = 'application/json; charset=utf-8'
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if method == 'GET' and exc.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** (attempt + 1))
                continue
            detail = exc.read().decode('utf-8', errors='replace')[:1000]
            raise RuntimeError(f'{method} {path}: HTTP {exc.code}: {detail}') from exc
    raise RuntimeError('Unexpected exhausted retry loop')


def blob_text(sha: str) -> str:
    item = api('git/blobs/' + sha)
    if item.get('encoding') != 'base64':
        raise RuntimeError('Unexpected blob encoding')
    return base64.b64decode(item['content']).decode('utf-8')


head = api('git/ref/heads/' + BRANCH)['object']['sha']
authored = api('git/trees/' + AUTHORED_TREE + '?recursive=1')
if authored.get('truncated'):
    raise SystemExit('Authored tree is truncated; refusing incomplete publication.')
entries = {x['path']: x for x in authored['tree'] if x['type'] == 'blob'}
course_paths = sorted(p for p in entries if p.startswith(PREFIX))
expected_lessons = {f'{PREFIX}u{u:02d}/{l:02d}.md' for u in range(1, 11) for l in range(1, 11)}
if not expected_lessons.issubset(entries):
    raise SystemExit('The authored tree does not contain all 100 lessons.')

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    contents = dict(zip(course_paths, pool.map(lambda p: blob_text(entries[p]['sha']), course_paths)))

# Correct two editorial issues without changing the surrounding lesson.
p = PREFIX + 'u05/10.md'
contents[p] = contents[p].replace('超过 10000 的部分税率 20。', '超过 10000 的部分税率 20%。')
p = PREFIX + 'u09/04.md'
contents[p] = contents[p].replace(
    '在同样价格与 U=xy 下，预算增为 160，求最优组合。再比较原预算下 A=(4,4) 与 B=(6,3)，解释为何“总件数更多”不一定更受偏好。',
    '在同样价格与 U=xy 下，预算增为 160，求最优组合。再比较原预算120下 B=(6,3) 与 C=(10,1)，核对两者支出与效用，解释为何“总件数更多”不一定更受偏好。')
contents[p] = contents[p].replace(
    'y=x/2，10x+20y=160，得 x=8、y=4。原预算下 A 花120、U=16，B 花120、U=18，所以 B 更好，尽管 A 总件数8、B9在本例也不同；总件数一般不是效用指标。可再比较 (10,1) 总件数11但 U=10，更直接看出件数更多不代表更好。',
    'y=x/2，10x+20y=160，得 x=8、y=4。原预算120下，B=(6,3)支出60+60=120，U=18，总件数9；C=(10,1)支出100+20=120，U=10，总件数11。虽然C的总件数更多，这个消费者仍偏好B。商品的组合与偏好很重要，不能用简单相加的件数替代效用排序。')

OPENSTAX = 'https://openstax.org/books/principles-economics-3e/pages/'
CORE = 'https://books.core-econ.org/the-economy/microeconomics/'
source_groups = [
('u01', '选择与方法', [('个人选择与预算约束', '2-1-how-individuals-make-choices-based-on-their-budget-constraint')]),
('u02', '比较优势与供需', [('绝对优势与比较优势', '33-1-absolute-and-comparative-advantage'), ('供给、需求与均衡', '3-1-demand-supply-and-equilibrium-in-markets-for-goods-and-services'), ('第3章总结', '3-key-concepts-and-summary')]),
('u03', '弹性与政策', [('需求与供给价格弹性', '5-1-price-elasticity-of-demand-and-price-elasticity-of-supply'), ('弹性与定价', '5-3-elasticity-and-pricing'), ('其他弹性', '5-4-elasticity-in-areas-other-than-price'), ('价格限制基础', '3-key-concepts-and-summary')]),
('u04', '福利与贸易', [('供需与效率', '3-5-demand-supply-and-efficiency'), ('贸易保护与分配', '34-key-concepts-and-summary'), ('贸易基础', '33-1-absolute-and-comparative-advantage')]),
('u05', '外部性与公共部门', [('污染的经济学', '12-1-the-economics-of-pollution'), ('外部性与政策工具', '12-key-concepts-and-summary'), ('公共物品', '13-3-public-goods')]),
('u06', '生产、成本与竞争', [('生产成本与行业结构', '7-introduction-to-production-costs-and-industry-structure'), ('短期成本', '7-3-costs-in-the-short-run'), ('长期成本', '7-5-costs-in-the-long-run'), ('竞争企业的产出决策', '8-2-how-perfectly-competitive-firms-make-output-decisions')]),
('u07', '市场势力与博弈', [('垄断与进入壁垒', '9-1-how-monopolies-form-barriers-to-entry'), ('垄断的产量与价格', '9-2-how-a-profit-maximizing-monopoly-chooses-output-and-price'), ('垄断竞争', '10-1-monopolistic-competition'), ('寡头', '10-2-oligopoly')]),
('u08', '劳动与分配', [('劳动市场理论', '14-1-the-theory-of-labor-markets'), ('不完全竞争劳动市场', '14-2-wages-and-employment-in-an-imperfectly-competitive-labor-market'), ('收入不平等测量', '15-4-income-inequality-measurement-and-causes')]),
('u09', '消费者选择', [('消费选择', '6-1-consumption-choices'), ('价格和收入变化', '6-2-how-changes-in-income-and-prices-affect-consumption-choices'), ('无差异曲线', 'b-indifference-curves')]),
('u10', '信息、集体选择与行为', [('不完全与不对称信息', '16-1-the-problem-of-imperfect-information-and-asymmetric-information'), ('保险与信息', '16-2-insurance-and-imperfect-information'), ('集体决策的局限', '18-3-flaws-in-the-democratic-system-of-government'), ('行为经济学', '6-3-behavioral-economics-an-alternative-viewpoint')])]
source_text = '''# 来源与核对口径

[课程地图](README.md) · [覆盖范围](SCOPE.md)

编写与网页核对日期：2026-09-05。章节范围沿用原仓库曼昆《经济学原理》第8版微观分册第1—22章；以下公开教材支持概念核对，各自章节号不与曼昆混用。教学正文、例子、短题、解析与分享参考重新编写，不复制原书整章或题库。

所有价格、税率、工资、收益和风险数值均为教学假设，不是当前市场数据、现行法律或用户个人财务记录。具体算例由课程自行构造，来源提供概念背景，不代表使用同一个数字例子。计算回归不等于现实因果验证，网页核对日期也不保证链接永久有效。

## 总体参考

'''
source_text += f'- [OpenStax, Principles of Economics 3e]({OPENSTAX}1-introduction)\n'
source_text += f'- [CORE Econ, The Economy 2.0: Microeconomics，目录]({CORE}0-3-contents.html)\n'
source_text += f'- [CORE主题索引：机会成本、约束选择与博弈]({CORE}0-7-features-list.html)\n'
notes = {
'u01': '模型与机会成本服务于具体问题。因果示例用于解释反事实，不宣称简单前后差足以识别因果；宏观段落只界定范围。',
'u02': '比较曲线上移动和整条关系移动。不同时间的均衡点连线不能直接当作需求曲线。',
'u03': '需求弹性按用途区别带符号值与绝对值。税补贴由两种净价格与楔子联立，局部弹性比例不无限外推。',
'u04': '福利图使用明确小国、世界价格给定等假设。资金转移、资源消耗、国内与全球范围分别核算。',
'u05': '外部成本需要区分平均与边际。许可交易的付款不是额外资源成本；分档税与NPV参数为假设。',
'u06': '自编TC=100+10q+q²的AVC单调上升，不硬套别处U形图。平均成本最低点与MC关系需相应条件。',
'u07': '统一定价下MR不同于售价。博弈矩阵与重复收益为思想实验，不据此判断现实企业违法，也不提供实际价格协调操作。',
'u08': 'VMPL与MRPL的区别依赖产品市场条件。工资公式不是人的社会价值，最低工资效果需市场结构与经验证据。',
'u09': 'Slutsky三点分解为本课自行演算，保持旧组合在新价下买得起，不等同于Hicks恒效用补偿。切点不是所有偏好的万能解。',
'u10': '隐藏类型与隐藏行动分别分析。行为效应强度受情境影响，损失侧系数2只是演示，不是普遍心理常数。一次课堂选择不能诊断人格。'}
for uid, title, links in source_groups:
    source_text += f'\n<a id="{uid}"></a>\n## {uid.upper()} {title}\n\n'
    for label, suffix in links:
        source_text += f'- [OpenStax：{label}]({OPENSTAX}{suffix})\n'
    if uid == 'u07':
        source_text += f'- [CORE：企业与顾客总结]({CORE}07-firm-and-customers-13-summary.html)\n'
    if uid == 'u08':
        source_text += f'- [CORE：企业与员工总结]({CORE}06-firm-and-employees-15-summary.html)\n'
    if uid in ('u01', 'u09'):
        source_text += f'- [CORE：相关主题索引]({CORE}0-7-features-list.html)\n'
    source_text += '\n' + notes[uid] + '\n'
source_text += '\n## 维护\n\n新增现实案例须记录事件与资料日期、变量口径、可反驳条件和可核验来源；不把整章或未获授权图表搬入仓库。失效链接保留原标题并寻找出版社替代入口。\n'
contents[PREFIX + 'SOURCES.md'] = source_text

contents[PREFIX + 'CAPSTONE.md'] = '''# 全课综合考核：建模、核算、解释与边界

[课程地图](README.md) · [工作簿](WORKBOOK.md) · [术语](GLOSSARY.md)

先保存独立答案，再展开解析。十组各十分，共一百分，可以分次完成。每组按建模与结果4分、机制3分、条件边界2分、术语单位1分评价。概念题不因没有公式扣分；计算题不能只报数字。

首次80分及以上，且机会成本、私人/社会成本、收入/利润、价格/MR等关键区分没有根本性错误，可记为待复习。延迟变式仍能完成，再判断掌握。材料文件齐全不等于个人已经通过。

## 01 相关成本

已付3000元，其中退出可退800。继续占用一段时间，未来价值2500；退出后该时间最佳替代用途净价值2000。无其他费用。比较当前方案，指出沉没部分。

<details><summary>解析01</summary>

继续未来得到2500；退出得到退款800和替代价值2000，共2800，退出优势300。不可退2200为沉没部分。等价写法2500−2000−800=−300，不能再扣全部3000或重复扣时间机会成本。真实选择还需风险和非金钱价值，本题假定价值可比。
</details>

## 02 供需与识别

需求Q_d=120−2P，供给Q_s=−30+3P。求均衡。材料成本上升使供给变为−50+3P，需求不变，再求均衡。为什么不能将其称为需求曲线左移？

<details><summary>解析02</summary>

原120−2P=−30+3P，P=30、Q=60。新120−2P=−50+3P，P=34、Q=52。供给左移使价格提高，消费者沿原需求线减少需求量，需求关系本身未变。应明确市场、时期和单位，现实中还要验证成本冲击与其他条件。
</details>

## 03 弹性与经营结果

同一需求关系上，价格20变25，销量100变80。计算中点需求价格弹性和总收入变化。每件可变成本6、固定成本不变，收入扣可变成本后的余额如何变？

<details><summary>解析03</summary>

均值价格22.5、数量90，带符号弹性=(-20/90)/(5/22.5)=−1，大小1。收入均2000。原可变成本600、余额1400；新可变成本480、余额1520，增加120。收入不变不等于利润不变，区间弹性也不能直接代表所有价格范围。
</details>

## 04 税与福利

需求P_d=50−0.5Q，供给P_s=10+0.5Q，单位税8。求数量、两种价格、消费者剩余、生产者剩余、税收与无谓损失，并说明税款与净损失的差别。

<details><summary>解析04</summary>

税楔子40−Q=8，Q=32，买方价34、卖方净价26。CS=0.5×16×32=256，PS=256，税收=256，总剩余768。原总剩余800，无谓损失32，也等于0.5×8×8。税收主要向政府转移，基础净损失来自取消的正净收益交易；征管成本与公共支出作用另计。
</details>

## 05 外部性与物品分类

边际收益100−Q，私人边际成本20+Q，边际外部成本10。求私人量、社会量与理想化矫正税。解释公开代码与拥挤算力为何不应一概视为同一种公共物品问题。

<details><summary>解析05</summary>

私人量40；社会成本30+Q，社会量35；在损害已知和执行有效等条件下，税10对齐激励。代码复制通常近似非竞争，算力使用会挤占容量；能否排除未授权使用另看技术和规则。数字化或免费并不自动定义公共物品。
</details>

## 06 成本、生产与退出

TC=100+10q+q²，竞争价格22，固定100本期不能避免。求最优正产量、利润与停产结果。下期可完全退出时，需要重新检查什么？

<details><summary>解析06</summary>

MC=10+2q，q=6。收入132，可变成本96，总成本196，利润−64；停产亏100，生产少亏36。本例利润凹，候选与零产量已经比较。下期固定费用、合同、残值、重启条件可能改变，不能无限沿用本期不可避免成本。该成本结构最低平均总成本为30，长期价格22不能覆盖全部经济成本。
</details>

## 07 定价与博弈

统一定价需求P=120−2Q，TC=80+40Q。求边际收入、最优数量、价格、利润，以及相对边际有效率数量的无谓损失。再解释纳什均衡为什么不保证整体最好。

<details><summary>解析07</summary>

TR=120Q−2Q²，MR=120−4Q，MC=40，得到Q=20、P=80。收入1600、成本880、利润720。价格等于边际成本对应有效率量40，无谓损失0.5×20×40=400；相同固定费用一致扣除不改变差额。纳什均衡检验给定他人策略时单方面偏离能否改善，不要求共同改变不能更好。
</details>

## 08 劳动与分布

产品价格20，新增三位工人的边际产量10、8、6，工资170，满足价格接受条件时应雇几位？若第二位对应产品MR=15，其MRPL是多少？收入5、5、20、贫困线8，求均值、中位数、贫困率。

<details><summary>解析08</summary>

VMPL为200、160、120，仅第一位覆盖工资170，选一位。第二位MRPL=15×8=120，不等于VMPL160。均值10、中位数5、贫困率2/3。工资公式不是个人社会价值，分布分析需统一人群、时期和税前后口径。
</details>

## 09 消费者选择

U=xy，预算160，价格10和20。X降到5，其他不变。求旧点、新点、Slutsky补偿收入和中间点，并给出X、Y的两条效应。

<details><summary>解析09</summary>

旧点(8,4)，新点(16,4)。旧组合在新价下支出120，补偿预算下最优(12,3)。X替代+4、收入+4、合计+8；Y替代−1、收入+1、合计0。保持旧组合仍买得起，不是效用固定；必须检验内部解与偏好形状，不能原样套用完全替代情形。
</details>

## 10 跨模型分析

某工程服务计划提价。客户事前难识别质量，合同后难观察维护努力。负责人只搜集支持提价的故事，并用过去投入很大证明应该扩张。写一页分析，含主体与替代、需求成本证据、信息类型、治理及成本、行为偏差、分配与不能直接推出的投资结论。

<details><summary>解析10与参考结构</summary>

先区分提价、扩容和合同三个决定。需求证据应排除客户构成与共同变化，成本区分新增可避免支出和不可回收历史支出。隐藏质量可能导致逆向选择，可考虑可信测试担保；隐藏努力可能导致道德风险，需要另外设计监督、报酬和风险分担。这些措施都要计执行成本。

确认偏误和沉没成本误用是题目提示的可能问题，不构成人格诊断；应事先写出反对原判断的可观察指标。定价要比较MR和MC，并核对利润、边界和实际交付能力，不能只看价格或销量。员工、客户和企业影响可能不同，效率与分配分开。技术或盈利机制不自动证明股票值得以任意价格购买，财务、估值、风险和预期仍需研究。
</details>

## 延迟变式与成果

将01退款改为不可退，04改为正外部性补贴，06改为部分固定费停产可免，09改为完全替代偏好。先说明哪个条件改变，再计算，不只换数字。保留原始、纠错、延迟答案，不能用正确答案覆盖原错误。

个人成果应包括一张知识图、一份答卷与纠错、一段约五分钟讲解、一页带假设和证据缺口的案例分析。本次编写课程并未替你完成这些个人学习证据。
'''

unit_specs = [
('u01','经济学思维',[1,2]),('u02','分工与供需',[3,4]),('u03','弹性与政策',[5,6]),
('u04','福利与贸易',[7,8,9]),('u05','公共部门',[10,11,12]),('u06','成本与竞争',[13,14]),
('u07','市场势力与博弈',[15,16,17]),('u08','劳动与分配',[18,19,20]),('u09','消费者选择',[21]),
('u10','信息与行为',[22])]
metadata = {'version': BRANCH, 'authored_date':'2026-09-05', 'baseline_commit':BASELINE,
 'unit_count':10, 'lessons_per_unit':10, 'lesson_count':100,
 'reference_minutes_per_lesson':12, 'reference_total_minutes':1200,
 'timing_is_estimate_not_mastery_criterion':True,
 'individual_learning_progress_automatically_updated':False,
 'units':[{'id':u,'title':title,'chapters':chapters} for u,title,chapters in unit_specs]}
contents[PREFIX+'course.json'] = json.dumps(metadata, ensure_ascii=False, indent=2)+'\n'

contents[PREFIX+'AUDIT.md'] = '''# gpt6-pro课程重构与验收边界

日期：2026-09-05。基线main提交`2b6ac7218b2e089ed4d302892c49323aae988edb`，工作分支`gpt6-pro`，不自动合并main。

## 原问题

原仓库已有十单元八十小课，主要问题不是缺少标题，而是按分钟片段安排正文、部分内容只给定义和提示、练习解析不够完整、英文术语规范不统一，并且第一章15天、80课与100天路线混杂为默认入口。

例如沉没成本Sunk Cost曾被写作自定SC，而术语规范又要求没有通用缩写时不要自造。根README与20小时入口也未指向同一主线，使学习者难判断下一步。

## 已完成的重构

100个小课均围绕一个问题，包含直觉、中文英文术语、机制、数字例子、练习解析与边界；10个单元各有导航、综合题和费曼分享参考。词表区分标准缩写、数学符号与无通用缩写，明确MR、MB、MC、两种IC和VMPL/MRPL。

不是把80篇机械切为100段。机会成本讲清退款和避免重复计费；供需从表到图到方程；税收联立买卖双方价格；福利双重核对；成本推导MC与ATC；垄断解释旧销量降价；劳动明确公式条件；消费者选择完整展开Slutsky三点；信息区分隐藏类型与隐藏行动。

时间只是首轮预算：100课×约12分钟约为20小时；理解、复习、数学补习、真实项目与公开分享可能额外用时，不以打卡时长判定掌握。

## 版本与历史

默认目录为`docs/course_gpt6_pro/`。根README、START_HERE、ROADMAP和旧80课地图均指向新版；原入口分别归档为`README_legacy_before_gpt6_pro.md`、`START_HERE_legacy_80.md`、`ROADMAP_legacy_100_days.md`和`docs/course_20h/README_legacy_80_lessons.md`。旧课正文和第一章15天资料保留。

原`docs/00_learning_system/`诊断、原始回答、进度与错误记录不重置。文件新增不代表用户已学100课，不自动把旧课号折算成新完成数。

## 验证

运行`python3 scripts/validate_gpt6_pro_course.py`，检查100课与10个导航、编号、解释和解析结构、本地链接与来源锚点、明显占位及分钟切片标题，并回归核对选定算例。

本次实际检查输出见[VALIDATION_REPORT.json](VALIDATION_REPORT.json)。后续分支推送可通过[只读工作流](https://github.com/XiaoJiNu/microeconomicsLearning/actions?query=branch%3Agpt6-pro)再次执行同一检查。

自动验证不证明全部经济学表述没有错误，不测量真实阅读时间，也不代替试学和因果证据。正文长度只作空壳粗检。后续改进应依据具体课号、卡住的术语或推导，以及改变条件后的独立作答，而不是增加页数和打卡要求。
'''

contents['README.md'] = '''# 微观经济学学习：把问题讲清，用证据判断掌握

本分支`gpt6-pro`为2026-09-05重构版。主课程包含**10个单元、100个完整小课**，首轮规划约20小时。课程按概念和问题展开，不按分钟片段切割讲解。

## 唯一默认入口

**[打开新版课程地图](docs/course_gpt6_pro/README.md)**，或直接进入[第一课](docs/course_gpt6_pro/u01/01.md)。已做过诊断者不必重做整套诊断，按原有证据选择下一知识点。

[使用方法](docs/course_gpt6_pro/GUIDE.md) · [中英术语与缩写](docs/course_gpt6_pro/GLOSSARY.md) · [工作簿](docs/course_gpt6_pro/WORKBOOK.md) · [综合考核](docs/course_gpt6_pro/CAPSTONE.md) · [重构说明](docs/course_gpt6_pro/AUDIT.md) · [来源](docs/course_gpt6_pro/SOURCES.md)

## 十个单元

| 单元 | 主题 | 入口 |
|---|---|---|
'''
for u,title,chapters in unit_specs:
    contents['README.md'] += f'| {u.upper()} | {title} | [10个小课]({PREFIX}{u}/README.md) |\n'
contents['README.md'] += '''
原仓库曼昆第8版微观分册第1—22章作为范围框架，OpenStax和CORE用于补充核对。每课有概念、机制、演算例子、短题及解析、适用边界；每单元有综合题和可展开约五分钟的费曼分享参考。

## 时间和术语

单课按约10—15分钟使用颗粒度设计，以12分钟估计100课约1200分钟。数学补习、延迟复习、真实项目和分享可能另需时间，不承诺人人严格20小时掌握。

专业词首次出现给中文、原始英文、通用缩写与解释；没有统一缩写就明确说明，不造简称。边际收入MR、边际收益MB、边际成本MC分开，缩写与数学符号分开。

## 保留历史，不并行执行多套日程

[原诊断与进度](docs/00_learning_system/progress.md)继续保留，不虚构个人完成数。旧入口归档：[原README](README_legacy_before_gpt6_pro.md)、[原80课指南](START_HERE_legacy_80.md)、[原100天路线](ROADMAP_legacy_100_days.md)、[原80课地图](docs/course_20h/README_legacy_80_lessons.md)。旧正文可回看，新版是唯一默认主线。

## 检查

```bash
python3 scripts/validate_gpt6_pro_course.py
```

[实际检查报告](docs/course_gpt6_pro/VALIDATION_REPORT.json)记录本次结构与算例核验；自动测试不等于教学效果证明。更新仅在`gpt6-pro`，不自动合并`main`。
'''
contents['START_HERE_20_HOURS.md'] = '''# 从这里开始：gpt6-pro新版

默认入口：[10单元100小课课程地图](docs/course_gpt6_pro/README.md)。先读[使用方法](docs/course_gpt6_pro/GUIDE.md)，再学[第一课](docs/course_gpt6_pro/u01/01.md)，或按自己的已有证据选择对应缺口。

原诊断和[学习进度](docs/00_learning_system/progress.md)保留，不重做长诊断、不因文件增加自动记为已学。先读完整教学，再独立作答，最后展开解析。专业词正文展开，[词表](docs/course_gpt6_pro/GLOSSARY.md)辅助查阅；[工作簿](docs/course_gpt6_pro/WORKBOOK.md)记录原始答案和纠错。

每课约10—15分钟颗粒度，十单元各十课，首轮预算约20小时，时间不作为掌握标准。每日分享可只讲一个例子，每单元另有五分钟分享参考。原八十课指南保存在[历史文件](START_HERE_legacy_80.md)，不再作为默认日程。
'''
contents['ROADMAP.md'] = '''# 学习路线：概念地图与证据驱动的复习

第一轮使用[新版100课](docs/course_gpt6_pro/README.md)：选择方法→分工供需→弹性政策→福利贸易→公共部门→成本竞争→市场势力博弈→劳动分配→消费者选择→信息行为。

每单元十个独立问题，约两小时首轮预算，不按第几天或分钟片段硬切内容。教材映射和边界见[SCOPE](docs/course_gpt6_pro/SCOPE.md)。完成[综合考核](docs/course_gpt6_pro/CAPSTONE.md)后，按错误做延迟变式和一页应用分析，不把微观基础冒充完整投资或黄金预测训练。

保留[历史进度](docs/00_learning_system/progress.md)，在[工作簿](docs/course_gpt6_pro/WORKBOOK.md)登记实际证据，每次只保留一个下一步。原100天规划保存在[历史路线](ROADMAP_legacy_100_days.md)，原第一章日课和80课也仅作回看，不与新版同时强制执行。
'''
contents['docs/course_20h/README.md'] = '''# 历史80课目录

原八十课正文保留，完整旧地图在[README_legacy_80_lessons.md](README_legacy_80_lessons.md)。

**当前默认学习使用[新版十单元、一百小课](../course_gpt6_pro/README.md)。** 新版按问题和知识依赖重写，补足中英术语、机制、例题、练习解析和分享，不按分钟片段组织正文。

旧版与新版安排冲突时，采用新版使用方法和当前实际学习证据。历史诊断与原始回答不删除、不按文件数量自动折算学习进度。
'''

validator = r'''#!/usr/bin/env python3
"""Validate the new course only; historical material and learner progress are not rewritten."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re
import statistics
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'docs/course_gpt6_pro'


def numeric_checks() -> int:
    checks = []
    def eq(label, actual, expected):
        if not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9):
            raise AssertionError(f'{label}: {actual} != {expected}')
        checks.append(label)
    eq('opportunity/refund', 2500-2000-800, -300)
    eq('comparative opportunity cost A', 3/6, .5)
    eq('comparative opportunity cost B', 2/2, 1)
    eq('base equilibrium price', (100+20)/4, 30)
    eq('base equilibrium quantity', 100-2*30, 40)
    eq('joint shift quantity', 120-2*30, 60)
    eq('cost shock price', (100+40)/4, 35)
    eq('cost shock quantity', 100-2*35, 30)
    eq('midpoint elastic', abs((-20/90)/(2/11)), 11/9)
    eq('unit arc elasticity', abs((-20/90)/(5/22.5)), 1)
    eq('revenue after increase', 12*80, 960)
    eq('contribution after increase', (12-6)*80, 480)
    eq('tax buyer price', 30+10/2, 35)
    eq('tax seller price', 30-10/2, 25)
    eq('tax quantity', 100-2*35, 30)
    eq('tax revenue', 10*30, 300)
    eq('tax CS', .5*(50-35)*30, 225)
    eq('tax PS', .5*(25-10)*30, 225)
    eq('tax DWL', 800-(225+225+300), 50)
    eq('tax 8 DWL', .5*8*8, 32)
    eq('tax 6 quantity', 100-2*33, 34)
    eq('tax 6 revenue', 6*34, 204)
    eq('subsidy quantity', 100-2*25, 50)
    eq('subsidy expenditure', 10*50, 500)
    eq('asymmetric tax share', 6/8, .75)
    eq('free trade CS', .5*(50-20)*60, 900)
    eq('free trade PS', .5*(20-10)*20, 100)
    eq('tariff CS', .5*(50-25)*50, 625)
    eq('tariff PS', .5*(25-10)*30, 225)
    eq('tariff revenue', 5*(50-30), 100)
    eq('tariff DWL', 1000-(625+225+100), 50)
    eq('foreign quota rent domestic welfare', 625+225, 850)
    eq('externality private Q', (100-20)/2, 40)
    eq('externality social Q', (100-20-20)/2, 30)
    eq('positive externality Q', (100+20-20)/2, 50)
    eq('abatement equal allocation', 2*10+2*40, 100)
    eq('abatement cost minimization', 4*10, 40)
    eq('NPV', -100+60/1.1+60/1.1**2, 500/121)
    eq('average tax rate', (10000*.1+10000*.2)/20000, .15)
    tc = lambda q: 100+10*q+q*q
    eq('TC q4', tc(4), 156)
    eq('discrete MC 4 to 5', tc(5)-tc(4), 19)
    eq('continuous MC at 5', 10+2*5, 20)
    eq('ATC minimum value', tc(10)/10, 30)
    eq('competitive profit P40', 40*15-tc(15), 125)
    eq('short run loss P18', 18*4-tc(4), -84)
    eq('short run advantage', -84-(-100), 16)
    eq('short run loss P22', 22*6-tc(6), -64)
    eq('discrete monopoly MR', 11*89-10*90, 79)
    eq('monopoly price', 100-40, 60)
    eq('monopoly profit', 60*40-(100+20*40), 1500)
    eq('monopoly DWL', .5*(80-40)*(60-20), 800)
    eq('Lerner index', (60-20)/60, 2/3)
    eq('alternative monopoly profit', 80*20-(80+40*20), 720)
    eq('repeat-game threshold', (10-8)/(10-4), 1/3)
    eq('VMPL', 20*8, 160)
    eq('MRPL', 15*8, 120)
    eq('monopsony quantity', 40/3, 13.333333333333334)
    eq('monopsony wage', 10+40/3, 70/3)
    eq('Gini population', 1-2*(.5*.25/2+.5*(.25+1)/2), .25)
    eq('EMTR', (100+500)/1000, .6)
    eq('consumer optimum x', 120/(2*10), 6)
    eq('consumer optimum y', 120/(2*20), 3)
    eq('consumer counterexample B', 6*3, 18)
    eq('consumer counterexample C', 10*1, 10)
    eq('Slutsky income', 5*6+20*3, 90)
    eq('Slutsky intermediate x', 90/(2*5), 9)
    eq('Slutsky intermediate y', 90/(2*20), 2.25)
    eq('Slutsky x SE', 9-6, 3)
    eq('Slutsky x IE', 12-9, 3)
    eq('Slutsky intermediate utility', 9*2.25, 20.25)
    eq('intertemporal future C', (100-60)*1.1, 44)
    eq('maintenance high effort', 10+.01*500, 15)
    eq('maintenance low effort', .05*500, 25)
    eq('maintenance deductible effort', 10+.01*100, 11)
    eq('lemons initial expected value', .5*200+.5*100, 150)
    eq('cost shock monopoly profit', 65*35-(100+30*35), 1125)
    return len(checks)


def validate() -> dict:
    expected = {COURSE/f'u{u:02d}'/f'{l:02d}.md' for u in range(1,11) for l in range(1,11)}
    actual = set(COURSE.glob('u[0-9][0-9]/[0-9][0-9].md'))
    if actual != expected:
        raise AssertionError(f'Lesson set mismatch. Missing: {sorted(expected-actual)}; extra: {sorted(actual-expected)}')
    required = ['README.md','GUIDE.md','GLOSSARY.md','WORKBOOK.md','SCOPE.md','SOURCES.md','CAPSTONE.md','AUDIT.md','course.json']
    for name in required:
        if not (COURSE/name).is_file():
            raise AssertionError('Missing required file: '+name)
    metadata = json.loads((COURSE/'course.json').read_text(encoding='utf-8'))
    assert metadata['lesson_count'] == 100
    assert metadata['unit_count'] == 10
    assert metadata['lessons_per_unit'] == 10
    assert metadata['reference_minutes_per_lesson'] * 100 == metadata['reference_total_minutes'] == 1200
    assert sorted(c for unit in metadata['units'] for c in unit['chapters']) == list(range(1,23))
    sizes = []
    for path in sorted(expected):
        text = path.read_text(encoding='utf-8')
        unit = int(path.parent.name[1:]); lesson = int(path.stem)
        if not re.search(r'^#\s+'+f'{unit:02d}\\.{lesson:02d}'+r'\b', text):
            # Use literal prefix to avoid regex differences across Unicode punctuation.
            if not text.startswith(f'# {unit:02d}.{lesson:02d}'):
                raise AssertionError('Lesson title ID mismatch: '+str(path))
        assert len(re.findall(r'^## ', text, flags=re.M)) >= 4, str(path)
        assert '<details>' in text and '</details>' in text and '<summary>' in text, str(path)
        assert f'../SOURCES.md#u{unit:02d}' in text, str(path)
        assert re.search(r'[A-Za-z]{3,}', text), str(path)
        count = len(re.findall(r'[\u4e00-\u9fff]', text))
        if count < 400:
            raise AssertionError(f'Unexpectedly short lesson: {path}: {count} Chinese characters')
        if re.search(r'(?i)\bTODO\b|\bTBD\b|待补充正文|此处占位', text):
            raise AssertionError('Placeholder found: '+str(path))
        if re.search(r'^#+\s*(?:第)?\s*\d+\s*[—–-]\s*\d+\s*分钟', text, re.M):
            raise AssertionError('Minute-sliced section found: '+str(path))
        sizes.append(count)
    for u in range(1,11):
        text = (COURSE/f'u{u:02d}'/'README.md').read_text(encoding='utf-8')
        assert '费曼' in text and '<details>' in text and '综合题' in text
        for l in range(1,11):
            assert f']({l:02d}.md)' in text, (u,l)
    sources = (COURSE/'SOURCES.md').read_text(encoding='utf-8')
    for u in range(1,11):
        assert f'id="u{u:02d}"' in sources
    assert '税率 20。' not in (COURSE/'u05/10.md').read_text(encoding='utf-8')
    assert 'C=(10,1)' in (COURSE/'u09/04.md').read_text(encoding='utf-8')
    checked_links = 0
    markdown = list(COURSE.rglob('*.md')) + [ROOT/p for p in ('README.md','START_HERE_20_HOURS.md','ROADMAP.md','docs/course_20h/README.md')]
    for path in markdown:
        raw = path.read_text(encoding='utf-8')
        raw = re.sub(r'```.*?```', '', raw, flags=re.S)
        for match in re.finditer(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', raw):
            destination = match.group(1).strip()
            if destination.startswith(('https://','http://','mailto:')):
                if re.search(r'\s', destination):
                    raise AssertionError(f'Malformed external URL in {path}: {destination}')
                continue
            target_part, _, fragment = destination.partition('#')
            if not target_part:
                target = path
            elif target_part.startswith('/'):
                target = ROOT / unquote(target_part.lstrip('/'))
            else:
                target = (path.parent/unquote(target_part)).resolve()
            if not target.exists():
                raise AssertionError(f'Broken local link in {path.relative_to(ROOT)}: {destination}')
            if fragment and target.name == 'SOURCES.md':
                target_text = target.read_text(encoding='utf-8')
                assert f'id="{fragment}"' in target_text, (path,destination)
            checked_links += 1
    return {'status':'passed', 'scope':'new course and current entry points; not a proof of all teaching claims',
            'lesson_count':100,'unit_count':10,'local_links_checked':checked_links,
            'numeric_regressions':numeric_checks(),'chinese_characters_in_lessons':sum(sizes),
            'minimum_lesson_chinese_characters':min(sizes),
            'median_lesson_chinese_characters':statistics.median(sizes),
            'maximum_lesson_chinese_characters':max(sizes),
            'estimated_first_pass_minutes':1200,
            'learner_mastery_not_inferred':True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--math-only', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = {'numeric_regressions':numeric_checks(),'status':'passed'} if args.math_only else validate()
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
'''
contents['scripts/validate_gpt6_pro_course.py'] = validator
contents['.github/workflows/validate-gpt6-pro-course.yml'] = '''name: Validate gpt6-pro course
on:
  push:
    branches: [gpt6-pro]
  pull_request:
    paths:
      - 'docs/course_gpt6_pro/**'
      - 'scripts/validate_gpt6_pro_course.py'
      - '.github/workflows/validate-gpt6-pro-course.yml'
      - 'README.md'
      - 'START_HERE_20_HOURS.md'
      - 'ROADMAP.md'
  workflow_dispatch:
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          persist-credentials: false
      - name: Check course, local links, and numerical examples
        run: python3 scripts/validate_gpt6_pro_course.py
'''

baseline_commit = api('git/commits/' + BASELINE)
baseline_tree = api('git/trees/' + baseline_commit['tree']['sha'] + '?recursive=1')
if baseline_tree.get('truncated'):
    raise SystemExit('Baseline tree is truncated.')
baseline_entries = {x['path']: x for x in baseline_tree['tree'] if x['type']=='blob'}
archives = {
 'README_legacy_before_gpt6_pro.md':'README.md',
 'START_HERE_legacy_80.md':'START_HERE_20_HOURS.md',
 'ROADMAP_legacy_100_days.md':'ROADMAP.md',
 'docs/course_20h/README_legacy_80_lessons.md':'docs/course_20h/README.md'}
for archive, original in archives.items():
    if original not in baseline_entries:
        raise SystemExit('Missing original archive source: '+original)

# Local validation uses real new text and the known original path inventory.
# Historical file contents are not claimed to have been revalidated.
with tempfile.TemporaryDirectory(prefix='gpt6-pro-course-') as directory:
    root = Path(directory)
    for path in entries:
        target = root/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch()
    for archive in archives:
        (root/archive).parent.mkdir(parents=True, exist_ok=True)
        (root/archive).touch()
    for path, text in contents.items():
        target = root/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
    report_path = root/PREFIX/'VALIDATION_REPORT.json'
    report_path.write_text('{}\n', encoding='utf-8')
    subprocess.run([sys.executable, str(root/'scripts/validate_gpt6_pro_course.py'), '--report', str(report_path)], check=True)
    report = json.loads(report_path.read_text(encoding='utf-8'))
    report.update({'authored_date':'2026-09-05','authored_tree':AUTHORED_TREE,
                   'baseline_commit':BASELINE, 'branch':BRANCH,
                   'historical_diagnostics_preserved':True,
                   'github_run_id':os.environ.get('GITHUB_RUN_ID')})
    contents[PREFIX+'VALIDATION_REPORT.json'] = json.dumps(report, ensure_ascii=False, indent=2)+'\n'

# Never overwrite unrelated newer work on the branch silently.
if api('git/ref/heads/'+BRANCH)['object']['sha'] != head:
    raise SystemExit('Branch changed during validation; publication aborted without a force push.')
changes = [{'path':p,'mode':'100644','type':'blob','content':text} for p,text in contents.items()
           if p not in entries or p not in course_paths or text != blob_text(entries[p]['sha'])]
for archive, original in archives.items():
    changes.append({'path':archive,'mode':'100644','type':'blob','sha':baseline_entries[original]['sha']})
new_tree = api('git/trees','POST',{'base_tree':AUTHORED_TREE,'tree':changes})['sha']
# Prove historical learning records have identical object IDs in the final tree.
final_tree = api('git/trees/'+new_tree+'?recursive=1')
final_map = {x['path']:x['sha'] for x in final_tree['tree'] if x['type']=='blob'}
for path,item in baseline_entries.items():
    if path.startswith('docs/00_learning_system/') and final_map.get(path) != item['sha']:
        raise SystemExit('Historical learning record would change: '+path)
commit = api('git/commits','POST',{'message':'Rewrite full microeconomics course: 100 concept-led lessons, bilingual terminology, worked answers and validated navigation',
                                 'tree':new_tree,'parents':[head]})
api('git/refs/heads/'+BRANCH,'PATCH',{'sha':commit['sha'],'force':False})
verified = api('git/ref/heads/'+BRANCH)['object']['sha']
if verified != commit['sha']:
    raise SystemExit('Branch verification did not match the published commit.')
print('PUBLISHED_COMMIT='+verified)
print('COURSE=https://github.com/'+REPO+'/tree/'+BRANCH+'/'+PREFIX.rstrip('/'))
print(json.dumps(report,ensure_ascii=False,indent=2))
summary = os.environ.get('GITHUB_STEP_SUMMARY')
if summary:
    Path(summary).write_text('# Course published\n\nCommit: `'+verified+'`\n\n100 lessons, 10 unit guides, bilingual glossary, exercises, Feynman references and capstone. Historical diagnostics unchanged.\n\n```json\n'+json.dumps(report,ensure_ascii=False,indent=2)+'\n```\n', encoding='utf-8')
