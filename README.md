# 微观经济学学习：把问题讲清，用证据判断掌握

本分支`gpt6-pro`为2026-09-05重构版。主课程包含**10个单元、100个完整小课**，首轮规划约20小时。课程按概念和问题展开，不按分钟片段切割讲解。

## 唯一默认入口

**[打开新版课程地图](docs/course_gpt6_pro/README.md)**，或直接进入[第一课](docs/course_gpt6_pro/u01/01.md)。已做过诊断者不必重做整套诊断，按原有证据选择下一知识点。

[使用方法](docs/course_gpt6_pro/GUIDE.md) · [中英术语与缩写](docs/course_gpt6_pro/GLOSSARY.md) · [工作簿](docs/course_gpt6_pro/WORKBOOK.md) · [综合考核](docs/course_gpt6_pro/CAPSTONE.md) · [重构说明](docs/course_gpt6_pro/AUDIT.md) · [来源](docs/course_gpt6_pro/SOURCES.md)

## 十个单元

| 单元 | 主题 | 入口 |
|---|---|---|
| U01 | 经济学思维 | [10个小课](docs/course_gpt6_pro/u01/README.md) |
| U02 | 分工与供需 | [10个小课](docs/course_gpt6_pro/u02/README.md) |
| U03 | 弹性与政策 | [10个小课](docs/course_gpt6_pro/u03/README.md) |
| U04 | 福利与贸易 | [10个小课](docs/course_gpt6_pro/u04/README.md) |
| U05 | 公共部门 | [10个小课](docs/course_gpt6_pro/u05/README.md) |
| U06 | 成本与竞争 | [10个小课](docs/course_gpt6_pro/u06/README.md) |
| U07 | 市场势力与博弈 | [10个小课](docs/course_gpt6_pro/u07/README.md) |
| U08 | 劳动与分配 | [10个小课](docs/course_gpt6_pro/u08/README.md) |
| U09 | 消费者选择 | [10个小课](docs/course_gpt6_pro/u09/README.md) |
| U10 | 信息与行为 | [10个小课](docs/course_gpt6_pro/u10/README.md) |

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
