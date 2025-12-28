import os
import logging
from typing import List
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from src.models import Inequality

logger = logging.getLogger(__name__)


class DocumentGenerator:
    def __init__(self, templates_dir: str, output_dir: str):
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_html(self, inequalities: List[Inequality], filename: str = 'inequality_summary.html'):
        try:
            template = self.env.get_template('summary_template.html')
            
            categorized = self._categorize_inequalities(inequalities)
            
            html_content = template.render(
                inequalities=inequalities,
                categorized=categorized,
                total_count=len(inequalities),
                generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated HTML document: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating HTML: {str(e)}")
            return None
    
    def generate_markdown(self, inequalities: List[Inequality], filename: str = 'inequality_summary.md'):
        try:
            template = self.env.get_template('summary_template.md')
            
            categorized = self._categorize_inequalities(inequalities)
            
            md_content = template.render(
                inequalities=inequalities,
                categorized=categorized,
                total_count=len(inequalities),
                generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            logger.info(f"Generated Markdown document: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating Markdown: {str(e)}")
            return None
    
    def _categorize_inequalities(self, inequalities: List[Inequality]) -> dict:
        categories = {
            '基本均值不等式': [],
            '经典不等式': [],
            '函数不等式': [],
            '高级不等式': [],
            '其他不等式': []
        }
        
        basic_keywords = ['基本', '均值', '二元', '三元', 'n元', '糖水']
        classic_keywords = ['柯西', '琴生', '伯努利', '切比雪夫', '三角']
        function_keywords = ['指数', '对数', '三角函数']
        advanced_keywords = ['赫尔德', '闵可夫斯基', '舒尔', '穆尔海德', '排序', 
                            '卡尔森', '杨氏', '幂平均', '权方', 'Aczel']
        
        for ineq in inequalities:
            name = ineq.name
            
            if any(kw in name for kw in basic_keywords):
                categories['基本均值不等式'].append(ineq)
            elif any(kw in name for kw in classic_keywords):
                categories['经典不等式'].append(ineq)
            elif any(kw in name for kw in function_keywords):
                categories['函数不等式'].append(ineq)
            elif any(kw in name for kw in advanced_keywords):
                categories['高级不等式'].append(ineq)
            else:
                categories['其他不等式'].append(ineq)
        
        return {k: v for k, v in categories.items() if v}
    
    def generate_pdf(self, inequalities: List[Inequality], filename: str = 'inequality_summary.pdf'):
        try:
            from weasyprint import HTML
            
            html_file = self.generate_html(inequalities, 'temp_for_pdf.html')
            if not html_file:
                return None
            
            output_path = os.path.join(self.output_dir, filename)
            HTML(html_file).write_pdf(output_path)
            
            os.remove(html_file)
            
            logger.info(f"Generated PDF document: {output_path}")
            return output_path
        except ImportError:
            logger.warning("weasyprint not installed, skipping PDF generation")
            return None
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return None
