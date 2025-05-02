import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from core.processor import ScoutReportProcessor, TranslationManager

def generate_scout_report_html(player_id, language='pt', output_dir=None):
    """
    Gera um relatório HTML de scout para um jogador específico.
    
    Args:
        player_id: ID do jogador
        language: Código do idioma (pt, en, bg, es)
        output_dir: Diretório de saída para o arquivo HTML
        
    Returns:
        Caminho para o arquivo HTML gerado
    """
    # Verifica se o idioma é suportado
    if language not in TranslationManager.SUPPORTED_LANGUAGES:
        language = 'pt'  # Idioma padrão
    
    # Inicializa o processador de dados
    processor = ScoutReportProcessor(language)
    
    try:
        # Obtém os dados do jogador
        from services.data_service import find_player_by_id
        player_data = find_player_by_id(player_id)
        if not player_data:
            raise ValueError(f"Jogador com ID {player_id} não encontrado.")
        
        # Obtém dados históricos do Transfermarkt
        from core.transfermarkt import get_player_data
        historical_data = get_player_data(player_data.get('name', ''))
        
        # Realiza análise técnica
        from core.data_analysis import complete_data_analysis
        technical_analysis = complete_data_analysis(player_id=player_id, language=language)
        
        # Processa os dados para o template
        template_data = processor.process_player_data(
            player_id, player_data, historical_data, technical_analysis
        )
        with open('template.json', 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=4)
            
        # Configura o ambiente Jinja2
        template_dir = os.path.dirname(os.path.abspath(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('scout_report_template_updated.html')
        
        # Adicionar função format_metric_name ao contexto do template
        def format_metric_name(metric_name):
            """
            Formata o nome de uma métrica para exibição no relatório.
            
            Args:
                metric_name: Nome da métrica em camelCase ou snake_case
                
            Returns:
                Nome formatado para exibição
            """
            import re
            formatted = re.sub(r'([a-z])([A-Z])', r'\1 \2', metric_name)
            formatted = formatted.replace('_', ' ')
            return ' '.join(word.capitalize() for word in formatted.split())

        # Adicionar a função ao dicionário de dados do template
        template_data['format_metric_name'] = format_metric_name
        
        # Renderiza o template
        html_content = template.render(**template_data)
        
        # Define o diretório de saída
        if not output_dir:
            output_dir = os.getcwd()
        
        # Cria o diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Gera um nome de arquivo baseado no ID do jogador e data
        player_name = player_data.get('name', '').replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scout_report_{player_name}_{player_id}_{language}_{timestamp}.html"
        output_path = os.path.join(output_dir, filename)
        
        # Salva o arquivo HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Relatório HTML gerado com sucesso: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Erro ao gerar relatório HTML: {str(e)}")
        raise
def generate_scout_report_pdf(player_id, language='pt', output_dir=None):
    """
    Gera um relatório PDF de scout para um jogador específico.
    
    Args:
        player_id: ID do jogador
        language: Código do idioma (pt, en, bg, es)
        output_dir: Diretório de saída para o arquivo PDF
        
    Returns:
        Caminho para o arquivo PDF gerado
    """
    try:
        # Primeiro gera o HTML
        html_path = generate_scout_report_html(player_id, language, output_dir)
        
        # Define o caminho de saída para o PDF
        pdf_path = html_path.replace('.html', '.pdf')
        
        # Tenta usar weasyprint para converter HTML para PDF
        try:
            from weasyprint import HTML
            HTML(html_path).write_pdf(pdf_path)
            print(f"Relatório PDF gerado com sucesso usando WeasyPrint: {pdf_path}")
        except ImportError:
            # Alternativa: usar wkhtmltopdf via subprocess
            import subprocess
            try:
                subprocess.run(['wkhtmltopdf', '--enable-javascript', '--javascript-delay', '1000', 
                               '--no-stop-slow-scripts', html_path, pdf_path], check=True)
                print(f"Relatório PDF gerado com sucesso usando wkhtmltopdf: {pdf_path}")
            except (subprocess.SubprocessError, FileNotFoundError):
                # Se ambos falharem, retorna apenas o caminho HTML
                print("Aviso: Não foi possível gerar PDF. Bibliotecas necessárias não estão instaladas.")
                return html_path
        
        return pdf_path
    
    except Exception as e:
        print(f"Erro ao gerar relatório PDF: {str(e)}")
        raise

def main():
    """Função principal para execução via linha de comando."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerador de Relatórios de Scout')
    parser.add_argument('player_id', help='ID do jogador')
    parser.add_argument('--language', '-l', choices=TranslationManager.SUPPORTED_LANGUAGES, 
                        default='pt', help='Idioma do relatório (padrão: pt)')
    parser.add_argument('--format', '-f', choices=['html', 'pdf'], 
                        default='html', help='Formato de saída (padrão: html)')
    parser.add_argument('--output-dir', '-o', help='Diretório de saída')
    
    args = parser.parse_args()
    
    try:
        if args.format.lower() == 'pdf':
            output_path = generate_scout_report_pdf(args.player_id, args.language, args.output_dir)
        else:
            output_path = generate_scout_report_html(args.player_id, args.language, args.output_dir)
        
        print(f"Relatório gerado com sucesso: {output_path}")
    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
