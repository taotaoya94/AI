import json
import os
import logging
from typing import List, Dict, Optional
from src.models import Inequality

logger = logging.getLogger(__name__)


class InequalityDatabase:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.inequalities: Dict[str, Inequality] = {}
        self.load()
    
    def load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        ineq = Inequality.from_dict(item)
                        self.inequalities[ineq.name] = ineq
                logger.info(f"Loaded {len(self.inequalities)} inequalities from database")
            except Exception as e:
                logger.error(f"Error loading database: {str(e)}")
                self.inequalities = {}
        else:
            logger.info("No existing database found, starting fresh")
            self.inequalities = {}
    
    def save(self):
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = [ineq.to_dict() for ineq in self.inequalities.values()]
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(self.inequalities)} inequalities to database")
        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
    
    def add_or_update(self, inequality: Inequality):
        existing = self.inequalities.get(inequality.name)
        
        if existing:
            if not existing.math_form and inequality.math_form:
                existing.math_form = inequality.math_form
            
            if not existing.description and inequality.description:
                existing.description = inequality.description
            
            if not existing.conditions and inequality.conditions:
                existing.conditions = inequality.conditions
            
            if len(inequality.proof_methods) > len(existing.proof_methods):
                existing.proof_methods = inequality.proof_methods
            
            if len(inequality.examples) > len(existing.examples):
                existing.examples = inequality.examples
            
            if inequality.aliases:
                existing.aliases = list(set(existing.aliases + inequality.aliases))
            
            if inequality.applications:
                existing.applications = list(set(existing.applications + inequality.applications))
            
            if inequality.related:
                existing.related = list(set(existing.related + inequality.related))
            
            logger.info(f"Updated inequality: {inequality.name}")
        else:
            self.inequalities[inequality.name] = inequality
            logger.info(f"Added new inequality: {inequality.name}")
    
    def get(self, name: str) -> Optional[Inequality]:
        return self.inequalities.get(name)
    
    def get_all(self) -> List[Inequality]:
        return list(self.inequalities.values())
    
    def get_complete_inequalities(self) -> List[Inequality]:
        return [ineq for ineq in self.inequalities.values() if ineq.is_complete()]
    
    def get_statistics(self) -> Dict:
        total = len(self.inequalities)
        complete = len(self.get_complete_inequalities())
        
        with_proofs = sum(1 for ineq in self.inequalities.values() if ineq.proof_methods)
        with_examples = sum(1 for ineq in self.inequalities.values() if ineq.examples)
        
        avg_completeness = sum(ineq.completeness_score() for ineq in self.inequalities.values()) / total if total > 0 else 0
        
        return {
            'total': total,
            'complete': complete,
            'with_proofs': with_proofs,
            'with_examples': with_examples,
            'avg_completeness': avg_completeness
        }
