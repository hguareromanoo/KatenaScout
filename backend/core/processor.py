"""
Processador e integrador de dados para relatórios de scout de futebol.
Este módulo prepara os dados para inicialização em templates Jinja2 com gráficos interativos.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import uuid
import base64
from io import BytesIO
import numpy as np
from pydantic import BaseModel

# Importações dos módulos existentes
from core.transfermarkt import PlayerData, PlayerVisualizationModule
from core.data_analysis import z_score_and_percentiles_aprimorado, calculate_profile_fit
from core.generate_report import ScoutingReportAI


class TranslationManager:
    """Gerenciador de traduções para suporte a múltiplos idiomas."""
    
    # Idiomas suportados
    SUPPORTED_LANGUAGES = ['pt', 'en', 'bg', 'es']
    
    # Dicionário de traduções
    TRANSLATIONS = {
        # Seções do relatório
        'position_group':{
            'pt': 'Grupo de Posição',
            'en': 'Position Group',
            'bg': 'Група Позиции',
            'es': 'Grupo de Posición'
        },
        'report_title': {
            'pt': 'Relatório Avançado de Scouting',
            'en': 'Advanced Scouting Report',
            'bg': 'Разширен Скаутски Доклад',
            'es': 'Informe Avanzado de Scouting'
        },
# Categorias funcionais de percentis
        'attacking': {
            'pt': 'Ataque',
            'en': 'Attacking',
            'bg': 'Атака',
            'es': 'Ataque'
        },
        'passing': {
            'pt': 'Passe',
            'en': 'Passing',
            'bg': 'Подаване',
            'es': 'Pase'
        },
        'defensive': {
            'pt': 'Defesa',
            'en': 'Defensive',
            'bg': 'Защита',
            'es': 'Defensa'
        },
        'possession': {
            'pt': 'Posse de bola',
            'en': 'Possession',
            'bg': 'Притежание',
            'es': 'Posesión'
        },
        'physical': {
            'pt': 'Físico',
            'en': 'Physical',
            'bg': 'Физическо',
            'es': 'Físico'
        },
        'goalkeeping': {
            'pt': 'Goleiro',
            'en': 'Goalkeeping',
            'bg': 'Вратарски умения',
            'es': 'Portero'
        },
        'positioning': {
            'pt': 'Posicionamento',
            'en': 'Positioning',
            'bg': 'Позициониране',
            'es': 'Posicionamiento'
        },

        # Grupos de posição
        'goalkeeper': {
            'pt': 'Goleiro',
            'en': 'Goalkeeper',
            'bg': 'Вратар',
            'es': 'Portero'
        },
        'center_backs': {
            'pt': 'Zagueiros',
            'en': 'Center Backs',
            'bg': 'Централни защитници',
            'es': 'Defensas centrales'
        },
        'full_backs': {
            'pt': 'Laterais',
            'en': 'Full Backs',
            'bg': 'Странични защитници',
            'es': 'Laterales'
        },
        'midfielders': {
            'pt': 'Meio-campistas',
            'en': 'Midfielders',
            'bg': 'Полузащитници',
            'es': 'Centrocampistas'
        },
        'wingers': {
            'pt': 'Pontas',
            'en': 'Wingers',
            'bg': 'Крила',
            'es': 'Extremos'
        },
        'center_forwards': {
            'pt': 'Centroavantes',
            'en': 'Center Forwards',
            'bg': 'Централни нападатели',
            'es': 'Delanteros centros'
        },
        'outfield': {
            'pt': 'Jogador de linha',
            'en': 'Outfield Player',
            'bg': 'Полеви играч',
            'es': 'Jugador de campo'
        },

        # Chaves adicionais para o sistema de percentis
        'percentiles_by_category': {
            'pt': 'Percentis por Categoria',
            'en': 'Percentiles by Category',
            'bg': 'Проценти по Категории',
            'es': 'Percentiles por Categoría'
        },
        'original_percentiles': {
            'pt': 'Percentis Originais',
            'en': 'Original Percentiles',
            'bg': 'Оригинални Проценти',
            'es': 'Percentiles Originales'
        },
        'player_info': {
            'pt': 'Informações do Jogador',
            'en': 'Player Information',
            'bg': 'Информация за Играча',
            'es': 'Información del Jugador'
        },
        'executive_summary': {
            'pt': 'Resumo Executivo',
            'en': 'Executive Summary',
            'bg': 'Резюме',
            'es': 'Resumen Ejecutivo'
        },
        'comparative_analysis': {
            'pt': 'Análise Comparativa',
            'en': 'Comparative Analysis',
            'bg': 'Сравнителен Анализ',
            'es': 'Análisis Comparativo'
        },
        'tactical_analysis': {
            'pt': 'Análise Tática',
            'en': 'Tactical Analysis',
            'bg': 'Тактически Анализ',
            'es': 'Análisis Táctico'
        },
        'swot_analysis': {
            'pt': 'Análise SWOT',
            'en': 'SWOT Analysis',
            'bg': 'SWOT Анализ',
            'es': 'Análisis DAFO'
        },
        'injury_history': {
            'pt': 'Histórico de Lesões',
            'en': 'Injury History',
            'bg': 'История на Контузиите',
            'es': 'Historial de Lesiones'
        },
        'market_value': {
            'pt': 'Valor de Mercado',
            'en': 'Market Value',
            'bg': 'Пазарна Стойност',
            'es': 'Valor de Mercado'
        },
        'recruitment_recommendation': {
            'pt': 'Recomendação de Recrutamento',
            'en': 'Recruitment Recommendation',
            'bg': 'Препоръка за Набиране',
            'es': 'Recomendación de Fichaje'
        },
        'historical_analysis': {
            'pt': 'Análise Histórica',
            'en': 'Historical Analysis',
            'bg': 'Исторически Анализ',
            'es': 'Análisis Histórico'
        },
        'transfers': {
            'pt': 'Transferências',
            'en': 'Transfers',
            'bg': 'Трансфери',
            'es': 'Transferencias'
        },
        'tactical_roles':{
            'pt': 'Perfis Táticos',
            'en': 'Tactical Roles',
            'bg': 'Тактически Роли',
            'es': 'Roles Tácticos'
        },
        'tactical_styles' : {
            'pt': 'Estilos Táticos',
            'en': 'Tactical Styles',
            'bg': 'Тактически Стилове',
            'es': 'Estilos Tácticos'

        },
        'tactical_role_tooltip': {
            'pt': 'Perfis táticos de maior compatibilidade com o jogador',
            'en': 'Tactical profiles most compatible with the player',
            'bg': 'Тактически профили, които са най-съвместими с играча',
            'es': 'Perfiles tácticos más compatibles con el jugador'
        },
        'tactical_style_tooltip': {
            'pt': 'Estilos táticos de maior compatibilidade com o jogador',
            'en': 'Tactical styles most compatible with the player',
            'bg': 'Тактически стилове, които са най-съвместими с играча',
            'es': 'Estilos tácticos más compatibles con el jugador'
        },
        'optimal_role': {
            'pt': 'Função Ideal',
            'en': 'Optimal Role',
            'bg': 'Оптимална Роля',
            'es': 'Rol Óptimo'
        },

        # Campos de informações do jogador
        'age': {
            'pt': 'Idade',
            'en': 'Age',
            'bg': 'Възраст',
            'es': 'Edad'
        },
        'birth_date': {
            'pt': 'Data de Nascimento',
            'en': 'Birth Date',
            'bg': 'Дата на Раждане',
            'es': 'Fecha de Nacimiento'
        },
        'nationality': {
            'pt': 'Nacionalidade',
            'en': 'Nationality',
            'bg': 'Националност',
            'es': 'Nacionalidad'
        },
        'height': {
            'pt': 'Altura',
            'en': 'Height',
            'bg': 'Височина',
            'es': 'Altura'
        },
        'weight': {
            'pt': 'Peso',
            'en': 'Weight',
            'bg': 'Тегло',
            'es': 'Peso'
        },
        'foot': {
            'pt': 'Pé Dominante',
            'en': 'Dominant Foot',
            'bg': 'Доминиращ Крак',
            'es': 'Pie Dominante'
        },
        'positions': {
            'pt': 'Posições',
            'en': 'Positions',
            'bg': 'Позиции',
            'es': 'Posiciones'
        },
        'current_club': {
            'pt': 'Clube Atual',
            'en': 'Current Club',
            'bg': 'Настоящ Клуб',
            'es': 'Club Actual'
        },
        'contract_until': {
            'pt': 'Contrato até',
            'en': 'Contract until',
            'bg': 'Договор до',
            'es': 'Contrato hasta'
        },
        'agent': {
            'pt': 'Agente',
            'en': 'Agent',
            'bg': 'Агент',
            'es': 'Agente'
        },
        
        # SWOT Analysis
        'strengths': {
            'pt': 'Pontos Fortes',
            'en': 'Strengths',
            'bg': 'Силни Страни',
            'es': 'Fortalezas'
        },
        'weaknesses': {
            'pt': 'Pontos Fracos',
            'en': 'Weaknesses',
            'bg': 'Слаби Страни',
            'es': 'Debilidades'
        },
        'opportunities': {
            'pt': 'Oportunidades',
            'en': 'Opportunities',
            'bg': 'Възможности',
            'es': 'Oportunidades'
        },
        'threats': {
            'pt': 'Ameaças',
            'en': 'Threats',
            'bg': 'Заплахи',
            'es': 'Amenazas'
        },
        'summary': {
            'pt': 'Resumo',
            'en': 'Summary',
            'bg': 'Резюме',
            'es': 'Resumen'
        },

        'percentiles_tooltip': {
            'pt': 'Percentis em comparação com outros jogadores na mesma posição',
            'en': 'Percentiles compared to other players in the same position',
            'bg': 'Проценти в сравнение с други играчи на същата позиция',
            'es': 'Percentiles en comparación con otros jugadores en la misma posición'
        },
        'ranking_tooltip': {
            'pt': 'Ranking em comparação com outros jogadores na mesma posição',
            'en': 'Ranking compared to other players in the same position',
            'bg': 'Ранжиране в сравнение с други играчи на същата позиция',
            'es': 'Clasificación en comparación con otros jugadores en la misma posición'
        },
        # Injury History
        'injury_type': {
            'pt': 'Tipo de Lesão',
            'en': 'Injury Type',
            'bg': 'Тип на Контузията',
            'es': 'Tipo de Lesión'
        },
        'from_club': {
            'pt': 'Clube de Origem',
            'en': 'From Club',
            'bg': 'От Клуб',
            'es': 'Desde Club'
        },
        'to_club': {
            'pt': 'Clube de Destino',
            'en': 'To Club',
            'bg': 'До Клуб',
            'es': 'Hasta Club'
        },
        'from_date': {
            'pt': 'Data de Início',
            'en': 'From Date',
            'bg': 'От Дата',
            'es': 'Fecha de Inicio'
        },
        'until_date': {
            'pt': 'Data de Retorno',
            'en': 'Until Date',
            'bg': 'До Дата',
            'es': 'Fecha de Retorno'
        },
        'days_missed': {
            'pt': 'Dias Ausente',
            'en': 'Days Missed',
            'bg': 'Пропуснати Дни',
            'es': 'Días Perdidos'
        },
        
        # Market Value
        'date': {
            'pt': 'Data',
            'en': 'Date',
            'bg': 'Дата',
            'es': 'Fecha'
        },
        'value': {
            'pt': 'Valor',
            'en': 'Value',
            'bg': 'Стойност',
            'es': 'Valor'
        },
        'club': {
            'pt': 'Clube',
            'en': 'Club',
            'bg': 'Клуб',
            'es': 'Club'
        },
        'attack_patterns': {
            'pt': 'Padrões de Ataque',
            'en': 'Attack Patterns',
            'bg': 'Модели на Атака',
            'es': 'Patrones de Ataque'
        },
        'defensive_contribution': {
            'pt': 'Contribuição Defensiva',
            'en': 'Defensive Contribution',
            'bg': 'Защитен Принос',
            'es': 'Contribución Defensiva'
        },
        'physical_technical_profile': {
            'pt': 'Perfil Físico e Técnico',
            'en': 'Physical & Technical Profile',
            'bg': 'Физически и Технически Профил',
            'es': 'Perfil Físico y Técnico'
        },
        'tactical_flexibility': {
            'pt': 'Flexibilidade Tática',
            'en': 'Tactical Flexibility',
            'bg': 'Тактическа Гъвкавост',
            'es': 'Flexibilidad Táctica'
        },
        'contextual_recommendations': {
            'pt': 'Recomendações Contextuais',
            'en': 'Contextual Recommendations',
            'bg': 'Контекстуални Препоръки',
            'es': 'Recomendaciones Contextuales'
        },
        'overall_summary': {
            'pt': 'Resumo Geral',
            'en': 'Overall Summary',
            'bg': 'Общо Резюме',
            'es': 'Resumen General'
        },
        
        # Recruitment Recommendation
        'acquisition_viability': {
            'pt': 'Viabilidade de Aquisição',
            'en': 'Acquisition Viability',
            'bg': 'Осъществимост на Придобиването',
            'es': 'Viabilidad de Adquisición'
        },
        'technical_tactical_fit': {
            'pt': 'Encaixe Técnico-Tático',
            'en': 'Technical-Tactical Fit',
            'bg': 'Техническо-Тактическо Съответствие',
            'es': 'Ajuste Técnico-Táctico'
        },
        'age_development_profile': {
            'pt': 'Perfil de Idade/Desenvolvimento',
            'en': 'Age/Development Profile',
            'bg': 'Възрастов/Развитиен Профил',
            'es': 'Perfil de Edad/Desarrollo'
        },
        'final_recommendation': {
            'pt': 'Recomendação Final',
            'en': 'Final Recommendation',
            'bg': 'Крайна Препоръка',
            'es': 'Recomendación Final'
        },
        'acquisition_strategy': {
            'pt': 'Estratégia de Aquisição',
            'en': 'Acquisition Strategy',
            'bg': 'Стратегия за Придобиване',
            'es': 'Estrategia de Adquisición'
        },
        
        # Misc
        'generated_on': {
            'pt': 'Gerado em',
            'en': 'Generated on',
            'bg': 'Генериран на',
            'es': 'Generado el'
        },
        'report_id': {
            'pt': 'ID do Relatório',
            'en': 'Report ID',
            'bg': 'ID на Доклада',
            'es': 'ID del Informe'
        },
        'percentiles':{
            'pt': 'Tabela de Percentis',
            'en': 'Percentiles Table',
            'bg': 'Таблица с Проценти',
            'es': 'Tabla de Percentiles'
        },
        'importance': {
            'pt': 'Importância',
            'en': 'Importance',
            'bg': 'Важност',
            'es': 'Importancia'
        },
        'high': {
            'pt': 'Alta',
            'en': 'High',
            'bg': 'Висока',
            'es': 'Alta'
        },
        'medium': {
            'pt': 'Média',
            'en': 'Medium',
            'bg': 'Средна',
            'es': 'Media'
        },
        'low': {
            'pt': 'Baixa',
            'en': 'Low',
            'bg': 'Ниска',
            'es': 'Baja'
        },
        'not_available': {
            'pt': 'Não disponível',
            'en': 'Not available',
            'bg': 'Не е налично',
            'es': 'No disponible'
        },
        'confidential': {
            'pt': 'Confidencial',
            'en': 'Confidential',
            'bg': 'Поверително',
            'es': 'Confidencial'
        },
        'rank': {
            'pt': 'Ranking',
            'en': 'Ranking',
            'bg': 'Ранжиране',
            'es': 'Clasificación'
        },
        'key_metrics': {
            'pt': 'Métricas Principais',
            'en': 'Key Metrics',
            'bg': 'Ключови Показатели',
            'es': 'Métricas Clave'
        },
        'category': {
            'pt': 'Categoria',
            'en': 'Category',
            'bg': 'Категория',
            'es': 'Categoría'
        },
        'stat_name': {
            'pt': 'Estatística',
            'en': 'Statistic',
            'bg': 'Статистика',
            'es': 'Estadística'
        },
        'insight': {
            'pt': 'Insight',
            'en': 'Insight',
            'bg': 'Прозрение',
            'es': 'Insight'
        },
        'based_on': {
            'pt': 'Baseado em',
            'en': 'Based on',
            'bg': 'Базирано на',
            'es': 'Basado en'
        },
        'optimal_role': {
            'pt': 'Função Ideal',
            'en': 'Optimal Role',
            'bg': 'Оптимална Роля',
            'es': 'Rol Óptimo'
        },
        'profile': {
            'pt': 'Perfil',
            'en': 'Profile',
            'bg': 'Профил',
            'es': 'Perfil'
        },
        'score': {
            'pt': 'Pontuação',
            'en': 'Score',
            'bg': 'Резултат',
            'es': 'Puntuación'
        },
        'description': {
            'pt': 'Descrição',
            'en': 'Description',
            'bg': 'Описание',
            'es': 'Descripción'
        },
        'position': {
            'pt': 'Posição',
            'en': 'Position',
            'bg': 'Позиция',
            'es': 'Posición'
        },
        'position_type': {
            'pt': 'Tipo de Posição',
            'en': 'Position Type',
            'bg': 'Тип Позиция',
            'es': 'Tipo de Posición'
        },
        'best_fit': {
            'pt': 'Melhor Encaixe',
            'en': 'Best Fit',
            'bg': 'Най-добро Съответствие',
            'es': 'Mejor Ajuste'
        },
        'best_score': {
            'pt': 'Melhor Pontuação',
            'en': 'Best Score',
            'bg': 'Най-добър Резултат',
            'es': 'Mejor Puntuación'
        },
        'best_description': {
            'pt': 'Melhor Descrição',
            'en': 'Best Description',
            'bg': 'Най-добро Описание',
            'es': 'Mejor Descripción'
        },
        'versatility': {
            'pt': 'Versatilidade',
            'en': 'Versatility',
            'bg': 'Многостранност',
            'es': 'Versatilidad'
        },
        'position_count': {
            'pt': 'Número de Posições',
            'en': 'Position Count',
            'bg': 'Брой Позиции',
            'es': 'Número de Posiciones'
        },
        'viable_roles_count': {
            'pt': 'Número de Funções Viáveis',
            'en': 'Viable Roles Count',
            'bg': 'Брой Жизнеспособни Роли',
            'es': 'Número de Roles Viables'
        },
        'analysis': {
            'pt': 'Análise',
            'en': 'Analysis',
            'bg': 'Анализ',
            'es': 'Análisis'
        },
        'areas_of_operation': {
            'pt': 'Áreas de Operação',
            'en': 'Areas of Operation',
            'bg': 'Области на Действие',
            'es': 'Áreas de Operación'
        },
        'work_rate_assessment': {
            'pt': 'Avaliação de Taxa de Trabalho',
            'en': 'Work Rate Assessment',
            'bg': 'Оценка на Работния Темп',
            'es': 'Evaluación de Ritmo de Trabajo'
        },
        'physical_strengths': {
            'pt': 'Pontos Fortes Físicos',
            'en': 'Physical Strengths',
            'bg': 'Физически Силни Страни',
            'es': 'Fortalezas Físicas'
        },
        'technical_skills': {
            'pt': 'Habilidades Técnicas',
            'en': 'Technical Skills',
            'bg': 'Технически Умения',
            'es': 'Habilidades Técnicas'
        },
        'playing_style': {
            'pt': 'Estilo de Jogo',
            'en': 'Playing Style',
            'bg': 'Стил на Игра',
            'es': 'Estilo de Juego'
        },
        'best_systems': {
            'pt': 'Melhores Sistemas',
            'en': 'Best Systems',
            'bg': 'Най-добри Системи',
            'es': 'Mejores Sistemas'
        },
        'unsuitable_systems': {
            'pt': 'Sistemas Inadequados',
            'en': 'Unsuitable Systems',
            'bg': 'Неподходящи Системи',
            'es': 'Sistemas Inadecuados'
        },
        'reasoning': {
            'pt': 'Raciocínio',
            'en': 'Reasoning',
            'bg': 'Обосновка',
            'es': 'Razonamiento'
        },
        'key_recommendations': {
            'pt': 'Recomendações Principais',
            'en': 'Key Recommendations',
            'bg': 'Ключови Препоръки',
            'es': 'Recomendaciones Clave'
        },
        'complementary_player_types': {
            'pt': 'Tipos de Jogadores Complementares',
            'en': 'Complementary Player Types',
            'bg': 'Допълващи Типове Играчи',
            'es': 'Tipos de Jugadores Complementarios'
        },
        'rationale': {
            'pt': 'Justificativa',
            'en': 'Rationale',
            'bg': 'Обосновка',
            'es': 'Justificación'
        },
        'risk_factors': {
            'pt': 'Fatores de Risco',
            'en': 'Risk Factors',
            'bg': 'Рискови Фактори',
            'es': 'Factores de Riesgo'
        },
        'system_compatibility': {
            'pt': 'Compatibilidade com Sistemas',
            'en': 'System Compatibility',
            'bg': 'Съвместимост със Системи',
            'es': 'Compatibilidad con Sistemas'
        },
        'role_assessment': {
            'pt': 'Avaliação de Função',
            'en': 'Role Assessment',
            'bg': 'Оценка на Ролята',
            'es': 'Evaluación de Rol'
        },
        'development_potential': {
            'pt': 'Potencial de Desenvolvimento',
            'en': 'Development Potential',
            'bg': 'Потенциал за Развитие',
            'es': 'Potencial de Desarrollo'
        },
        'recommendation': {
            'pt': 'Recomendação',
            'en': 'Recommendation',
            'bg': 'Препоръка',
            'es': 'Recomendación'
        },
        'justification': {
            'pt': 'Justificativa',
            'en': 'Justification',
            'bg': 'Обосновка',
            'es': 'Justificación'
        },
        'overall_score': {
            'pt': 'Pontuação Geral',
            'en': 'Overall Score',
            'bg': 'Обща Оценка',
            'es': 'Puntuación General'
        },
        'negotiation_approach': {
            'pt': 'Abordagem de Negociação',
            'en': 'Negotiation Approach',
            'bg': 'Подход за Преговори',
            'es': 'Enfoque de Negociación'
        },
        'suggested_contract': {
            'pt': 'Contrato Sugerido',
            'en': 'Suggested Contract',
            'bg': 'Предложен Договор',
            'es': 'Contrato Sugerido'
        },
        'integration_plan': {
            'pt': 'Plano de Integração',
            'en': 'Integration Plan',
            'bg': 'План за Интеграция',
            'es': 'Plan de Integración'
        },
        'key_considerations': {
            'pt': 'Considerações Principais',
            'en': 'Key Considerations',
            'bg': 'Ключови Съображения',
            'es': 'Consideraciones Clave'
        }
    }
    
    @classmethod
    def get_translation(cls, key: str, language: str) -> str:
        """
        Obtém a tradução para uma chave específica no idioma solicitado.
        
        Args:
            key: Chave de tradução
            language: Código do idioma (pt, en, bg, es)
            
        Returns:
            Texto traduzido ou a própria chave se não encontrada
        """
        if language not in cls.SUPPORTED_LANGUAGES:
            language = 'pt'  # Idioma padrão
            
        if key in cls.TRANSLATIONS:
            return cls.TRANSLATIONS[key].get(language, key)
        
        return key


class ScoutReportProcessor:
    """
    Processador e integrador de dados para relatórios de scout.
    Prepara os dados para inicialização em templates Jinja2 com gráficos interativos.
    """
    
    def __init__(self, language: str = 'pt'):
        """
        Inicializa o processador de relatórios.
        
        Args:
            language: Código do idioma para o relatório (pt, en, bg, es)
        """
        if language not in TranslationManager.SUPPORTED_LANGUAGES:
            language = 'pt'  # Idioma padrão
            
        self.language = language
        self.visualization_module = PlayerVisualizationModule()
        self.ai_content_generator = ScoutingReportAI(language=language)
        self.report_id = str(uuid.uuid4())[:8].upper()
        self.generation_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def translate(self, key: str) -> str:
        """
        Obtém a tradução para uma chave específica no idioma do relatório.
        
        Args:
            key: Chave de tradução
            
        Returns:
            Texto traduzido
        """
        return TranslationManager.get_translation(key, self.language)
    
    def process_player_data(self, player_id: str, player_data: Dict[str, Any], 
                           historical_data: PlayerData, technical_analysis: Any) -> Dict[str, Any]:
        """
        Processa todos os dados do jogador e prepara para o template.
        
        Args:
            player_id: ID do jogador
            player_data: Dados básicos do jogador
            historical_data: Dados históricos (lesões, valor de mercado, transferências)
            technical_analysis: Análise técnica do jogador
            
        Returns:
            Dicionário com todos os dados processados para o template
        """
        # Inicializa o dicionário de dados para o template
        template_data = {
            'language': self.language,
            'report_id': self.report_id,
            'generation_date': self.generation_date,
            'player': self._process_player_info(player_data),
            'market_value_data': self._process_market_value_data(historical_data),
            'injuries': self._process_injuries(historical_data),
            'transfers': self._process_transfers(historical_data),
            'swot': self._process_swot_analysis(technical_analysis),
            'tactical_fit': self._process_tactical_fit(technical_analysis),
            'tactical_styles': self._process_tactical_styles(technical_analysis),
            'percentiles': self._process_percentiles(technical_analysis),
            'ranking': self._process_ranking(technical_analysis),
            'radar_data': self._process_radar_data(technical_analysis),
            'content': self._generate_ai_content(player_id, technical_analysis, historical_data),
            'translations': self._get_translations_for_template()
        }
        
        return template_data
    
    def _process_player_info(self, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa as informações básicas do jogador.
        
        Args:
            player_data: Dados do jogador
            
        Returns:
            Dicionário com informações processadas do jogador
        """
        # Extrai posições de forma segura
        positions = []
        if 'positions' in player_data and player_data['positions']:
            for pos in player_data['positions']:
                if isinstance(pos, dict):
                    if 'position' in pos and isinstance(pos['position'], dict):
                        positions.append(pos['position'].get('name', 'Unknown'))
                    else:
                        positions.append(pos.get('name', 'Unknown'))
                else:
                    positions.append(str(pos))
        from services.data_service import find_club_by_id
        if player_data.get('currentTeamId') is None:
            club_name = "N/A"
        else:
            if find_club_by_id(str(player_data.get('currentTeamId'))) is None:
                club_name = "N/A"
            else:
                club_name = find_club_by_id(str(player_data.get('currentTeamId'))).get('name', 'N/A')
        # Extrai informações de contrato
        contract_until = "N/A"
        if 'contract' in player_data and player_data['contract']:
            contract_until = player_data['contract'].get('contractExpiration', 'N/A')
        
        # Processa o agente (agências) do jogador
        agent = "N/A"
        if 'contract' in player_data and player_data['contract']:
            agencies = player_data['contract'].get('agencies', [])
            if isinstance(agencies, list):
                agent = ", ".join(agencies)
        # Processa e retorna as informações do jogador
        return {
            'id': player_data.get('playerId', 'N/A'),
            'name': player_data.get('name', 'N/A'),
            'age': player_data.get('age', 'N/A'),
            'birth_date': player_data.get('birthDate', 'N/A'),
            'nationality': player_data['birthArea'].get('name', 'N/A'),
            'height': player_data.get('height', 'N/A'),
            'weight': player_data.get('weight', 'N/A'),
            'foot': player_data.get('foot', 'N/A'),
            'positions': positions,
            'club': club_name,
            'contract_until': contract_until,
            'agent': agent,
            'image_url': player_data.get('imageDataURL', '')
        }
    
    def _process_market_value_data(self, historical_data: PlayerData) -> List[Dict[str, Any]]:
        """
        Processa os dados de valor de mercado para gráfico interativo.
        
            historical_data: Dados históricos do jogador
          
        Returns:
            Lista de dicionários com dados de valor de mercado
        """
        if not historical_data or not historical_data.market_value_history:
            return []
        
        market_values = []
        
        for mv in historical_data.market_value_history:
            if hasattr(mv, 'date') and hasattr(mv, 'market_value'):
                # Converte a data para formato adequado
                date_str = mv.date
                if not isinstance(date_str, str) and date_str is not None:
                    date_str = date_str.strftime("%Y-%m-%d")
                
                # Extract and parse the value - log for debugging
                value_str = mv.market_value
                value_num = self._parse_currency_value(value_str)
                print(f"Parsing market value: '{value_str}' -> {value_num}")
                
                # Adiciona ao array
                market_values.append({
                    'date': date_str,
                    'value': value_num,
                    'value_display': value_str,
                    'club': getattr(mv, 'club_name', '')
                })
        
        # Ordena por data
        market_values.sort(key=lambda x: x['date'])
        
        # Log the processed values
        print(f"Processed {len(market_values)} market values")
        if market_values:
            print(f"Example value: date={market_values[0]['date']}, value={market_values[0]['value']}, display={market_values[0]['value_display']}")
        
        return market_values

    def _parse_currency_value(self, value_str: str) -> float:
        """
        Converte uma string de valor monetário para um número.
        
        Args:
            value_str: String de valor monetário (ex: "€10M", "€500K")
            
        Returns:
            Valor numérico em milhões
        """
        if not isinstance(value_str, str):
            if isinstance(value_str, (int, float)):
                # If it's already a number, convert to millions
                value_in_millions = float(value_str) / 1000000
                print(f"Numeric input: {value_str} -> {value_in_millions}M")
                return value_in_millions
            else:
                print(f"Invalid market value type: {type(value_str)}")
                return 0.0
        
        # Log input for debugging
        print(f"Parsing currency value: '{value_str}'")
        
        # Remove o símbolo de moeda
        cleaned_value = value_str.replace('€', '').replace('$', '').replace('£', '')
        
        # Converte para valor numérico
        try:
            if 'M' in cleaned_value:
                value = float(cleaned_value.replace('M', ''))
                print(f"Parsed as M value: {value}")
                return value
            elif 'm' in cleaned_value:
                value = float(cleaned_value.replace('m', ''))
                print(f"Parsed as m value: {value}")
                return value
            elif 'K' in cleaned_value:
                value = float(cleaned_value.replace('K', '')) / 1000
                print(f"Parsed as K value: {value/1000}")
                return value
            elif 'k' in cleaned_value:
                value = float(cleaned_value.replace('k', '')) / 1000
                print(f"Parsed as k value: {value/1000}")
                return value
            else:
                # Try to parse as raw number
                value = float(cleaned_value) / 1000000
                print(f"Parsed as raw number: {value}")
                return value
        except ValueError as e:
            print(f"Error parsing currency value '{value_str}': {str(e)}")
            return 0.0
    
    def _process_injuries(self, historical_data: PlayerData) -> List[Dict[str, Any]]:
        """
        Processa o histórico de lesões do jogador.
        
        Args:
            historical_data: Dados históricos do jogador
            
        Returns:
            Lista de lesões processadas
        """
        if not historical_data or not historical_data.injuries:
            return []
        
        processed_injuries = []
        
        for injury in historical_data.injuries:
            # Formata as datas
            from_date = getattr(injury, 'from_date', 'N/A')
            if from_date != 'N/A' and not isinstance(from_date, str) and from_date is not None:
                from_date = from_date.strftime("%d/%m/%Y")
                
            until_date = getattr(injury, 'until_date', 'N/A')
            if until_date != 'N/A' and not isinstance(until_date, str) and until_date is not None:
                until_date = until_date.strftime("%d/%m/%Y")
            
            # Calcula a duração
            duration = getattr(injury, 'days_missed', 'N/A')
            if duration == 'N/A':
                if from_date != 'N/A' and until_date != 'N/A' and \
                   from_date != 'Unknown' and until_date != 'Unknown':
                    try:
                        from_date_obj = datetime.strptime(from_date, "%d/%m/%Y")
                        until_date_obj = datetime.strptime(until_date, "%d/%m/%Y")
                        duration = (until_date_obj - from_date_obj).days
                    except (ValueError, TypeError):
                        duration = 'N/A'
            
            processed_injuries.append({
                'type': getattr(injury, 'injury', 'N/A'),
                'from_date': from_date,
                'until_date': until_date,
                'days_missed': duration
            })
        
        # Ordena por data de início (mais recente primeiro)
        processed_injuries.sort(
            key=lambda x: datetime.strptime(x['from_date'], "%d/%m/%Y") 
            if x['from_date'] != 'N/A' else datetime.min,
            reverse=True
        )
        
        return processed_injuries
    
    def _process_transfers(self, historical_data: PlayerData) -> List[Dict[str, Any]]:
        """
        Processa o histórico de transferências do jogador.
        
        Args:
            historical_data: Dados históricos do jogador
            
        Returns:
            Lista de transferências processadas
        """
        if not historical_data or not historical_data.transfers:
            return []
        
        processed_transfers = []
        
        for transfer in historical_data.transfers:
            # Formata a data
            date_str = getattr(transfer, 'date', 'N/A')
            if date_str != 'N/A' and not isinstance(date_str, str) and date_str is not None:
                date_str = date_str.strftime("%d/%m/%Y")
            
            # Extrai clubes
            from_club = "N/A"
            if hasattr(transfer, 'club_from'):
                club_from = transfer.club_from
                if isinstance(club_from, dict):
                    from_club = club_from.get('name', 'N/A')
                else:
                    from_club = getattr(club_from, 'name', 'N/A')
            
            to_club = "N/A"
            if hasattr(transfer, 'club_to'):
                club_to = transfer.club_to
                if isinstance(club_to, dict):
                    to_club = club_to.get('name', 'N/A')
                else:
                    to_club = getattr(club_to, 'name', 'N/A')
            
            # Extrai valor
            fee_str = getattr(transfer, 'fee', 'N/A')
            is_loan = isinstance(fee_str, str) and "loan" in fee_str.lower()
            
            processed_transfers.append({
                'date': date_str,
                'from_club': from_club,
                'to_club': to_club,
                'fee': fee_str,
                'is_loan': is_loan
            })
        
        # Ordena por data (mais recente primeiro)
        processed_transfers.sort(
            key=lambda x: datetime.strptime(x['date'], "%d/%m/%Y") 
            if x['date'] != 'N/A' else datetime.min,
            reverse=True
        )
        
        return processed_transfers
    
    def _process_swot_analysis(self, technical_analysis: Any) -> Dict[str, Any]:
        """
        Processa a análise SWOT do jogador.
        
        Args:
            technical_analysis: Análise técnica do jogador
            
        Returns:
            Dicionário com as categorias SWOT processadas
        """
        if not hasattr(technical_analysis, 'swot'):
            return {
                'strengths': [],
                'weaknesses': [],
                'opportunities': [],
                'threats': [],
                'summary': ''
            }
        
        swot = technical_analysis.swot
        
        # Processa cada categoria
        strengths = self._process_swot_strengths(swot)
        weaknesses = self._process_swot_weaknesses(swot)
        opportunities = self._process_swot_opportunities(swot)
        threats = self._process_swot_threats(swot)
        summary = getattr(swot, 'summary', '')
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'opportunities': opportunities,
            'threats': threats,
            'summary': summary
        }
    
    def _process_swot_strengths(self, swot: Any) -> List[Dict[str, Any]]:
        """
        Processa os pontos fortes da análise SWOT.
        
        Args:
            swot: Objeto de análise SWOT
            
        Returns:
            Lista de pontos fortes processados
        """
        strengths = []
        
        for item in getattr(swot, 'strengths', []):
            strength = {
                'text': getattr(item, 'text', getattr(item, 'stat_name', 'N/A')),
                'percentile': getattr(item, 'percentile', None),
                'category': getattr(item, 'category', 'N/A')
            }
            strengths.append(strength)
        
        return strengths
    
    def _process_swot_weaknesses(self, swot: Any) -> List[Dict[str, Any]]:
        """
        Processa os pontos fracos da análise SWOT.
        
        Args:
            swot: Objeto de análise SWOT
            
        Returns:
            Lista de pontos fracos processados
        """
        weaknesses = []
        
        for item in getattr(swot, 'weaknesses', []):
            weakness = {
                'text': getattr(item, 'text', getattr(item, 'stat_name', 'N/A')),
                'percentile': getattr(item, 'percentile', None),
                'category': getattr(item, 'category', 'N/A')
            }
            weaknesses.append(weakness)
        
        return weaknesses
    
    def _process_swot_opportunities(self, swot: Any) -> List[Dict[str, Any]]:
        """
        Processa as oportunidades da análise SWOT.
        
        Args:
            swot: Objeto de análise SWOT
            
        Returns:
            Lista de oportunidades processadas
        """
        opportunities = []
        
        for item in getattr(swot, 'opportunities', []):
            opportunity = {
                'insight': getattr(item, 'insight', 'N/A'),
                'based_on': getattr(item, 'based_on', []),
                'importance': getattr(item, 'importance', 2)
            }
            opportunities.append(opportunity)
        
        return opportunities
    
    def _process_swot_threats(self, swot: Any) -> List[Dict[str, Any]]:
        """
        Processa as ameaças da análise SWOT.
        
        Args:
            swot: Objeto de análise SWOT
            
        Returns:
            Lista de ameaças processadas
        """
        threats = []
        
        for item in getattr(swot, 'threats', []):
            threat = {
                'insight': getattr(item, 'insight', 'N/A'),
                'based_on': getattr(item, 'based_on', []),
                'importance': getattr(item, 'importance', 2)
            }
            threats.append(threat)
        
        return threats
    
    def _process_tactical_fit(self, technical_analysis: Any) -> Dict[str, Any]:
        """
        Processa a adequação tática do jogador.
        
        Args:
            technical_analysis: Análise técnica do jogador
            
        Returns:
            Dicionário com informações de adequação tática
        """
        if not hasattr(technical_analysis, 'tactical_fit'):
            return {
                'player_name': 'N/A',
                'player_id': 'N/A',
                'primary_position': 'N/A',
                'all_positions': [],
                'by_position': {},
                'best_fits': [],
                'optimal_role': {},
                'primary_position_best_fit': 'N/A',
                'versatility': {
                    'position_count': 0,
                    'viable_roles_count': 0
                }
            }
        
        tactical_fit = technical_analysis.tactical_fit
        
        # Processa posições
        by_position = {}
        for pos, analysis in getattr(tactical_fit, 'by_position', {}).items():
            profiles = {}
            for profile_name, details in getattr(analysis, 'profiles', {}).items():
                profiles[profile_name] = {
                    'score': getattr(details, 'score', 0),
                    'description': getattr(details, 'description', 'N/A'),
                    'category': getattr(details, 'category', 'N/A'),
                    'position': getattr(details, 'position', 'N/A'),
                    'position_type': getattr(details, 'position_type', 'N/A')
                }
            
            by_position[pos] = {
                'profiles': profiles,
                'best_fit': getattr(analysis, 'best_fit', 'N/A'),
                'best_score': getattr(analysis, 'best_score', 0),
                'best_description': getattr(analysis, 'best_description', 'N/A'),
                'key_metrics': getattr(analysis, 'key_metrics', [])
            }
        
        # Processa melhores encaixes
        best_fits = []
        for fit in getattr(tactical_fit, 'best_fits', []):
            best_fits.append({
                'position': getattr(fit, 'position', 'N/A'),
                'position_type': getattr(fit, 'position_type', 'N/A'),
                'profile': getattr(fit, 'profile', 'N/A'),
                'score': getattr(fit, 'score', 0),
                'description': getattr(fit, 'description', 'N/A'),
                'category': getattr(fit, 'category', 'N/A')
            })
        
        # Processa função ideal
        optimal_role = {}
        if hasattr(tactical_fit, 'optimal_role'):
            optimal_role = {
                'position': getattr(tactical_fit.optimal_role, 'position', 'N/A'),
                'position_type': getattr(tactical_fit.optimal_role, 'position_type', 'N/A'),
                'profile': getattr(tactical_fit.optimal_role, 'profile', 'N/A'),
                'score': getattr(tactical_fit.optimal_role, 'score', 0),
                'description': getattr(tactical_fit.optimal_role, 'description', 'N/A'),
                'category': getattr(tactical_fit.optimal_role, 'category', 'N/A')
            }
        
        # Processa versatilidade
        versatility = {
            'position_count': 0,
            'viable_roles_count': 0
        }
        if hasattr(tactical_fit, 'versatility'):
            versatility = {
                'position_count': getattr(tactical_fit.versatility, 'position_count', 0),
                'viable_roles_count': getattr(tactical_fit.versatility, 'viable_roles_count', 0)
            }
        
        return {
            'player_name': getattr(tactical_fit, 'player_name', 'N/A'),
            'player_id': getattr(tactical_fit, 'player_id', 'N/A'),
            'primary_position': getattr(tactical_fit, 'primary_position', 'N/A'),
            'all_positions': getattr(tactical_fit, 'all_positions', []),
            'by_position': by_position,
            'best_fits': best_fits,
            'optimal_role': optimal_role,
            'primary_position_best_fit': getattr(tactical_fit, 'primary_position_best_fit', 'N/A'),
            'versatility': versatility
        }
    
    def _process_tactical_styles(self, technical_analysis: Any) -> List[Dict[str, Any]]:
        """
        Processa os estilos táticos compatíveis com o jogador.
        
        Args:
            technical_analysis: Análise técnica do jogador (instance of DataAnalysis)
            
        Returns:
            Lista de estilos táticos com pontuação
        """
        tactical_styles = []
        
        # Log for debugging
        print(f"Processing tactical styles from: {type(technical_analysis).__name__}")
        
        if not hasattr(technical_analysis, 'tactical_styles'):
            print("technical_analysis does not have tactical_styles attribute")
            return []
        
        # Access the tactical_styles dictionary
        ts = technical_analysis.tactical_styles
        
        # Check if tactical_styles has the expected structure
        if isinstance(ts, dict) and 'best_fits' in ts:
            # Process the best_fits list
            best_fits = ts.get('best_fits', [])
            print(f"Found best_fits with {len(best_fits)} items")
            
            for style in best_fits:
                # Extract the necessary fields
                style_name = style.get('style_name', 'N/A')
                style_score = style.get('style_score', 0)
                style_description = style.get('style_description', '')
                
                # Create a standardized style entry
                tactical_styles.append({
                    'style': style_name,
                    'score': style_score,
                    'description': style_description
                })
        else:
            # Alternative structure - try to extract directly from the tactical_styles dict
            print(f"tactical_styles does not have 'best_fits'; keys: {ts.keys() if isinstance(ts, dict) else 'N/A'}")
            
            # If tactical_styles is itself a mapping of style names to scores
            if isinstance(ts, dict):
                for style_key, style_data in ts.items():
                    # Skip non-style entries
                    if style_key in ('best_fits', 'compatible_styles'):
                        continue
                    
                    # Handle different possible value types
                    if isinstance(style_data, dict):
                        # If it's a dict, extract score and description
                        score = style_data.get('style_score', 
                                style_data.get('score', 
                                style_data.get('normalized_style_score', 0)))
                        
                        description = style_data.get('style_description', 
                                    style_data.get('description', ''))
                        
                        # Use the style name from the data if available, otherwise use the key
                        style_name = style_data.get('style_name', style_key)
                    
                    elif isinstance(style_data, (int, float)):
                        # If it's just a number, assume it's the score
                        score = style_data
                        style_name = style_key
                        description = ''
                    else:
                        # Skip if we can't interpret the data
                        continue
                    
                    tactical_styles.append({
                        'style': style_name,
                        'score': score,
                        'description': description
                    })
        
        # Sort by score in descending order
        tactical_styles.sort(key=lambda x: x['score'], reverse=True)
        
        # Take top 5 for display
        tactical_styles = tactical_styles[:5]
        
        print(f"Processed {len(tactical_styles)} tactical styles")
        return tactical_styles
        
    def _process_percentiles(self, technical_analysis: Any) -> Dict[str, Any]:
            """
            Processa os percentis do jogador, incluindo tanto a estrutura antiga quanto a nova.
            
            Args:
                technical_analysis: Análise técnica do jogador
                
            Returns:
                Dicionário com percentis em ambos os formatos (original e por categoria funcional)
            """
            result = {}
            
            # Processamento da estrutura antiga (original)
            if hasattr(technical_analysis, 'percentiles') and technical_analysis.percentiles:
                result['percentiles'] = technical_analysis.percentiles
            
            # Processamento da estrutura nova (por categoria funcional)
            if hasattr(technical_analysis, 'percentiles_by_category') and technical_analysis.percentiles_by_category:
                result['percentiles_by_category'] = technical_analysis.percentiles_by_category
            
            # Incluir também o grupo de posição, se disponível
            if hasattr(technical_analysis, 'position_group'):
                result['position_group'] = technical_analysis.position_group
            
            return result
    def _process_ranking(self, technical_analysis: Any) -> List[Dict[str, Any]]:
        
        """
        Processa o ranking do jogador em diferentes categorias,
        suportando tanto o formato antigo quanto o novo.
        
        Args:
            technical_analysis: Análise técnica do jogador
            
        Returns:
            Lista com informações de ranking processadas
        """
        if not hasattr(technical_analysis, 'ranking'):
            return []
        
        ranking = []
        
        # Verificar se temos o formato novo (lista de dicionários mapeando posições para RankingItems)
        if isinstance(technical_analysis.ranking, list) and all(isinstance(item, dict) for item in technical_analysis.ranking):
            for rank_dict in technical_analysis.ranking:
                # Iterar por cada posição no dicionário
                for position, item in rank_dict.items():
                    # Extrair informações básicas do ranking
                    rank_info = {
                        'position': position,
                        'key_metrics': [],
                        'metrics_percentiles': {}
                    }
                    
                    # Obter rank e métricas-chave
                    if hasattr(item, 'rank'):
                        # Acesso direto para objetos RankingItem
                        rank_info['rank'] = item.rank
                        rank_info['key_metrics'] = getattr(item, 'key_metrics', [])
                        
                        # Obter métricas com percentis (nova estrutura)
                        if hasattr(item, 'metrics_percentiles'):
                            rank_info['metrics_percentiles'] = item.metrics_percentiles
                    elif isinstance(item, dict):
                        # Acesso via dicionário
                        rank_info['rank'] = item.get('rank', 0)
                        rank_info['key_metrics'] = item.get('key_metrics', [])
                        rank_info['metrics_percentiles'] = item.get('metrics_percentiles', {})
                    
                    # Adicionar métricas formatadas para exibição
                    rank_info['display_metrics'] = [
                        {
                            'name': metric,
                            'display_name': self._format_metric_name(metric),
                            'percentile': rank_info['metrics_percentiles'].get(metric, 0)
                        }
                        for metric in rank_info['key_metrics']
                    ]
                    
                    ranking.append(rank_info)
        else:
            # Fallback para formato antigo se necessário
            for rank_item in technical_analysis.ranking:
                if hasattr(rank_item, 'category'):
                    # Usar acesso de atributos para objetos modelo
                    ranking.append({
                        'category': rank_item.category,
                        'position': rank_item.position,
                        'total': rank_item.total,
                        'percentile': rank_item.percentile
                    })
                elif isinstance(rank_item, dict):
                    # Usar acesso de dicionário para dicts
                    ranking.append({
                        'category': rank_item.get('category', 'N/A'),
                        'position': rank_item.get('position', 0),
                        'total': rank_item.get('total', 0),
                        'percentile': rank_item.get('percentile', 0)
                    })
        
        return ranking    
    def _find_percentile_for_metric(self, technical_analysis: Any, metric: str, category: str = None) -> float:
        """
        Busca o valor do percentil para uma métrica específica, usando a estrutura nova ou antiga.
        
        Args:
            technical_analysis: Análise técnica do jogador
            metric: Nome da métrica
            category: Categoria opcional para busca específica (ex: "attacking", "defensive")
            
        Returns:
            Valor do percentil (0-100) ou 0 se não encontrado
        """
        # Verificar se a análise tem percentis
        if not hasattr(technical_analysis, 'percentiles') and not hasattr(technical_analysis, 'percentiles_by_category'):
            return 0
        
        # 1. Buscar na categoria específica da estrutura nova, se fornecida
        if hasattr(technical_analysis, 'percentiles_by_category') and category:
            categories = technical_analysis.percentiles_by_category
            if category in categories and metric in categories[category]:
                return categories[category][metric]
        
        # 2. Buscar em todas as categorias da estrutura nova
        if hasattr(technical_analysis, 'percentiles_by_category'):
            categories = technical_analysis.percentiles_by_category
            for cat, metrics in categories.items():
                if metric in metrics:
                    return metrics[metric]
        
        # 3. Buscar na estrutura antiga (para compatibilidade)
        if hasattr(technical_analysis, 'percentiles'):
            percentiles = technical_analysis.percentiles
            for category, metrics in percentiles.items():
                if metric in metrics:
                    return metrics[metric]
        
        # 4. Busca aproximada por nome similar (para lidar com variações como blocks/shotsBlocked)
        if hasattr(technical_analysis, 'percentiles'):
            percentiles = technical_analysis.percentiles
            metric_lower = metric.lower()
            for category, metrics in percentiles.items():
                for key in metrics.keys():
                    if metric_lower in key.lower() or key.lower() in metric_lower:
                        return metrics[key]
        
        # Não encontrado após todas as tentativas
        return 0


    def _process_radar_data(self, technical_analysis: Any) -> Dict[str, Any]:
        """
        Processa os dados para gráficos de radar usando a estrutura nova ou antiga de percentis.
        """
        radar_data = {
            'metrics': {},
            'tactical_profiles': {}
        }
        
        # Processa métricas para gráfico de radar
        if hasattr(technical_analysis, 'ranking'):
            # Check if we have the new format (list of dicts mapping positions to RankingItems)
            if isinstance(technical_analysis.ranking, list) and all(isinstance(item, dict) for item in technical_analysis.ranking):
                for rank_dict in technical_analysis.ranking:
                    # Iterate through each position in the dictionary
                    for position, item in rank_dict.items():
                        # Extract key_metrics - use attribute access for RankingItem objects
                        key_metrics = []
                        metrics_percentiles = {}
                        
                        # Tentar acessar metrics_percentiles primeiro (nova implementação)
                        if hasattr(item, 'metrics_percentiles'):
                            metrics_percentiles = item.metrics_percentiles
                        elif isinstance(item, dict) and 'metrics_percentiles' in item:
                            metrics_percentiles = item['metrics_percentiles']
                        
                        # Obter key_metrics
                        if hasattr(item, 'key_metrics'):
                            key_metrics = item.key_metrics
                        elif isinstance(item, dict) and 'key_metrics' in item:
                            key_metrics = item['key_metrics']
                        
                        if key_metrics:
                            metrics_values = {}
                            
                            # Primeiro tentar usar metrics_percentiles se disponível
                            if metrics_percentiles:
                                for metric in key_metrics:
                                    # Usar valor pré-calculado se disponível
                                    metrics_values[metric] = metrics_percentiles.get(metric, 0)
                            else:
                                # Caso contrário, buscar o valor via _find_percentile_for_metric
                                for metric in key_metrics:
                                    # Determinar a categoria com base na posição
                                    category = self._get_category_for_position(position)
                                    value = self._find_percentile_for_metric(technical_analysis, metric, category)
                                    metrics_values[metric] = value
                            
                            # Formatar para exibição no radar
                            radar_data['metrics'][position] = {
                                'labels': key_metrics,
                                'values': [metrics_values.get(metric, 0) for metric in key_metrics],
                                'display_labels': [self._format_metric_name(metric) for metric in key_metrics]
                            }
        
        if hasattr(technical_analysis, 'tactical_fit'):
                tactical_fit = technical_analysis.tactical_fit
                profiles_data = {}
                
                for pos, analysis in getattr(tactical_fit, 'by_position', {}).items():
                    profiles = getattr(analysis, 'profiles', {})
                    if profiles:
                        labels = list(profiles.keys())
                        # Handle both Pydantic models and dicts for profile values
                        values = []
                        for profile in labels:
                            profile_data = profiles[profile]
                            if hasattr(profile_data, 'score'):
                                # For Pydantic models, use attribute access
                                values.append(profile_data.score)
                            elif isinstance(profile_data, dict):
                                # For dictionaries, use dictionary access
                                values.append(profile_data.get('score', 0))
                            else:
                                # Default value if we can't determine
                                values.append(0)
                        
                        profiles_data[pos] = {
                            'labels': labels,
                            'values': values
                        }
                
                radar_data['tactical_profiles'] = profiles_data
        
        

        return radar_data


    def _get_category_for_position(self, position: str) -> str:
        """
        Determina a categoria principal para uma posição.
        Útil para direcionar a busca por métricas em categorias específicas.
        
        Args:
            position: Código da posição (ex: "cb", "cf", "gk")
            
        Returns:
            Categoria principal para a posição (ex: "defensive", "attacking", "goalkeeping")
        """
        # Mapeamento básico de posições para categorias principais
        position = position.lower()
        
        if position in ["gk"]:
            return "goalkeeping"
        elif position in ["cb", "lcb", "rcb", "lb", "rb", "lwb", "rwb"]:
            return "defensive"
        elif position in ["dmf", "cmf", "lcmf", "rcmf"]:
            return "passing"
        elif position in ["amf", "lamf", "ramf"]:
            return "possession" 
        elif position in ["cf", "lw", "rw", "lwf", "rwf"]:
            return "attacking"
        
        return None  # Retorna None se não encontrar uma categoria específica


    def _format_metric_name(self, metric_name: str) -> str:
        """
        Formata o nome de uma métrica para exibição no gráfico.
        
        Args:
            metric_name: Nome da métrica em camelCase ou snake_case
            
        Returns:
            Nome formatado para exibição
        """
        # Converter camelCase para espaços entre palavras
        import re
        formatted = re.sub(r'([a-z])([A-Z])', r'\1 \2', metric_name)
        
        # Converter snake_case
        formatted = formatted.replace('_', ' ')
        
        # Capitalizar primeira letra de cada palavra
        return ' '.join(word.capitalize() for word in formatted.split())
        
      
    def _generate_ai_content(self, player_id: str, technical_analysis: Any, 
                       historical_data: PlayerData) -> Dict[str, Any]:
        """
        Gera conteúdo textual usando IA para o relatório.
        """
        try:
            # Gera o resumo executivo
            executive_summary = self.ai_content_generator.generate_executive_summary(
                player_id, technical_analysis
            )
            
            # Gera a análise tática
            tactical_analysis_raw = self.ai_content_generator.generate_tactical_analysis(
                player_id, technical_analysis
            )
            
            # Gera a recomendação de recrutamento
            recruitment_recommendation_raw = self.ai_content_generator.generate_recruitment_recommendation(
                player_id, technical_analysis, historical_data
            )
            
            # Print the raw outputs for debugging
            print(f"Tactical analysis type: {type(tactical_analysis_raw)}")
            print(f"Recruitment recommendation type: {type(recruitment_recommendation_raw)}")
            
            from models.analysis import RecruitmentDecisionMatrix, AIAnalysis
        
            if isinstance(tactical_analysis_raw, dict):
                print("Using generated tactical analysis")
                tactical_analysis_structured = tactical_analysis_raw
            if isinstance(recruitment_recommendation_raw, dict):
                print("Using generated recruitment recommendation")
                recruitment_recommendation_structured = recruitment_recommendation_raw
            
            # Return the content for the template
            return {
                'executive_summary': executive_summary,
                'tactical_analysis': tactical_analysis_structured,
                'recruitment_recommendation': recruitment_recommendation_structured
            }
        except Exception as e:
            print(f"Error in _generate_ai_content: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'executive_summary': f"Erro ao gerar resumo executivo: {str(e)}",
                'tactical_analysis': {},
                'recruitment_recommendation': {}
            }

    def _get_translations_for_template(self) -> Dict[str, str]:
        """
        Obtém todas as traduções necessárias para o template.
        
        Returns:
            Dicionário com todas as traduções no idioma atual
        """
        translations = {}
        
        # Adiciona todas as chaves de tradução ao dicionário
        for key in TranslationManager.TRANSLATIONS:
            translations[key] = self.translate(key)
        
        return translations


def generate_scout_report(player_id: str, language: str = 'pt') -> Dict[str, Any]:
    """
    Função principal para gerar um relatório de scout completo.
    
    Args:
        player_id: ID do jogador
        language: Código do idioma (pt, en, bg, es)
        
    Returns:
        Dicionário com todos os dados processados para o template
    """
    from services.data_service import find_player_by_id
    
    # Obtém os dados do jogador
    player_data = find_player_by_id(player_id)
    if not player_data:
        raise ValueError(f"Jogador com ID {player_id} não encontrado.")
    
    # Obtém o nome do jogador para buscar dados históricos
    player_name = player_data.get('name', '')
    if not player_name:
        raise ValueError(f"Nome do jogador não encontrado para ID {player_id}.")
    
    # Obtém dados históricos do Transfermarkt
    from core.transfermarkt import get_player_data
    historical_data = get_player_data(player_name)
    
    # Realiza análise técnica
    from core.data_analysis import complete_data_analysis
    technical_analysis = complete_data_analysis(player_id, language=language)
    
    # Processa os dados para o template
    processor = ScoutReportProcessor(language)
    template_data = processor.process_player_data(
        player_id, player_data, historical_data, technical_analysis
    )
    
    return template_data
