#!/usr/bin/env python3
import logging
import sys

import config
from src.parser import InequalityParser
from src.database import InequalityDatabase
from src.generator import DocumentGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    logger.info("="*60)
    logger.info("快速演示：使用预定义数据生成文档")
    logger.info("="*60)
    
    db = InequalityDatabase(config.DATA_FILE)
    parser = InequalityParser()
    
    predefined_names = [
        "基本不等式",
        "柯西不等式",
        "三角不等式",
        "琴生不等式",
        "伯努利不等式",
        "切比雪夫不等式",
        "赫尔德不等式",
        "闵可夫斯基不等式"
    ]
    
    logger.info(f"使用 {len(predefined_names)} 个预定义不等式生成示例文档")
    
    for name in predefined_names:
        from src.models import Inequality
        ineq = Inequality(name=name)
        ineq = parser.enrich_with_predefined_data(ineq)
        db.add_or_update(ineq)
        logger.info(f"✓ 添加: {name} (完整度: {ineq.completeness_score():.2%})")
    
    db.save()
    
    logger.info("\n生成文档...")
    
    generator = DocumentGenerator(config.TEMPLATES_DIR, config.OUTPUT_DIR)
    
    all_inequalities = db.get_all()
    all_inequalities.sort(key=lambda x: x.completeness_score(), reverse=True)
    
    html_file = generator.generate_html(all_inequalities)
    if html_file:
        logger.info(f"✓ HTML文档: {html_file}")
    
    md_file = generator.generate_markdown(all_inequalities)
    if md_file:
        logger.info(f"✓ Markdown文档: {md_file}")
    
    stats = db.get_statistics()
    logger.info(f"\n数据统计:")
    logger.info(f"  总不等式数: {stats['total']}")
    logger.info(f"  完整不等式数: {stats['complete']}")
    logger.info(f"  平均完整度: {stats['avg_completeness']:.2%}")
    
    logger.info("\n" + "="*60)
    logger.info("✓ 演示完成!")
    logger.info("="*60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"错误: {str(e)}", exc_info=True)
        sys.exit(1)
