# 📐 36种常见数学不等式总结

**共收录 {{ total_count }} 个不等式 | 生成时间: {{ generation_date }}**

---

## 📑 目录

{% for category_name, items in categorized.items() %}
### {{ category_name }} ({{ items|length }})
{% for ineq in items %}
- [{{ ineq.name }}](#{{ ineq.name|replace(' ', '-') }})
{% endfor %}

{% endfor %}

---

{% for category_name, items in categorized.items() %}
## {{ category_name }}

{% for ineq in items %}
### {{ ineq.name }}

{% if ineq.aliases %}
**别名:** {{ ineq.aliases|join(', ') }}
{% endif %}

{% if ineq.description %}
{{ ineq.description }}
{% endif %}

{% if ineq.math_form %}
#### 📝 数学形式

```
{{ ineq.math_form }}
```
{% endif %}

{% if ineq.conditions %}
#### ⚙️ 应用条件

{{ ineq.conditions }}
{% endif %}

{% if ineq.proof_methods %}
#### 🔍 证明方法

{% for proof in ineq.proof_methods %}
**证法 {{ loop.index }}:**

{{ proof }}

{% endfor %}
{% endif %}

{% if ineq.examples %}
#### 💡 典型例题

{% for example in ineq.examples %}
**例 {{ loop.index }}:** {{ example.description }}

**解答:** {{ example.solution }}

{% endfor %}
{% endif %}

{% if ineq.applications or ineq.related %}
#### 🏷️ 标签

{% if ineq.applications %}
**应用场景:** {{ ineq.applications|join(', ') }}
{% endif %}

{% if ineq.related %}
**相关不等式:** {{ ineq.related|join(', ') }}
{% endif %}
{% endif %}

**完整度:** {{ "%.0f"|format(ineq.completeness_score() * 100) }}%

---

{% endfor %}
{% endfor %}

---

*本文档由不等式自动汇总系统生成 | © 2024*
