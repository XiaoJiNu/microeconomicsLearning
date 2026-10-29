# Spine · 经济学十大原理

BookEngine 的章节骨架。每一行是一页活书，不是进度清单。字段与 DeepTutor 的章节规格对齐：`title`、`learning_objectives`、`content_type`、`summary`、`prerequisites`。

`content_type` 只用 `theory`、`concept`、`practice`、`history`。本骨架没有单独的 history 页；亚当·斯密与看不见的手写在理论页里。

## 章节树

| id | title | content_type | prerequisites | page |
|---|---|---|---|---|
| ch01-p01 | 人们面临权衡 | concept | — | [pages/01_tradeoff.md](pages/01_tradeoff.md) |
| ch01-p02 | 成本是为了得到它所放弃的东西 | concept | ch01-p01 | [pages/02_opportunity_cost.md](pages/02_opportunity_cost.md) |
| ch01-p03 | 理性人考虑边际量 | concept | ch01-p02 | [pages/03_margin.md](pages/03_margin.md) |
| ch01-p04 | 人们对激励做出反应 | concept | ch01-p03 | [pages/04_incentives.md](pages/04_incentives.md) |
| ch01-p05 | 贸易可以使每个人状况更好 | concept | ch01-p02 | [pages/05_trade.md](pages/05_trade.md) |
| ch01-p06 | 市场通常靠价格来组织 | theory | ch01-p04, ch01-p05 | [pages/06_markets.md](pages/06_markets.md) |
| ch01-p07 | 政府有时可以改善结果 | concept | ch01-p06 | [pages/07_government.md](pages/07_government.md) |
| ch01-p08 | 整体经济的三条边界 | concept | ch01-p01, ch01-p07 | [pages/08_economy_boundary.md](pages/08_economy_boundary.md) |
| ch01-p09 | 把情景交给十条 | practice | ch01-p08 | [pages/09_scenes.md](pages/09_scenes.md) |

## JSON

```json
[
  {
    "id": "ch01-p01",
    "title": "人们面临权衡",
    "content_type": "concept",
    "summary": "稀缺使选择变成权衡。用时间、收入、冰淇淋与披萨、枪炮与黄油、环境与收入、效率与平等，把少掉的那一边写出来，先不选边。",
    "learning_objectives": [
      "点出不够用的资源，并写出多得到的一边与少掉的一边",
      "把枪炮与黄油、环境与收入、效率与平等分成不同的对子",
      "停在看清让步，不在本页宣布哪一边该赢"
    ],
    "prerequisites": [],
    "page": "pages/01_tradeoff.md"
  },
  {
    "id": "ch01-p02",
    "title": "成本是为了得到它所放弃的东西",
    "content_type": "concept",
    "summary": "用上大学把成本分成显成本、隐成本和两边都要付的部分。机会成本只记下一最好的替代。",
    "learning_objectives": [
      "列出上大学的显成本、常常最大的隐成本，以及食宿里该剔除的部分",
      "说明机会成本只记最佳替代",
      "在最佳替代不是工作时，把工资换成那一件事的价值"
    ],
    "prerequisites": ["ch01-p01"],
    "page": "pages/02_opportunity_cost.md"
  },
  {
    "id": "ch01-p03",
    "title": "理性人考虑边际量",
    "content_type": "concept",
    "summary": "决定常常是再多一单位。用空位机票分开平均、边际和沉没；用水与钻石说明价格跟着再多一单位的好处走。",
    "learning_objectives": [
      "把全有或全无和再多一单位分开",
      "用 300 美元、花生饮料、500 美元和 10 万美元判断下一张票",
      "解释水便宜、钻石贵跟着哪一个量"
    ],
    "prerequisites": ["ch01-p02"],
    "page": "pages/03_margin.md"
  },
  {
    "id": "ch01-p04",
    "title": "人们对激励做出反应",
    "content_type": "concept",
    "summary": "价格和规则改写代价或好处，行为就改。苹果、汽油税、安全带用来看见点名的一侧和没被加价的一侧。",
    "learning_objectives": [
      "用苹果说明价格怎样同时推动买方和卖方",
      "列出汽油税之后课本里出现的那些去向",
      "把安全带拆成两列，并说得出佩尔兹曼记下的方向"
    ],
    "prerequisites": ["ch01-p03"],
    "page": "pages/04_incentives.md"
  },
  {
    "id": "ch01-p05",
    "title": "贸易可以使每个人状况更好",
    "content_type": "concept",
    "summary": "交换不是零和。家庭不必样样自做；种粮的与养牛的专做再交换，可以好于各自单干。互利不保证平分。",
    "learning_objectives": [
      "说明一方多得并不必然使另一方少得",
      "用种粮与养牛说清比较对象是各自单干",
      "记住更适合看放弃的比例，本页不算数值"
    ],
    "prerequisites": ["ch01-p02"],
    "page": "pages/05_trade.md"
  },
  {
    "id": "ch01-p06",
    "title": "市场通常靠价格来组织",
    "content_type": "theory",
    "summary": "没有总调度时，价格同时带着社会价值和生产成本。冰淇淋涨价让买方少买、店家多做。价格若不许动，这只手就难起作用。",
    "learning_objectives": [
      "说出市场经济把哪些决定交给企业和家庭",
      "用冰淇淋价格说明看不见的手靠什么协调",
      "指出税收和房租管制挡住的是价格调整"
    ],
    "prerequisites": ["ch01-p04", "ch01-p05"],
    "page": "pages/06_markets.md"
  },
  {
    "id": "ch01-p07",
    "title": "政府有时可以改善结果",
    "content_type": "concept",
    "summary": "产权是前提。政府动手有效率与平等两条线。效率这边认外部性、市场势力，信息不完全只认名。再分配不在这几扇门里。",
    "learning_objectives": [
      "用农民、餐馆、影视说明产权",
      "给污染、一口井、旧车各贴对名字",
      "把再分配放在失灵的门外，并记住政策不自动变好"
    ],
    "prerequisites": ["ch01-p06"],
    "page": "pages/07_government.md"
  },
  {
    "id": "ch01-p08",
    "title": "整体经济的三条边界",
    "content_type": "concept",
    "summary": "生活水平跟着生产率，大幅持续的通胀几乎都来自货币过多，短期里通胀与失业常被推向相反方向。本页不建模型。",
    "learning_objectives": [
      "用一小时的产出说出生活水平差别的落点",
      "把个别物品涨价和物价总体上升分开",
      "说出短期权衡的方向，并拒绝在本页画曲线或写公式"
    ],
    "prerequisites": ["ch01-p01", "ch01-p07"],
    "page": "pages/08_economy_boundary.md"
  },
  {
    "id": "ch01-p09",
    "title": "把情景交给十条",
    "content_type": "practice",
    "summary": "用学生的一小时、空位机票、种粮养牛和三扇门，练习把情景交到对应的原理上。边界三条只许贴标签。",
    "learning_objectives": [
      "在一个情景里连续使用权衡、机会成本、边际和激励",
      "把贸易、价格和政府的门从个人决策里分出来",
      "遇到生产率、货币和短期失业时停在边界句"
    ],
    "prerequisites": ["ch01-p08"],
    "page": "pages/09_scenes.md"
  }
]
```

读序就是表的顺序。掌握路径另有硬门槛，见 [MASTERY_PATH.md](../../MASTERY_PATH.md)。
