#!/usr/bin/env python3
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

import config
from src.crawler import InequalityCrawler
from src.parser import InequalityParser
from src.database import InequalityDatabase
from src.generator import DocumentGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('inequality_summarizer.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


ENGLISH_NAMES = {
    "柯西不等式": "Cauchy-Schwarz inequality",
    "琴生不等式": "Jensen's inequality",
    "伯努利不等式": "Bernoulli's inequality",
    "赫尔德不等式": "Hölder's inequality",
    "闵可夫斯基不等式": "Minkowski inequality",
    "杨氏不等式": "Young's inequality",
    "切比雪夫不等式": "Chebyshev's inequality",
    "三角不等式": "Triangle inequality",
    "均值不等式": "AM-GM inequality",
    "基本不等式": "Basic inequality",
    "排序不等式": "Rearrangement inequality",
    "幂平均不等式": "Power mean inequality",
    "卡尔森不等式": "Carlson inequality",
    "舒尔不等式": "Schur's inequality",
    "穆尔海德不等式": "Muirhead's inequality",
    "麦克劳林不等式": "Maclaurin's inequality"
}


def crawl_single_inequality(name: str, crawler: InequalityCrawler, parser: InequalityParser) -> tuple:
    try:
        english_name = ENGLISH_NAMES.get(name)
        
        crawled_data = crawler.crawl_inequality(name, english_name)
        
        if crawled_data:
            inequality = parser.parse_crawled_data(name, crawled_data)
            inequality = parser.enrich_with_predefined_data(inequality)
            
            logger.info(f"✓ Successfully processed: {name} (completeness: {inequality.completeness_score():.2%})")
            return (name, inequality, True)
        else:
            inequality = parser.enrich_with_predefined_data(parser.parse_crawled_data(name, []))
            logger.warning(f"⚠ No data crawled for {name}, using predefined data only")
            return (name, inequality, False)
    
    except Exception as e:
        logger.error(f"✗ Error processing {name}: {str(e)}")
        return (name, None, False)


def main():
    logger.info("="*60)
    logger.info("数学不等式自动汇总系统启动")
    logger.info("="*60)
    
    db = InequalityDatabase(config.DATA_FILE)
    crawler = InequalityCrawler(delay=config.CRAWL_DELAY)
    parser = InequalityParser()
    generator = DocumentGenerator(config.TEMPLATES_DIR, config.OUTPUT_DIR)
    
    logger.info(f"目标: 爬取 {len(config.INEQUALITY_NAMES)} 个不等式")
    
    use_multithreading = True
    max_workers = 3
    
    if use_multithreading:
        logger.info(f"使用多线程模式 (workers={max_workers})")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(crawl_single_inequality, name, crawler, parser): name
                for name in config.INEQUALITY_NAMES
            }
            
            completed = 0
            for future in as_completed(futures):
                name, inequality, success = future.result()
                completed += 1
                
                if inequality:
                    db.add_or_update(inequality)
                
                logger.info(f"进度: {completed}/{len(config.INEQUALITY_NAMES)} ({completed/len(config.INEQUALITY_NAMES)*100:.1f}%)")
    else:
        logger.info("使用单线程模式")
        
        for idx, name in enumerate(config.INEQUALITY_NAMES, 1):
            logger.info(f"\n[{idx}/{len(config.INEQUALITY_NAMES)}] 处理: {name}")
            
            name, inequality, success = crawl_single_inequality(name, crawler, parser)
            
            if inequality:
                db.add_or_update(inequality)
    
    db.save()
    
    logger.info("\n" + "="*60)
    logger.info("数据收集完成，开始生成文档...")
    logger.info("="*60)
    
    stats = db.get_statistics()
    logger.info(f"\n数据统计:")
    logger.info(f"  总不等式数: {stats['total']}")
    logger.info(f"  完整不等式数: {stats['complete']}")
    logger.info(f"  包含证法: {stats['with_proofs']}")
    logger.info(f"  包含例题: {stats['with_examples']}")
    logger.info(f"  平均完整度: {stats['avg_completeness']:.2%}")
    
    all_inequalities = db.get_all()
    all_inequalities.sort(key=lambda x: x.completeness_score(), reverse=True)
    
    html_file = generator.generate_html(all_inequalities)
    if html_file:
        logger.info(f"✓ HTML文档已生成: {html_file}")
    
    md_file = generator.generate_markdown(all_inequalities)
    if md_file:
        logger.info(f"✓ Markdown文档已生成: {md_file}")
    
    try:
        pdf_file = generator.generate_pdf(all_inequalities)
        if pdf_file:
            logger.info(f"✓ PDF文档已生成: {pdf_file}")
    except Exception as e:
        logger.warning(f"PDF生成失败 (可选功能): {str(e)}")
    
    logger.info("\n" + "="*60)
    logger.info("✓ 所有任务完成!")
    logger.info("="*60)
    
    logger.info("\n生成的文档:")
    logger.info(f"  - HTML: {config.OUTPUT_DIR}/inequality_summary.html")
    logger.info(f"  - Markdown: {config.OUTPUT_DIR}/inequality_summary.md")
    logger.info(f"  - 数据文件: {config.DATA_FILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n程序异常退出: {str(e)}", exc_info=True)
        sys.exit(1)
