#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.models import Inequality, Example
from src.parser import InequalityParser
from src.database import InequalityDatabase
from src.generator import DocumentGenerator


def test_models():
    print("Testing models...")
    
    example = Example(
        description="测试例题",
        solution="测试解答"
    )
    
    ineq = Inequality(
        name="测试不等式",
        aliases=["别名1"],
        math_form="a + b >= 2*sqrt(ab)",
        conditions="a, b > 0",
        proof_methods=["证法1"],
        examples=[example],
        applications=["应用1"]
    )
    
    assert ineq.name == "测试不等式"
    assert len(ineq.examples) == 1
    assert ineq.completeness_score() > 0.5
    
    ineq_dict = ineq.to_dict()
    ineq2 = Inequality.from_dict(ineq_dict)
    assert ineq2.name == ineq.name
    
    print("✓ Models test passed")


def test_parser():
    print("Testing parser...")
    
    parser = InequalityParser()
    
    text = "对于 a > 0, b > 0, 有 a + b >= 2*sqrt(ab)"
    expressions = parser.extract_math_expressions(text)
    
    predefined = parser._get_predefined_data()
    assert len(predefined) > 0
    assert "基本不等式" in predefined
    
    ineq = Inequality(name="基本不等式")
    enriched = parser.enrich_with_predefined_data(ineq)
    assert enriched.math_form != ""
    assert len(enriched.proof_methods) > 0
    
    print("✓ Parser test passed")


def test_database():
    print("Testing database...")
    
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file.close()
    
    try:
        db = InequalityDatabase(temp_file.name)
        
        ineq = Inequality(
            name="测试不等式",
            math_form="a + b > 0"
        )
        
        db.add_or_update(ineq)
        assert len(db.get_all()) == 1
        
        retrieved = db.get("测试不等式")
        assert retrieved is not None
        assert retrieved.name == "测试不等式"
        
        stats = db.get_statistics()
        assert stats['total'] == 1
        
        db.save()
        
        db2 = InequalityDatabase(temp_file.name)
        assert len(db2.get_all()) == 1
        
        print("✓ Database test passed")
    finally:
        os.unlink(temp_file.name)


def test_generator():
    print("Testing generator...")
    
    import tempfile
    temp_dir = tempfile.mkdtemp()
    templates_dir = 'templates'
    
    try:
        gen = DocumentGenerator(templates_dir, temp_dir)
        
        ineq = Inequality(
            name="测试不等式",
            math_form="a + b >= c",
            description="这是一个测试",
            proof_methods=["证法1"],
            examples=[Example("例题", "解答")]
        )
        
        inequalities = [ineq]
        
        categorized = gen._categorize_inequalities(inequalities)
        assert len(categorized) > 0
        
        print("✓ Generator test passed")
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    print("="*60)
    print("Running basic tests...")
    print("="*60)
    
    try:
        test_models()
        test_parser()
        test_database()
        test_generator()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
