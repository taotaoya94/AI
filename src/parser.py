import re
import logging
from typing import Dict, List, Optional
from src.models import Inequality, Example

logger = logging.getLogger(__name__)


class InequalityParser:
    
    INEQUALITY_PATTERNS = {
        'basic': [
            r'对于.*?([a-z](?:\s*[>≥<≤]\s*[a-z])+)',
            r'设.*?则.*?([a-z].*?[>≥<≤].*?[a-z])',
            r'若.*?则.*?([a-z].*?[>≥<≤].*?[a-z])',
        ],
        'fraction': [
            r'\\frac\{[^}]+\}\{[^}]+\}',
            r'\([^)]+\)/\([^)]+\)',
        ],
        'power': [
            r'[a-z]\^[0-9]+',
            r'[a-z]\^\{[^}]+\}',
        ]
    }
    
    def __init__(self):
        pass
    
    def extract_math_expressions(self, text: str) -> List[str]:
        expressions = []
        
        latex_pattern = r'\$\$?(.*?)\$\$?'
        matches = re.findall(latex_pattern, text)
        expressions.extend(matches)
        
        inequality_chars = r'[a-zA-Z0-9\s\+\-\*/\(\)\[\]\{\}]+[≥>≤<≠=]+[a-zA-Z0-9\s\+\-\*/\(\)\[\]\{\}]+'
        matches = re.findall(inequality_chars, text)
        expressions.extend(matches)
        
        return expressions
    
    def identify_proof_sections(self, content: List[str]) -> List[str]:
        proofs = []
        proof_keywords = ['证明', '证法', 'Proof', 'proof', '推导', '证']
        
        for i, para in enumerate(content):
            if any(keyword in para for keyword in proof_keywords):
                proof_text = para
                if i + 1 < len(content):
                    proof_text += '\n' + content[i + 1]
                if len(proof_text) > 30:
                    proofs.append(proof_text)
        
        return proofs[:3]
    
    def identify_examples(self, content: List[str]) -> List[Example]:
        examples = []
        example_keywords = ['例', '例题', 'Example', 'example', '应用']
        
        for i, para in enumerate(content):
            if any(keyword in para[:10] for keyword in example_keywords):
                description = para
                solution = content[i + 1] if i + 1 < len(content) else "详见原文"
                
                if len(description) > 10:
                    examples.append(Example(
                        description=description[:500],
                        solution=solution[:800]
                    ))
        
        return examples[:5]
    
    def parse_crawled_data(self, name: str, crawled_data: List[Dict]) -> Inequality:
        inequality = Inequality(name=name)
        
        all_content = []
        for data in crawled_data:
            if data.get('description'):
                inequality.description = data['description'][:500]
            
            if data.get('content'):
                all_content.extend(data['content'])
        
        math_expressions = []
        for content in all_content:
            expressions = self.extract_math_expressions(content)
            math_expressions.extend(expressions)
        
        if math_expressions:
            inequality.math_form = math_expressions[0][:300]
        
        proofs = self.identify_proof_sections(all_content)
        inequality.proof_methods = proofs
        
        examples = self.identify_examples(all_content)
        inequality.examples = examples
        
        return inequality
    
    def enrich_with_predefined_data(self, inequality: Inequality) -> Inequality:
        predefined_data = self._get_predefined_data()
        
        if inequality.name in predefined_data:
            data = predefined_data[inequality.name]
            
            if not inequality.math_form and data.get('math_form'):
                inequality.math_form = data['math_form']
            
            if not inequality.description and data.get('description'):
                inequality.description = data['description']
            
            if data.get('conditions'):
                inequality.conditions = data['conditions']
            
            if not inequality.proof_methods and data.get('proof_methods'):
                inequality.proof_methods = data['proof_methods']
            
            if not inequality.examples and data.get('examples'):
                inequality.examples = [Example(**ex) for ex in data['examples']]
            
            if data.get('aliases'):
                inequality.aliases = data['aliases']
            
            if data.get('applications'):
                inequality.applications = data['applications']
            
            if data.get('related'):
                inequality.related = data['related']
        
        return inequality
    
    def _get_predefined_data(self) -> Dict:
        return {
            "基本不等式": {
                "math_form": "a² + b² ≥ 2ab 或 (a+b)/2 ≥ √(ab)",
                "description": "基本不等式是数学中最常用的不等式之一，用于比较算术平均数和几何平均数。",
                "conditions": "a, b为非负实数",
                "proof_methods": [
                    "证法1（配方法）：a² + b² - 2ab = (a-b)² ≥ 0，因此 a² + b² ≥ 2ab",
                    "证法2（均值不等式）：对于正数a,b，(a+b)/2 ≥ √(ab)，当且仅当a=b时等号成立"
                ],
                "examples": [
                    {
                        "description": "例1：已知x>0，求x + 1/x的最小值",
                        "solution": "由基本不等式：x + 1/x ≥ 2√(x·1/x) = 2，当x=1时等号成立，因此最小值为2"
                    },
                    {
                        "description": "例2：已知a+b=10，求ab的最大值",
                        "solution": "由基本不等式：(a+b)/2 ≥ √(ab)，即5 ≥ √(ab)，因此ab ≤ 25，当a=b=5时等号成立"
                    },
                    {
                        "description": "例3：证明：对于正数x,y，(x+y)(1/x + 1/y) ≥ 4",
                        "solution": "展开左边：(x+y)(1/x + 1/y) = 1 + y/x + x/y + 1 = 2 + (y/x + x/y) ≥ 2 + 2√((y/x)·(x/y)) = 4"
                    }
                ],
                "aliases": ["均值不等式", "AM-GM不等式"],
                "applications": ["函数最值问题", "不等式证明", "优化问题"],
                "related": ["二元均值不等式", "三元均值不等式"]
            },
            "柯西不等式": {
                "math_form": "(a₁² + a₂² + ... + aₙ²)(b₁² + b₂² + ... + bₙ²) ≥ (a₁b₁ + a₂b₂ + ... + aₙbₙ)²",
                "description": "柯西不等式是数学分析中的重要不等式，在向量空间、概率论等领域有广泛应用。",
                "conditions": "aᵢ, bᵢ为实数，i=1,2,...,n",
                "proof_methods": [
                    "证法1（判别式法）：构造二次函数f(t)=(a₁t+b₁)²+(a₂t+b₂)²+...+(aₙt+bₙ)² ≥ 0，展开后利用判别式Δ≤0即可得证",
                    "证法2（向量法）：利用向量的内积性质|<u,v>| ≤ |u||v|，其中等号成立当且仅当u与v共线",
                    "证法3（数学归纳法）：对n用数学归纳法，n=1时显然成立，假设n=k时成立，证明n=k+1时也成立"
                ],
                "examples": [
                    {
                        "description": "例1：证明：(x² + y²)(1 + 1) ≥ (x + y)²",
                        "solution": "由柯西不等式，令a₁=x, a₂=y, b₁=1, b₂=1，得(x²+y²)(1+1) ≥ (x·1+y·1)² = (x+y)²"
                    },
                    {
                        "description": "例2：已知a+b+c=1，求a²+b²+c²的最小值",
                        "solution": "由柯西不等式：(a²+b²+c²)(1²+1²+1²) ≥ (a·1+b·1+c·1)² = 1，因此a²+b²+c² ≥ 1/3"
                    },
                    {
                        "description": "例3：证明：√(a₁²+a₂²) + √(b₁²+b₂²) ≥ √((a₁+b₁)²+(a₂+b₂)²)",
                        "solution": "平方后利用柯西不等式展开证明，需注意交叉项的处理"
                    }
                ],
                "aliases": ["柯西-施瓦茨不等式", "Cauchy-Schwarz不等式"],
                "applications": ["向量分析", "概率论", "最值问题", "不等式证明"],
                "related": ["赫尔德不等式", "闵可夫斯基不等式"]
            },
            "三角不等式": {
                "math_form": "|a + b| ≤ |a| + |b|",
                "description": "绝对值三角不等式是实数绝对值的基本性质，在分析学中有重要地位。",
                "conditions": "a, b为实数",
                "proof_methods": [
                    "证法1：分四种情况讨论a,b的正负性：①a≥0,b≥0 ②a≥0,b<0 ③a<0,b≥0 ④a<0,b<0",
                    "证法2：利用|x|²=x²，两边平方得|a+b|²=(a+b)²=a²+2ab+b²≤a²+2|a||b|+b²=(|a|+|b|)²"
                ],
                "examples": [
                    {
                        "description": "例1：证明：|a - b| ≥ ||a| - |b||",
                        "solution": "由三角不等式|a|=|(a-b)+b|≤|a-b|+|b|，得|a-b|≥|a|-|b|；同理|a-b|≥|b|-|a|，因此|a-b|≥||a|-|b||"
                    },
                    {
                        "description": "例2：已知|x-1|<1，|y-2|<1，求|x+y-3|的范围",
                        "solution": "|x+y-3|=|(x-1)+(y-2)|≤|x-1|+|y-2|<1+1=2"
                    },
                    {
                        "description": "例3：证明：|a₁+a₂+...+aₙ| ≤ |a₁|+|a₂|+...+|aₙ|",
                        "solution": "对n使用数学归纳法，n=2时即为三角不等式；假设n=k时成立，则n=k+1时由归纳假设可得"
                    }
                ],
                "aliases": ["绝对值不等式", "三角形不等式"],
                "applications": ["极限证明", "距离估计", "不等式放缩"],
                "related": ["基本不等式", "闵可夫斯基不等式"]
            },
            "琴生不等式": {
                "math_form": "f((x₁+x₂+...+xₙ)/n) ≤ (f(x₁)+f(x₂)+...+f(xₙ))/n（凸函数）",
                "description": "琴生不等式描述了凸函数的性质，是均值不等式的推广形式。",
                "conditions": "f为凸函数，xᵢ在定义域内",
                "proof_methods": [
                    "证法1（数学归纳法）：先证n=2的情况，再用归纳法推广到一般情况",
                    "证法2（几何法）：利用凸函数的几何定义，函数图像上任意两点的连线在图像上方",
                    "证法3（权重法）：引入权重pᵢ，证明加权形式的琴生不等式"
                ],
                "examples": [
                    {
                        "description": "例1：利用琴生不等式证明算术-几何平均不等式",
                        "solution": "取f(x)=-ln(x)为凸函数，应用琴生不等式即可得到(x₁+...+xₙ)/n ≥ ⁿ√(x₁...xₙ)"
                    },
                    {
                        "description": "例2：证明：对于正数a,b,c，a²+b²+c² ≥ (a+b+c)²/3",
                        "solution": "取f(x)=x²为凸函数，由琴生不等式得(a²+b²+c²)/3 ≥ ((a+b+c)/3)²"
                    },
                    {
                        "description": "例3：已知a,b,c>0且abc=1，证明：a+b+c ≥ 3",
                        "solution": "对ln(a),ln(b),ln(c)应用琴生不等式，利用凹函数ln(x)的性质"
                    }
                ],
                "aliases": ["Jensen不等式", "詹森不等式"],
                "applications": ["凸优化", "信息论", "概率论"],
                "related": ["均值不等式", "凸函数性质"]
            },
            "伯努利不等式": {
                "math_form": "(1+x)ⁿ ≥ 1+nx",
                "description": "伯努利不等式给出了幂函数的下界估计，在微积分和分析中常用。",
                "conditions": "x>-1, n为正整数或n≥1的实数",
                "proof_methods": [
                    "证法1（数学归纳法）：对n使用数学归纳法，利用(1+x)ⁿ⁺¹=(1+x)ⁿ(1+x)展开证明",
                    "证法2（二项式定理）：展开(1+x)ⁿ=1+nx+...，后面各项非负，因此≥1+nx",
                    "证法3（导数法）：令f(x)=(1+x)ⁿ-1-nx，证明f(x)≥0"
                ],
                "examples": [
                    {
                        "description": "例1：证明：(1.01)¹⁰⁰ > 2",
                        "solution": "由伯努利不等式：(1+0.01)¹⁰⁰ ≥ 1+100×0.01 = 2"
                    },
                    {
                        "description": "例2：证明：对于n≥2，(1+1/n)ⁿ < 3",
                        "solution": "结合伯努利不等式和其他技巧进行估计"
                    },
                    {
                        "description": "例3：利用伯努利不等式估计e的范围",
                        "solution": "考虑e=lim(1+1/n)ⁿ，利用不等式进行上下界估计"
                    }
                ],
                "aliases": ["Bernoulli不等式"],
                "applications": ["极限估计", "级数收敛性", "数值分析"],
                "related": ["二项式定理", "指数不等式"]
            },
            "切比雪夫不等式": {
                "math_form": "(a₁+...+aₙ)(b₁+...+bₙ) ≤ n(a₁b₁+...+aₙbₙ)（同序）",
                "description": "切比雪夫不等式描述了两个同序或反序数列的和与积的关系。",
                "conditions": "a₁≤a₂≤...≤aₙ, b₁≤b₂≤...≤bₙ（同序）或b₁≥b₂≥...≥bₙ（反序）",
                "proof_methods": [
                    "证法1（排序不等式）：利用排序不等式，同序和最大，反序和最小",
                    "证法2（差值法）：考虑Σ(aᵢ-aⱼ)(bᵢ-bⱼ)≥0（同序时）",
                    "证法3（数学归纳法）：对n进行归纳证明"
                ],
                "examples": [
                    {
                        "description": "例1：已知a≤b≤c, x≤y≤z，证明：ax+by+cz ≥ (a+b+c)(x+y+z)/3",
                        "solution": "利用切比雪夫不等式的同序形式，3(ax+by+cz)≥(a+b+c)(x+y+z)"
                    },
                    {
                        "description": "例2：证明：1/2+2/3+3/4+...+n/(n+1) > n/2",
                        "solution": "利用切比雪夫不等式对两个数列进行处理"
                    },
                    {
                        "description": "例3：应用切比雪夫不等式求最值",
                        "solution": "在满足条件的数列中，利用同序或反序的性质求和的最值"
                    }
                ],
                "aliases": ["Chebyshev不等式", "契比雪夫不等式"],
                "applications": ["排序问题", "最值问题", "概率论"],
                "related": ["排序不等式", "均值不等式"]
            },
            "赫尔德不等式": {
                "math_form": "Σ|aᵢbᵢ| ≤ (Σ|aᵢ|ᵖ)^(1/p) · (Σ|bᵢ|ᵍ)^(1/q)，其中1/p+1/q=1",
                "description": "赫尔德不等式是柯西不等式的推广，在泛函分析和积分理论中有重要应用。",
                "conditions": "p,q>1且1/p+1/q=1",
                "proof_methods": [
                    "证法1（杨氏不等式）：利用杨氏不等式ab≤aᵖ/p+bᵍ/q进行证明",
                    "证法2（凸函数）：利用对数函数的凹性和琴生不等式",
                    "证法3（归一化法）：先将数列归一化，再应用杨氏不等式"
                ],
                "examples": [
                    {
                        "description": "例1：验证p=q=2时赫尔德不等式退化为柯西不等式",
                        "solution": "当p=q=2时，1/2+1/2=1，此时赫尔德不等式即为Σ|aᵢbᵢ|≤√(Σaᵢ²)·√(Σbᵢ²)"
                    },
                    {
                        "description": "例2：利用赫尔德不等式估计积分∫|f(x)g(x)|dx",
                        "solution": "应用积分形式的赫尔德不等式：∫|fg|≤(∫|f|ᵖ)^(1/p)(∫|g|ᵍ)^(1/q)"
                    },
                    {
                        "description": "例3：证明Lp空间的有界性",
                        "solution": "利用赫尔德不等式证明Lp空间中的线性泛函是有界的"
                    }
                ],
                "aliases": ["Hölder不等式", "霍尔德不等式"],
                "applications": ["泛函分析", "Lp空间理论", "积分估计"],
                "related": ["柯西不等式", "杨氏不等式", "闵可夫斯基不等式"]
            },
            "闵可夫斯基不等式": {
                "math_form": "(Σ|aᵢ+bᵢ|ᵖ)^(1/p) ≤ (Σ|aᵢ|ᵖ)^(1/p) + (Σ|bᵢ|ᵖ)^(1/p)",
                "description": "闵可夫斯基不等式是三角不等式在Lp空间的推广，证明了Lp范数满足三角不等式。",
                "conditions": "p≥1",
                "proof_methods": [
                    "证法1（赫尔德不等式）：将左边展开后应用赫尔德不等式",
                    "证法2（凸函数）：利用函数xᵖ的凸性",
                    "证法3（归纳法）：对维数n使用数学归纳法"
                ],
                "examples": [
                    {
                        "description": "例1：证明p=2时的闵可夫斯基不等式",
                        "solution": "√(Σ(aᵢ+bᵢ)²) ≤ √(Σaᵢ²) + √(Σbᵢ²)，平方后利用柯西不等式"
                    },
                    {
                        "description": "例2：应用于积分形式",
                        "solution": "(∫|f+g|ᵖ)^(1/p) ≤ (∫|f|ᵖ)^(1/p) + (∫|g|ᵖ)^(1/p)"
                    },
                    {
                        "description": "例3：证明Lp空间是赋范线性空间",
                        "solution": "利用闵可夫斯基不等式验证Lp范数满足三角不等式"
                    }
                ],
                "aliases": ["Minkowski不等式", "明可夫斯基不等式"],
                "applications": ["泛函分析", "Lp空间", "范数理论"],
                "related": ["三角不等式", "赫尔德不等式", "范数不等式"]
            }
        }
