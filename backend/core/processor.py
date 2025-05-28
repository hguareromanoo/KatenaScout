"""
Processador e integrador de dados para relatórios de scout de futebol.
Este módulo prepara os dados para inicialização em templates Jinja2 com gráficos interativos.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import uuid
# import base64 # Not used directly here
# from io import BytesIO # Not used directly here
# import numpy as np # Not used directly here
# from pydantic import BaseModel # Not used directly here
from sqlalchemy.orm import Session

# Importações dos módulos existentes
from core.transfermarkt import PlayerData, PlayerVisualizationModule # PlayerVisualizationModule might need review if it uses player data directly
from core.data_analysis import complete_data_analysis # This now needs db
from core.generate_report import ScoutingReportAI # This now needs db for its methods
from services.data_service import find_player_by_id as find_player_by_id_service
from services.data_service import find_club_by_id as find_club_by_id_service
from services.data_service import DB_TO_GRANULAR_FALLBACK_MAP
from backend.database import get_db # For the global generate_scout_report function


class TranslationManager:
    """Gerenciador de traduções para suporte a múltiplos idiomas."""
    
    SUPPORTED_LANGUAGES = ['pt', 'en', 'bg', 'es']
    TRANSLATIONS = {
        'position_group':{'pt': 'Grupo de Posição', 'en': 'Position Group', 'bg': 'Група Позиции', 'es': 'Grupo de Posición'},
        'report_title': {'pt': 'Relatório Avançado de Scouting','en': 'Advanced Scouting Report','bg': 'Разширен Скаутски Доклад','es': 'Informe Avanzado de Scouting'},
        'attacking': {'pt': 'Ataque','en': 'Attacking','bg': 'Атака','es': 'Ataque'},
        'passing': {'pt': 'Passe','en': 'Passing','bg': 'Подаване','es': 'Pase'},
        'defensive': {'pt': 'Defesa','en': 'Defensive','bg': 'Защита','es': 'Defensa'},
        'possession': {'pt': 'Posse de bola','en': 'Possession','bg': 'Притежание','es': 'Posesión'},
        'physical': {'pt': 'Físico','en': 'Physical','bg': 'Физическо','es': 'Físico'},
        'goalkeeping': {'pt': 'Goleiro','en': 'Goalkeeping','bg': 'Вратарски умения','es': 'Portero'},
        'positioning': {'pt': 'Posicionamento','en': 'Positioning','bg': 'Позициониране','es': 'Posicionamiento'},
        'goalkeeper': {'pt': 'Goleiro','en': 'Goalkeeper','bg': 'Вратар','es': 'Portero'},
        'center_backs': {'pt': 'Zagueiros','en': 'Center Backs','bg': 'Централни защитници','es': 'Defensas centrales'},
        'full_backs': {'pt': 'Laterais','en': 'Full Backs','bg': 'Странични защитници','es': 'Laterales'},
        'midfielders': {'pt': 'Meio-campistas','en': 'Midfielders','bg': 'Полузащитници','es': 'Centrocampistas'},
        'wingers': {'pt': 'Pontas','en': 'Wingers','bg': 'Крила','es': 'Extremos'},
        'center_forwards': {'pt': 'Centroavantes','en': 'Center Forwards','bg': 'Централни нападатели','es': 'Delanteros centros'},
        'outfield': {'pt': 'Jogador de linha','en': 'Outfield Player','bg': 'Полеви играч','es': 'Jugador de campo'},
        'percentiles_by_category': {'pt': 'Percentis por Categoria','en': 'Percentiles by Category','bg': 'Проценти по Категории','es': 'Percentiles por Categoría'},
        'original_percentiles': {'pt': 'Percentis Originais','en': 'Original Percentiles','bg': 'Оригинални Проценти','es': 'Percentiles Originales'},
        'player_info': {'pt': 'Informações do Jogador','en': 'Player Information','bg': 'Информация за Играча','es': 'Información del Jugador'},
        'executive_summary': {'pt': 'Resumo Executivo','en': 'Executive Summary','bg': 'Резюме','es': 'Resumen Ejecutivo'},
        'comparative_analysis': {'pt': 'Análise Comparativa','en': 'Comparative Analysis','bg': 'Сравнителен Анализ','es': 'Análisis Comparativo'},
        'tactical_analysis': {'pt': 'Análise Tática','en': 'Tactical Analysis','bg': 'Тактически Анализ','es': 'Análisis Táctico'},
        'swot_analysis': {'pt': 'Análise SWOT','en': 'SWOT Analysis','bg': 'SWOT Анализ','es': 'Análisis DAFO'},
        'injury_history': {'pt': 'Histórico de Lesões','en': 'Injury History','bg': 'История на Контузиите','es': 'Historial de Lesiones'},
        'market_value': {'pt': 'Valor de Mercado','en': 'Market Value','bg': 'Пазарна Стойност','es': 'Valor de Mercado'},
        'recruitment_recommendation': {'pt': 'Recomendação de Recrutamento','en': 'Recruitment Recommendation','bg': 'Препоръка за Набиране','es': 'Recomendación de Fichaje'},
        'historical_analysis': {'pt': 'Análise Histórica','en': 'Historical Analysis','bg': 'Исторически Анализ','es': 'Análisis Histórico'},
        'transfers': {'pt': 'Transferências','en': 'Transfers','bg': 'Трансфери','es': 'Transferencias'},
        'tactical_roles':{'pt': 'Perfis Táticos','en': 'Tactical Roles','bg': 'Тактически Роли','es': 'Roles Tácticos'},
        'tactical_styles' : {'pt': 'Estilos Táticos','en': 'Tactical Styles','bg': 'Тактически Стилове','es': 'Estilos Tácticos'},
        'tactical_role_tooltip': {'pt': 'Perfis táticos de maior compatibilidade com o jogador','en': 'Tactical profiles most compatible with the player','bg': 'Тактически профили, които са най-съвместими с играча','es': 'Perfiles tácticos más compatibles con el jugador'},
        'tactical_style_tooltip': {'pt': 'Estilos táticos de maior compatibilidade com o jogador','en': 'Tactical styles most compatible with the player','bg': 'Тактически стилове, които са най-съвместими с играча','es': 'Estilos tácticos más compatibles con el jugador'},
        'optimal_role': {'pt': 'Função Ideal','en': 'Optimal Role','bg': 'Оптимална Роля','es': 'Rol Óptimo'},
        'age': {'pt': 'Idade','en': 'Age','bg': 'Възраст','es': 'Edad'},
        'birth_date': {'pt': 'Data de Nascimento','en': 'Birth Date','bg': 'Дата на Раждане','es': 'Fecha de Nacimiento'},
        'nationality': {'pt': 'Nacionalidade','en': 'Nationality','bg': 'Националност','es': 'Nacionalidad'},
        'height': {'pt': 'Altura','en': 'Height','bg': 'Височина','es': 'Altura'},
        'weight': {'pt': 'Peso','en': 'Weight','bg': 'Тегло','es': 'Peso'},
        'foot': {'pt': 'Pé Dominante','en': 'Dominant Foot','bg': 'Доминиращ Крак','es': 'Pie Dominante'},
        'positions': {'pt': 'Posições','en': 'Positions','bg': 'Позиции','es': 'Posiciones'},
        'current_club': {'pt': 'Clube Atual','en': 'Current Club','bg': 'Настоящ Клуб','es': 'Club Actual'},
        'contract_until': {'pt': 'Contrato até','en': 'Contract until','bg': 'Договор до','es': 'Contrato hasta'},
        'agent': {'pt': 'Agente','en': 'Agent','bg': 'Агент','es': 'Agente'},
        'strengths': {'pt': 'Pontos Fortes','en': 'Strengths','bg': 'Силни Страни','es': 'Fortalezas'},
        'weaknesses': {'pt': 'Pontos Fracos','en': 'Weaknesses','bg': 'Слаби Страни','es': 'Debilidades'},
        'opportunities': {'pt': 'Oportunidades','en': 'Opportunities','bg': 'Възможности','es': 'Oportunidades'},
        'threats': {'pt': 'Ameaças','en': 'Threats','bg': 'Заплахи','es': 'Amenazas'},
        'summary': {'pt': 'Resumo','en': 'Summary','bg': 'Резюме','es': 'Resumen'},
        'percentiles_tooltip': {'pt': 'Percentis em comparação com outros jogadores na mesma posição','en': 'Percentiles compared to other players in the same position','bg': 'Проценти в сравнение с други играчи на същата позиция','es': 'Percentiles en comparación con otros jugadores en la misma posición'},
        'ranking_tooltip': {'pt': 'Ranking em comparação com outros jogadores na mesma posição','en': 'Ranking compared to other players in the same position','bg': 'Ранжиране в сравнение с други играчи на същата позиция','es': 'Clasificación en comparación con otros jugadores en la misma posición'},
        'injury_type': {'pt': 'Tipo de Lesão','en': 'Injury Type','bg': 'Тип на Контузията','es': 'Tipo de Lesión'},
        'from_club': {'pt': 'Clube de Origem','en': 'From Club','bg': 'От Клуб','es': 'Desde Club'},
        'to_club': {'pt': 'Clube de Destino','en': 'To Club','bg': 'До Клуб','es': 'Hasta Club'},
        'from_date': {'pt': 'Data de Início','en': 'From Date','bg': 'От Дата','es': 'Fecha de Inicio'},
        'until_date': {'pt': 'Data de Retorno','en': 'Until Date','bg': 'До Дата','es': 'Fecha de Retorno'},
        'days_missed': {'pt': 'Dias Ausente','en': 'Days Missed','bg': 'Пропуснати Дни','es': 'Días Perdidos'},
        'date': {'pt': 'Data','en': 'Date','bg': 'Дата','es': 'Fecha'},
        'value': {'pt': 'Valor','en': 'Value','bg': 'Стойност','es': 'Valor'},
        'club': {'pt': 'Clube','en': 'Club','bg': 'Клуб','es': 'Club'},
        'attack_patterns': {'pt': 'Padrões de Ataque','en': 'Attack Patterns','bg': 'Модели на Атака','es': 'Patrones de Ataque'},
        'defensive_contribution': {'pt': 'Contribuição Defensiva','en': 'Defensive Contribution','bg': 'Защитен Принос','es': 'Contribución Defensiva'},
        'physical_technical_profile': {'pt': 'Perfil Físico e Técnico','en': 'Physical & Technical Profile','bg': 'Физически и Технически Профил','es': 'Perfil Físico y Técnico'},
        'tactical_flexibility': {'pt': 'Flexibilidade Tática','en': 'Tactical Flexibility','bg': 'Тактическа Гъвкавост','es': 'Flexibilidad Táctica'},
        'contextual_recommendations': {'pt': 'Recomendações Contextuais','en': 'Contextual Recommendations','bg': 'Контекстуални Препоръки','es': 'Recomendaciones Contextuales'},
        'overall_summary': {'pt': 'Resumo Geral','en': 'Overall Summary','bg': 'Общо Резюме','es': 'Resumen General'},
        'acquisition_viability': {'pt': 'Viabilidade de Aquisição','en': 'Acquisition Viability','bg': 'Осъществимост на Придобиването','es': 'Viabilidad de Adquisición'},
        'technical_tactical_fit': {'pt': 'Encaixe Técnico-Tático','en': 'Technical-Tactical Fit','bg': 'Техническо-Тактическо Съответствие','es': 'Ajuste Técnico-Táctico'},
        'age_development_profile': {'pt': 'Perfil de Idade/Desenvolvimento','en': 'Age/Development Profile','bg': 'Възрастов/Развитиен Профил','es': 'Perfil de Edad/Desarrollo'},
        'final_recommendation': {'pt': 'Recomendação Final','en': 'Final Recommendation','bg': 'Крайна Препоръка','es': 'Recomendación Final'},
        'acquisition_strategy': {'pt': 'Estratégia de Aquisição','en': 'Acquisition Strategy','bg': 'Стратегия за Придобиване','es': 'Estrategia de Adquisición'},
        'generated_on': {'pt': 'Gerado em','en': 'Generated on','bg': 'Генериран на','es': 'Generado el'},
        'report_id': {'pt': 'ID do Relatório','en': 'Report ID','bg': 'ID на Доклада','es': 'ID del Informe'},
        'percentiles':{'pt': 'Tabela de Percentis','en': 'Percentiles Table','bg': 'Таблица с Проценти','es': 'Tabla de Percentiles'},
        'importance': {'pt': 'Importância','en': 'Importance','bg': 'Важност','es': 'Importancia'},
        'high': {'pt': 'Alta','en': 'High','bg': 'Висока','es': 'Alta'},
        'medium': {'pt': 'Média','en': 'Medium','bg': 'Средна','es': 'Media'},
        'low': {'pt': 'Baixa','en': 'Low','bg': 'Ниска','es': 'Baja'},
        'not_available': {'pt': 'Não disponível','en': 'Not available','bg': 'Не е налично','es': 'No disponible'},
        'confidential': {'pt': 'Confidencial','en': 'Confidential','bg': 'Поверително','es': 'Confidencial'},
        'rank': {'pt': 'Ranking','en': 'Ranking','bg': 'Ранжиране','es': 'Clasificación'},
        'key_metrics': {'pt': 'Métricas Principais','en': 'Key Metrics','bg': 'Ключови Показатели','es': 'Métricas Clave'},
        'category': {'pt': 'Categoria','en': 'Category','bg': 'Категория','es': 'Categoría'},
        'stat_name': {'pt': 'Estatística','en': 'Statistic','bg': 'Статистика','es': 'Estadística'},
        'insight': {'pt': 'Insight','en': 'Insight','bg': 'Прозрение','es': 'Insight'},
        'based_on': {'pt': 'Baseado em','en': 'Based on','bg': 'Базирано на','es': 'Basado en'},
        'optimal_role': {'pt': 'Função Ideal','en': 'Optimal Role','bg': 'Оптимална Роля','es': 'Rol Óptimo'},
        'profile': {'pt': 'Perfil','en': 'Profile','bg': 'Профил','es': 'Perfil'},
        'score': {'pt': 'Pontuação','en': 'Score','bg': 'Резултат','es': 'Puntuación'},
        'description': {'pt': 'Descrição','en': 'Description','bg': 'Описание','es': 'Descripción'},
        'position': {'pt': 'Posição','en': 'Position','bg': 'Позиция','es': 'Posición'},
        'position_type': {'pt': 'Tipo de Posição','en': 'Position Type','bg': 'Тип Позиция','es': 'Tipo de Posición'},
        'best_fit': {'pt': 'Melhor Encaixe','en': 'Best Fit','bg': 'Най-добро Съответствие','es': 'Mejor Ajuste'},
        'best_score': {'pt': 'Melhor Pontuação','en': 'Best Score','bg': 'Най-добър Резултат','es': 'Mejor Puntuación'},
        'best_description': {'pt': 'Melhor Descrição','en': 'Best Description','bg': 'Най-добро Описание','es': 'Mejor Descripción'},
        'versatility': {'pt': 'Versatilidade','en': 'Versatility','bg': 'Многостранност','es': 'Versatilidad'},
        'position_count': {'pt': 'Número de Posições','en': 'Position Count','bg': 'Брой Позиции','es': 'Número de Posiciones'},
        'viable_roles_count': {'pt': 'Número de Funções Viáveis','en': 'Viable Roles Count','bg': 'Брой Жизнеспособни Роли','es': 'Número de Roles Viables'},
        'analysis': {'pt': 'Análise','en': 'Analysis','bg': 'Анализ','es': 'Análisis'},
        'areas_of_operation': {'pt': 'Áreas de Operação','en': 'Areas of Operation','bg': 'Области на Действие','es': 'Áreas de Operación'},
        'work_rate_assessment': {'pt': 'Avaliação de Taxa de Trabalho','en': 'Work Rate Assessment','bg': 'Оценка на Работния Темп','es': 'Evaluación de Ritmo de Trabajo'},
        'physical_strengths': {'pt': 'Pontos Fortes Físicos','en': 'Physical Strengths','bg': 'Физически Силни Страни','es': 'Fortalezas Físicas'},
        'technical_skills': {'pt': 'Habilidades Técnicas','en': 'Technical Skills','bg': 'Технически Умения','es': 'Habilidades Técnicas'},
        'playing_style': {'pt': 'Estilo de Jogo','en': 'Playing Style','bg': 'Стил на Игра','es': 'Estilo de Juego'},
        'best_systems': {'pt': 'Melhores Sistemas','en': 'Best Systems','bg': 'Най-добри Системи','es': 'Mejores Sistemas'},
        'unsuitable_systems': {'pt': 'Sistemas Inadequados','en': 'Unsuitable Systems','bg': 'Неподходящи Системи','es': 'Sistemas Inadecuados'},
        'reasoning': {'pt': 'Raciocínio','en': 'Reasoning','bg': 'Обосновка','es': 'Razonamiento'},
        'key_recommendations': {'pt': 'Recomendações Principais','en': 'Key Recommendations','bg': 'Ключови Препоръки','es': 'Recomendaciones Clave'},
        'complementary_player_types': {'pt': 'Tipos de Jogadores Complementares','en': 'Complementary Player Types','bg': 'Допълващи Типове Играчи','es': 'Tipos de Jugadores Complementarios'},
        'rationale': {'pt': 'Justificativa','en': 'Rationale','bg': 'Обосновка','es': 'Justificación'},
        'risk_factors': {'pt': 'Fatores de Risco','en': 'Risk Factors','bg': 'Рискови Фактори','es': 'Factores de Riesgo'},
        'system_compatibility': {'pt': 'Compatibilidade com Sistemas','en': 'System Compatibility','bg': 'Съвместимост със Системи','es': 'Compatibilidad con Sistemas'},
        'role_assessment': {'pt': 'Avaliação de Função','en': 'Role Assessment','bg': 'Оценка на Ролята','es': 'Evaluación de Rol'},
        'development_potential': {'pt': 'Potencial de Desenvolvimento','en': 'Development Potential','bg': 'Потенциал за Развитие','es': 'Potencial de Desarrollo'},
        'recommendation': {'pt': 'Recomendação','en': 'Recommendation','bg': 'Препоръка','es': 'Recomendación'},
        'justification': {'pt': 'Justificativa','en': 'Justification','bg': 'Обосновка','es': 'Justificación'},
        'overall_score': {'pt': 'Pontuação Geral','en': 'Overall Score','bg': 'Обща Оценка','es': 'Puntuación General'},
        'negotiation_approach': {'pt': 'Abordagem de Negociação','en': 'Negotiation Approach','bg': 'Подход за Преговори','es': 'Enfoque de Negociación'},
        'suggested_contract': {'pt': 'Contrato Sugerido','en': 'Suggested Contract','bg': 'Предложен Договор','es': 'Contrato Sugerido'},
        'integration_plan': {'pt': 'Plano de Integração','en': 'Integration Plan','bg': 'План за Интеграция','es': 'Plan de Integración'},
        'key_considerations': {'pt': 'Considerações Principais','en': 'Key Considerations','bg': 'Ключови Съображения','es': 'Consideraciones Clave'}
    }
    
    @classmethod
    def get_translation(cls, key: str, language: str) -> str:
        if language not in cls.SUPPORTED_LANGUAGES:
            language = 'pt' 
        if key in cls.TRANSLATIONS:
            return cls.TRANSLATIONS[key].get(language, key)
        return key

class ScoutReportProcessor:
    def __init__(self, language: str = 'pt'):
        if language not in TranslationManager.SUPPORTED_LANGUAGES:
            language = 'pt'
        self.language = language
        self.visualization_module = PlayerVisualizationModule()
        self.ai_content_generator = ScoutingReportAI(language=language)
        self.report_id = str(uuid.uuid4())[:8].upper()
        self.generation_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def translate(self, key: str) -> str:
        return TranslationManager.get_translation(key, self.language)
    
    def _format_timestamp(self, timestamp: Optional[int], date_format: str = '%Y-%m-%d') -> str: # Helper moved here
        if not timestamp: return "N/A"
        try: return datetime.fromtimestamp(timestamp).strftime(date_format)
        except: return "N/A"

    def process_player_data(self, player_id_str: str, player_model_obj: Any, 
                           historical_data: Optional[PlayerData], technical_analysis: Any, db: Session) -> Dict[str, Any]:
        template_data = {
            'language': self.language,
            'report_id': self.report_id,
            'generation_date': self.generation_date,
            'player': self._process_player_info(player_model_obj, db), 
            'market_value_data': self._process_market_value_data(historical_data) if historical_data else [],
            'injuries': self._process_injuries(historical_data) if historical_data else [],
            'transfers': self._process_transfers(historical_data) if historical_data else [],
            'swot': self._process_swot_analysis(technical_analysis),
            'tactical_fit': self._process_tactical_fit(technical_analysis),
            'tactical_styles': self._process_tactical_styles(technical_analysis),
            'percentiles': self._process_percentiles(technical_analysis),
            'ranking': self._process_ranking(technical_analysis),
            'radar_data': self._process_radar_data(technical_analysis),
            'content': self._generate_ai_content(player_id_str, technical_analysis, historical_data, db),
            'translations': self._get_translations_for_template()
        }
        return template_data
    
    def _process_player_info(self, player_obj: Any, db: Session) -> Dict[str, Any]:
        age_val = "N/A"
        if player_obj.date_of_birth_timestamp:
            try:
                birth_date = datetime.fromtimestamp(player_obj.date_of_birth_timestamp)
                today = datetime.today()
                age_val = str(today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day)))
            except: pass
        
        birth_date_str = self._format_timestamp(player_obj.date_of_birth_timestamp)
        nationality_str = player_obj.country.name if player_obj.country else "N/A"
        display_pos_str = DB_TO_GRANULAR_FALLBACK_MAP.get(player_obj.position, player_obj.position)

        club_name_str = "Unknown Club" 
        # Simplified: currentTeamId logic was complex and based on old JSON structure.
        # A proper implementation would involve PlayerTeam relationship and is_current flag.
        # Example: if player_obj.player_teams:
        #    current_team_relation = next((pt for pt in player_obj.player_teams if pt.is_current), None)
        #    if current_team_relation and current_team_relation.team:
        #        club_name_str = current_team_relation.team.name
        #    elif player_obj.player_teams: # Fallback to first team if no current
        #        club_name_str = player_obj.player_teams[0].team.name if player_obj.player_teams[0].team else "N/A"
        
        contract_until_val = self._format_timestamp(player_obj.contract_until_timestamp)
        
        return {
            'id': str(player_obj.id),
            'name': player_obj.name,
            'age': age_val,
            'birth_date': birth_date_str,
            'nationality': nationality_str,
            'height': player_obj.height or "N/A",
            'weight': "N/A", 
            'foot': player_obj.preferred_foot or "N/A",
            'positions': [display_pos_str], 
            'club': club_name_str,
            'contract_until': contract_until_val,
            'agent': "N/A", 
            'image_url': "" 
        }

    def _process_market_value_data(self, historical_data: Optional[PlayerData]) -> List[Dict[str, Any]]:
        if not historical_data or not historical_data.market_value_history: return []
        # ... (rest of the method, assuming it's largely okay but check for dict vs object access if PlayerData fields changed)
        market_values = []
        for mv in historical_data.market_value_history:
            date_str = getattr(mv, 'date', None)
            if isinstance(date_str, datetime): date_str = date_str.strftime("%Y-%m-%d")
            elif not isinstance(date_str, str): date_str = 'N/A'
            
            value_str = getattr(mv, 'market_value', '0')
            value_num = self._parse_currency_value(value_str)
            
            market_values.append({
                'date': date_str, 'value': value_num, 
                'value_display': value_str, 'club': getattr(mv, 'club_name', '')
            })
        market_values.sort(key=lambda x: x['date'] if x['date'] != 'N/A' else '0000-00-00')
        return market_values

    def _parse_currency_value(self, value_str: str) -> float:
        if not isinstance(value_str, str):
            return float(value_str) / 1000000.0 if isinstance(value_str, (int, float)) else 0.0
        cleaned_value = value_str.replace('€', '').replace('$', '').replace('£', '')
        try:
            if 'M' in cleaned_value.upper(): return float(cleaned_value.upper().replace('M', ''))
            if 'K' in cleaned_value.upper(): return float(cleaned_value.upper().replace('K', '')) / 1000.0
            return float(cleaned_value) / 1000000.0
        except ValueError: return 0.0

    def _process_injuries(self, historical_data: Optional[PlayerData]) -> List[Dict[str, Any]]:
        if not historical_data or not historical_data.injuries: return []
        # ... (rest of the method)
        processed_injuries = []
        for injury in historical_data.injuries:
            from_date = getattr(injury, 'from_date', None)
            until_date = getattr(injury, 'until_date', None)
            if isinstance(from_date, datetime): from_date = from_date.strftime("%d/%m/%Y")
            if isinstance(until_date, datetime): until_date = until_date.strftime("%d/%m/%Y")
            
            days_missed = getattr(injury, 'days_missed', 'N/A')
            processed_injuries.append({
                'type': getattr(injury, 'injury', 'N/A'), 'from_date': from_date or 'N/A',
                'until_date': until_date or 'N/A', 'days_missed': days_missed
            })
        processed_injuries.sort(key=lambda x: datetime.strptime(x['from_date'], "%d/%m/%Y") if x['from_date'] != 'N/A' else datetime.min, reverse=True)
        return processed_injuries

    def _process_transfers(self, historical_data: Optional[PlayerData]) -> List[Dict[str, Any]]:
        if not historical_data or not historical_data.transfers: return []
        # ... (rest of the method)
        processed_transfers = []
        for transfer in historical_data.transfers:
            date_str = getattr(transfer, 'date', None)
            if isinstance(date_str, datetime): date_str = date_str.strftime("%d/%m/%Y")
            elif not isinstance(date_str, str): date_str = 'N/A'

            from_club = getattr(transfer.club_from, 'name', 'N/A') if hasattr(transfer, 'club_from') and transfer.club_from else 'N/A'
            to_club = getattr(transfer.club_to, 'name', 'N/A') if hasattr(transfer, 'club_to') and transfer.club_to else 'N/A'
            fee_str = getattr(transfer, 'fee', 'N/A')
            
            processed_transfers.append({
                'date': date_str, 'from_club': from_club, 'to_club': to_club,
                'fee': fee_str, 'is_loan': isinstance(fee_str, str) and "loan" in fee_str.lower()
            })
        processed_transfers.sort(key=lambda x: datetime.strptime(x['date'], "%d/%m/%Y") if x['date'] != 'N/A' else datetime.min, reverse=True)
        return processed_transfers
    
    def _process_swot_analysis(self, technical_analysis: Any) -> Dict[str, Any]:
        if not hasattr(technical_analysis, 'swot'): return {'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': [], 'summary': ''}
        swot = technical_analysis.swot
        return {
            'strengths': [{'text': getattr(s, 'stat_name', 'N/A'), 'percentile': getattr(s, 'percentile', None), 'category': getattr(s, 'category', 'N/A')} for s in getattr(swot, 'strengths', [])],
            'weaknesses': [{'text': getattr(w, 'stat_name', 'N/A'), 'percentile': getattr(w, 'percentile', None), 'category': getattr(w, 'category', 'N/A')} for w in getattr(swot, 'weaknesses', [])],
            'opportunities': [{'insight': getattr(o, 'insight', 'N/A'), 'based_on': getattr(o, 'based_on', []), 'importance': getattr(o, 'importance', 2)} for o in getattr(swot, 'opportunities', [])],
            'threats': [{'insight': getattr(t, 'insight', 'N/A'), 'based_on': getattr(t, 'based_on', []), 'importance': getattr(t, 'importance', 2)} for t in getattr(swot, 'threats', [])],
            'summary': getattr(swot, 'summary', '')
        }

    def _process_tactical_fit(self, technical_analysis: Any) -> Dict[str, Any]:
        if not hasattr(technical_analysis, 'tactical_fit'): return {} # Default empty
        # ... (Ensure this function correctly processes the structure of technical_analysis.tactical_fit)
        # This function seems to expect technical_analysis.tactical_fit to be an object with attributes.
        # If technical_analysis.tactical_fit is a dictionary, access needs to be dict.get('attribute_name')
        # For now, assuming it's an object as per original access pattern.
        tf = technical_analysis.tactical_fit
        return {
            'player_name': getattr(tf, 'player_name', 'N/A'),
            'best_fits': [{'profile': getattr(f, 'profile', 'N/A'), 'score': getattr(f, 'score', 0), 'description': getattr(f, 'description', 'N/A')} for f in getattr(tf, 'best_fits', [])[:5]], # Top 5
            'optimal_role': {'profile': getattr(tf.optimal_role, 'profile', 'N/A'), 'score': getattr(tf.optimal_role, 'score', 0)} if hasattr(tf, 'optimal_role') and tf.optimal_role else {}
        }

    def _process_tactical_styles(self, technical_analysis: Any) -> List[Dict[str, Any]]:
        if not hasattr(technical_analysis, 'tactical_styles') or not isinstance(technical_analysis.tactical_styles, dict): return []
        best_fits = technical_analysis.tactical_styles.get('best_fits', [])
        return [{'style': fit.get('style_name', 'N/A'), 'score': fit.get('style_score', 0), 'description': fit.get('style_description', '')} for fit in best_fits[:5]] # Top 5


    def _process_percentiles(self, technical_analysis: Any) -> Dict[str, Any]:
        return {
            'percentiles': getattr(technical_analysis, 'percentiles', {}),
            'percentiles_by_category': getattr(technical_analysis, 'percentiles_by_category', {}),
            'position_group': getattr(technical_analysis, 'position_group', 'N/A')
        }

    def _process_ranking(self, technical_analysis: Any) -> List[Dict[str, Any]]:
        if not hasattr(technical_analysis, 'ranking'): return []
        # ... (Ensure this function correctly processes the structure of technical_analysis.ranking)
        # Assuming ranking is a list of objects/dicts with 'position', 'rank', 'key_metrics', 'metrics_percentiles'
        processed_ranking = []
        for rank_item_dict in getattr(technical_analysis, 'ranking', []):
             for position, item_data in rank_item_dict.items(): # rank_item_dict is like {'GK': RankingItem(...)}
                item_data_obj = item_data # If it's already an object
                if isinstance(item_data, dict) : # If it's a dict, create a simple obj for consistent access
                    item_data_obj = type('obj', (object,), item_data)

                processed_ranking.append({
                    'position': position,
                    'rank': getattr(item_data_obj, 'rank', 'N/A'),
                    'key_metrics': getattr(item_data_obj, 'key_metrics', []),
                    'metrics_percentiles': getattr(item_data_obj, 'metrics_percentiles', {})
                })
        return processed_ranking


    def _process_radar_data(self, technical_analysis: Any) -> Dict[str, Any]:
        # ... (Ensure this function correctly processes the structure of technical_analysis for radar data)
        # This function is complex and highly dependent on the structure of technical_analysis.ranking and technical_analysis.tactical_fit
        # For now, returning empty dicts to avoid errors. A full review is needed based on actual technical_analysis structure.
        return {'metrics': {}, 'tactical_profiles': {}}
        
      
    def _generate_ai_content(self, player_id_str: str, technical_analysis: Any, 
                       historical_data: Optional[PlayerData], db: Session) -> Dict[str, Any]:
        try:
            player_id_int = int(player_id_str) 
            executive_summary = self.ai_content_generator.generate_executive_summary(player_id_int, technical_analysis, db)
            tactical_analysis_content = self.ai_content_generator.generate_tactical_analysis(player_id_int, technical_analysis, db)
            recruitment_recommendation_content = self.ai_content_generator.generate_recruitment_recommendation(player_id_int, technical_analysis, historical_data, db)
            
            return {
                'executive_summary': executive_summary,
                'tactical_analysis': tactical_analysis_content,
                'recruitment_recommendation': recruitment_recommendation_content
            }
        except Exception as e:
            print(f"Error in _generate_ai_content: {str(e)}")
            return {'executive_summary': "Error generating AI content.", 'tactical_analysis': {}, 'recruitment_recommendation': {}}

    def _get_translations_for_template(self) -> Dict[str, str]:
        translations = {}
        for key in TranslationManager.TRANSLATIONS:
            translations[key] = self.translate(key)
        return translations

def generate_scout_report(player_id: str, language: str = 'pt', db: Session = None) -> Dict[str, Any]: # Added db with default None for safety
    # This global function is the main entry point from app.py
    # It MUST handle the db session correctly.
    
    db_session_managed_here = False
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        db_session_managed_here = True
    
    try:
        player_id_int = 0
        try:
            player_id_int = int(player_id)
        except ValueError:
            raise ValueError(f"Invalid player ID format: {player_id}")

        player_obj = find_player_by_id_service(player_id=player_id_int, db=db)
        if not player_obj:
            raise ValueError(f"Jogador com ID {player_id_int} não encontrado.")
        
        player_name = player_obj.name
        
        from core.transfermarkt import get_player_data 
        historical_data = get_player_data(player_name) # This does not require DB
        
        from core.data_analysis import complete_data_analysis 
        technical_analysis = complete_data_analysis(player_id=player_id_int, language=language, db=db)
        
        processor = ScoutReportProcessor(language=language) 
        template_data = processor.process_player_data(
            player_id, player_obj, historical_data, technical_analysis, db
        )
        return template_data
    finally:
        if db_session_managed_here:
            next(db_gen, None) # Close session only if managed here
