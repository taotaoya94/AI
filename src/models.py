from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class Example:
    description: str
    solution: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Inequality:
    name: str
    aliases: List[str] = field(default_factory=list)
    math_form: str = ""
    conditions: str = ""
    proof_methods: List[str] = field(default_factory=list)
    examples: List[Example] = field(default_factory=list)
    related: List[str] = field(default_factory=list)
    applications: List[str] = field(default_factory=list)
    description: str = ""
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['examples'] = [ex.to_dict() if isinstance(ex, Example) else ex for ex in self.examples]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Inequality':
        examples = []
        for ex in data.get('examples', []):
            if isinstance(ex, dict):
                examples.append(Example(**ex))
            else:
                examples.append(ex)
        
        return cls(
            name=data.get('name', ''),
            aliases=data.get('aliases', []),
            math_form=data.get('math_form', ''),
            conditions=data.get('conditions', ''),
            proof_methods=data.get('proof_methods', []),
            examples=examples,
            related=data.get('related', []),
            applications=data.get('applications', []),
            description=data.get('description', '')
        )
    
    def is_complete(self) -> bool:
        return (
            bool(self.name) and
            bool(self.math_form) and
            len(self.proof_methods) >= 1 and
            len(self.examples) >= 1
        )
    
    def completeness_score(self) -> float:
        score = 0.0
        if self.name:
            score += 0.1
        if self.math_form:
            score += 0.2
        if self.description:
            score += 0.1
        if self.conditions:
            score += 0.1
        score += min(len(self.proof_methods) * 0.15, 0.3)
        score += min(len(self.examples) * 0.1, 0.2)
        return min(score, 1.0)
