from services.data_service import find_player_by_id

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from services.claude_api import call_claude_api
from services.claude_api import get_anthropic_api_key

from services.format_metrics import TacticalAnalysisDataExtractor
from models.analysis import *
from core.transfermarkt import *
from core.data_analysis import *

class ScoutingReportAI:
    """Geração de conteúdo textual para relatórios de scouting usando IA"""
    
    def __init__(self,language):
        """Inicializar com as configurações do modelo"""
        # Parâmetros padrão para chamadas de IA
        self.default_model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 1500
        self.language = "pt"
        self.anthropic_api_key = get_anthropic_api_key()
    
    def generate_executive_summary(self, player_id, technical_analysis: DataAnalysis):
        """Gerar resumo executivo do jogador"""
        # Extrair dados relevantes para o prompt
        language = self.language
        swot = technical_analysis.swot
        tactical_fit = technical_analysis.tactical_fit
        player_info = find_player_by_id(player_id)
        if player_info is None:
            raise ValueError("Player data not found.")
        
        # Extract position names from position dictionaries
        position_list = player_info.get('positions', [])
        position_names = self._extract_position_names(position_list)

        executive_summary_prompts = {
    "en": f"""
        Executive Summary for scouting report of:
        
        Name: {player_info.get('name', 'Not available')}
        Position: {', '.join(position_names)}
        Age: {player_info.get('age', 'Not available')}
        Dominant foot: {player_info.get('foot', 'Not available')}

        Strengths (based on percentiles):
        {self._format_swot_strengths(swot)}
        
        Weaknesses (based on percentiles):
        {self._format_swot_weaknesses(swot)}
        
        Best tactical fit:
        {self._format_tactical_fit(tactical_fit)}
        
        Generate a concise and technical executive summary, highlighting the player's profile,
        tactical compatibility, strengths and development areas.
        """,
    
    "pt": f"""
        Resumo Executivo para relatório de scouting de:
        
        Nome: {player_info.get('name', 'Não disponível')}
        Posição: {', '.join(position_names)}
        Idade: {player_info.get('age', 'Não disponível')}
        Pé dominante: {player_info.get('foot', 'Não disponível')}

        Pontos fortes (baseados em percentis):
        {self._format_swot_strengths(swot)}
        
        Pontos fracos (baseados em percentis):
        {self._format_swot_weaknesses(swot)}
        
        Melhor encaixe tático:
        {self._format_tactical_fit(tactical_fit)}
        
        Gere um resumo executivo conciso e técnico, destacando o perfil do jogador,
        compatibilidade tática, pontos fortes e áreas de desenvolvimento.
        """,
    
    "es": f"""
        Resumen Ejecutivo para informe de scouting de:
        
        Nombre: {player_info.get('name', 'No disponible')}
        Posición: {', '.join(position_names)}
        Edad: {player_info.get('age', 'No disponible')}
        Pie dominante: {player_info.get('foot', 'No disponible')}

        Fortalezas (basadas en percentiles):
        {self._format_swot_strengths(swot)}
        
        Debilidades (basadas en percentiles):
        {self._format_swot_weaknesses(swot)}
        
        Mejor ajuste táctico:
        {self._format_tactical_fit(tactical_fit)}
        
        Genera un resumen ejecutivo conciso y técnico, destacando el perfil del jugador,
        compatibilidad táctica, puntos fuertes y áreas de desarrollo.
        """,
    
    "bg": f"""
        Резюме на скаутски доклад за:
        
        Име: {player_info.get('name', 'Не е налично')}
        Позиция: {', '.join(position_names)}
        Възраст: {player_info.get('age', 'Не е налична')}
        Доминиращ крак: {player_info.get('foot', 'Не е наличен')}

        Силни страни (базирани на перцентили):
        {self._format_swot_strengths(swot)}
        
        Слаби страни (базирани на перцентили):
        {self._format_swot_weaknesses(swot)}
        
        Най-добро тактическо съответствие:
        {self._format_tactical_fit(tactical_fit)}
        
        Генерирайте кратко и техническо резюме, подчертаващо профила на играча,
        тактическата съвместимост, силните страни и областите за развитие.
        """
}
        # Construir prompt para IA
        system_prompt = """
        Você é um analista de scouting de futebol profissional com 20 anos de experiência.
        Crie um resumo executivo conciso (3-4 frases) que capture a essência do jogador,
        destacando sua principal função tática, pontos fortes, áreas de desenvolvimento
        e potencial de carreira. Use linguagem técnica apropriada para scouts de futebol. 
        <IMPORTANTE>Não faça menções a valores ou menções a métricas. Isso será abordado por outras sessões do relatório</IMPORTANTE> 
        """
        
        prompt = executive_summary_prompts.get(language, executive_summary_prompts["pt"])

        
        # Chamar IA e retornar resposta
        return self._call_ai(system_prompt, prompt)

    
    def generate_tactical_analysis(self, player_id, technical_analysis):
        language = self.language
        from models.analysis import AIAnalysis
        """Gerar prompt para análise tática"""
        # Extrair informações básicas do jogador
        player_info = find_player_by_id(player_id)

        # Get both tactical role and tactical styles
        tactical_role_data = technical_analysis.tactical_fit  # Using backward compatibility name
        tactical_styles = technical_analysis.tactical_styles
        
        # Inicializar o extrator e obter métricas formatadas
        extractor = TacticalAnalysisDataExtractor()
        metrics = extractor.extract_player_metrics(player_info)
        formatted_metrics = extractor.format_for_prompt(metrics)
        
        # Posição principal e sistemas compatíveis
        positions = player_info.get('positions', [])
        main_position = "Unknown"
        if positions:
            if isinstance(positions[0], dict):
                if "position" in positions[0] and isinstance(positions[0]["position"], dict):
                    main_position = positions[0]["position"].get("code", "Unknown")
                else:
                    main_position = positions[0].get("name", "Unknown")
        
        # Construir o prompt completo
        system_prompt = """
        Você é um analista tático de futebol especializado em identificar padrões de jogo.
        Analise as estatísticas do jogador para descrever seus padrões ofensivos e defensivos,
        contribuição tática e como ele se encaixa em diferentes sistemas.
        Use linguagem técnica apropriada para scouts profissionais e cite estatísticas específicas.
        """
        tactical_analysis_prompts = {
    "en": f"""
        ## Player Tactical Analysis
        
        PLAYER: {player_info.get('name', 'Not available')}
        MAIN POSITION: {main_position}
        DOMINANT FOOT: {player_info.get('foot', 'Not available')}
        AGE: {player_info.get('age', 'Not available')}
        MATCHES ANALYZED: {player_info.get('total', {}).get('matches', 0)}
        
        ## DETAILED METRICS
        {formatted_metrics}
        
        ## PLAYER TACTICAL ROLES
        {self._format_tactical_fit(tactical_role_data)}
        
        ## COMPATIBLE PLAYING STYLES
        {self._format_tactical_styles(tactical_styles)}
        
        Based on these detailed statistics:
        
        1. ATTACKING PATTERNS: Describe how the player acts offensively, their movement patterns, preferred areas of action and how they create or finish plays. Cite specific metrics that support your analysis.
        
        2. DEFENSIVE CONTRIBUTION: Analyze how the player contributes defensively, considering their main position. Comment on work rate, counter-pressing, and participation in defensive duels. Cite specific metrics.
        
        3. PHYSICAL AND TECHNICAL PROFILE: Evaluate the player's physical profile (duels, accelerations, runs) and technical skills (passing, dribbling, finishing), explaining how this translates into their playing style.
        
        4. TACTICAL FLEXIBILITY: Indicate the tactical systems in which the player would perform best and why. Identify systems that would be less suitable.
        
        5. CONTEXTUAL RECOMMENDATIONS: Explain how a team should be structured around this player to maximize their strengths and minimize their weaknesses.
        
        Use appropriate technical language for professional scouts, but maintain clarity.
        Mention specific statistics to support each point of the analysis.
        Your text should be concise and data-driven, avoiding generalities.
        """,
    
    "pt": f"""
        ## Análise Tática do Jogador
        
        JOGADOR: {player_info.get('name', 'Não disponível')}
        POSIÇÃO PRINCIPAL: {main_position}
        PÉ DOMINANTE: {player_info.get('foot', 'Não disponível')}
        IDADE: {player_info.get('age', 'Não disponível')}
        PARTIDAS ANALISADAS: {player_info.get('total', {}).get('matches', 0)}
        
        ## MÉTRICAS DETALHADAS
        {formatted_metrics}
        
        ## FUNÇÕES TÁTICAS DO JOGADOR
        {self._format_tactical_fit(tactical_role_data)}
        
        ## ESTILOS DE JOGO COMPATÍVEIS
        {self._format_tactical_styles(tactical_styles)}
        
        Com base nessas estatísticas detalhadas:
        
        1. PADRÕES DE ATAQUE: Descreva como o jogador atua ofensivamente, seus padrões de movimento, áreas de atuação preferidas e como ele cria ou finaliza jogadas. Cite métricas específicas que comprovem suas análises.
        
        2. CONTRIBUIÇÃO DEFENSIVA: Analise como o jogador contribui defensivamente, considerando sua posição principal. Comente sobre taxa de trabalho, contrapressão, e participação em duelos defensivos. Cite métricas específicas.
        
        3. PERFIL FÍSICO E TÉCNICO: Avalie o perfil físico do jogador (duelos, acelerações, corridas) e suas habilidades técnicas (passe, drible, finalização), explicando como isso se traduz em seu estilo de jogo.
        
        4. FLEXIBILIDADE TÁTICA: Indique os sistemas táticos em que o jogador teria melhor desempenho e por quê. Identifique sistemas que seriam menos adequados.
        
        5. RECOMENDAÇÕES CONTEXTUAIS: Explique como uma equipe deve ser estruturada ao redor deste jogador para maximizar suas forças e minimizar suas fraquezas.
        
        Use linguagem técnica apropriada para scouts profissionais, mas mantenha a clareza. 
        Mencione estatísticas específicas para fundamentar cada ponto da análise.
        Seu texto deve ser conciso e orientado por dados, evitando generalidades.
        """,
    
    "es": f"""
        ## Análisis Táctico del Jugador
        
        JUGADOR: {player_info.get('name', 'No disponible')}
        POSICIÓN PRINCIPAL: {main_position}
        PIE DOMINANTE: {player_info.get('foot', 'No disponible')}
        EDAD: {player_info.get('age', 'No disponible')}
        PARTIDOS ANALIZADOS: {player_info.get('total', {}).get('matches', 0)}
        
        ## MÉTRICAS DETALLADAS
        {formatted_metrics}
        
        ## ROLES TÁCTICOS DEL JUGADOR
        {self._format_tactical_fit(tactical_role_data)}
        
        ## ESTILOS DE JUEGO COMPATIBLES
        {self._format_tactical_styles(tactical_styles)}
        
        En base a estas estadísticas detalladas:
        
        1. PATRONES DE ATAQUE: Describe cómo actúa el jugador ofensivamente, sus patrones de movimiento, áreas preferidas de acción y cómo crea o finaliza jugadas. Cita métricas específicas que respalden tus análisis.
        
        2. CONTRIBUCIÓN DEFENSIVA: Analiza cómo contribuye el jugador defensivamente, considerando su posición principal. Comenta sobre su ritmo de trabajo, contrapresión y participación en duelos defensivos. Cita métricas específicas.
        
        3. PERFIL FÍSICO Y TÉCNICO: Evalúa el perfil físico del jugador (duelos, aceleraciones, carreras) y sus habilidades técnicas (pase, regate, finalización), explicando cómo esto se traduce en su estilo de juego.
        
        4. FLEXIBILIDAD TÁCTICA: Indica los sistemas tácticos en los que el jugador tendría mejor rendimiento y por qué. Identifica sistemas que serían menos adecuados.
        
        5. RECOMENDACIONES CONTEXTUALES: Explica cómo debería estructurarse un equipo alrededor de este jugador para maximizar sus fortalezas y minimizar sus debilidades.
        
        Utiliza lenguaje técnico apropiado para scouts profesionales, pero mantén la claridad.
        Menciona estadísticas específicas para fundamentar cada punto del análisis.
        Tu texto debe ser conciso y orientado a datos, evitando generalidades.
        """,
    
    "bg": f"""
        ## Тактически Анализ на Играча
        
        ИГРАЧ: {player_info.get('name', 'Не е налично')}
        ОСНОВНА ПОЗИЦИЯ: {main_position}
        ДОМИНИРАЩ КРАК: {player_info.get('foot', 'Не е наличен')}
        ВЪЗРАСТ: {player_info.get('age', 'Не е налична')}
        АНАЛИЗИРАНИ МАЧОВЕ: {player_info.get('total', {}).get('matches', 0)}
        
        ## ДЕТАЙЛНИ МЕТРИКИ
        {formatted_metrics}
        
        ## ТАКТИЧЕСКИ РОЛИ НА ИГРАЧА
        {self._format_tactical_fit(tactical_role_data)}
        
        ## СЪВМЕСТИМИ СТИЛОВЕ НА ИГРА
        {self._format_tactical_styles(tactical_styles)}
        
        Въз основа на тези подробни статистики:
        
        1. МОДЕЛИ НА АТАКА: Опишете как играчът действа офанзивно, моделите му на движение, предпочитаните зони на действие и как създава или завършва игри. Цитирайте конкретни метрики, които подкрепят анализа ви.
        
        2. ЗАЩИТЕН ПРИНОС: Анализирайте как играчът допринася в защита, имайки предвид основната му позиция. Коментирайте работния темп, контрапресата и участието в защитни дуели. Цитирайте конкретни метрики.
        
        3. ФИЗИЧЕСКИ И ТЕХНИЧЕСКИ ПРОФИЛ: Оценете физическия профил на играча (дуели, ускорения, бягания) и техническите му умения (пасове, дрибъл, завършване), обяснявайки как това се отразява в стила му на игра.
        
        4. ТАКТИЧЕСКА ГЪВКАВОСТ: Посочете тактическите системи, в които играчът би се представил най-добре и защо. Идентифицирайте системи, които биха били по-малко подходящи.
        
        5. КОНТЕКСТУАЛНИ ПРЕПОРЪКИ: Обяснете как трябва да бъде структуриран отборът около този играч, за да се максимизират силните му страни и минимизират слабостите му.
        
        Използвайте подходящ технически език за професионални скаути, но запазете яснотата.
        Споменете конкретни статистики, за да подкрепите всяка точка от анализа.
        Текстът ви трябва да бъде кратък и основан на данни, избягвайки общи фрази.
        """
}
        prompt = tactical_analysis_prompts.get(self.language, tactical_analysis_prompts["pt"])
    # Rest of the function remains the same...
        tools = [{
    "name": "tactical_analysis_tool",
    "description": "Generate comprehensive tactical analysis for a football player based on statistics and metrics",
    "input_schema": AIAnalysis.model_json_schema()
        }]


        response= self._call_ai_with_tool(system_prompt, prompt, tools)

        tool_input = response.content[0].input
        if isinstance(tool_input, str):
            try:
                # Attempt to parse the string as JSON
                import json
                parsed_input = json.loads(tool_input)
                args = parsed_input
            except json.JSONDecodeError as e:
                print(f"ERROR - Failed to parse tool_input as JSON: {e}")
                raise ValueError(f"Claude API returned an invalid response format: {tool_input}")
        else:
            # It's already a dict
            args = tool_input
        tactical_analysis = args
        return tactical_analysis

    def _call_ai_with_tool(self, system_prompt, user_prompt, tools):
        """Chamar API de IA com os prompts fornecidos e ferramenta"""
        try:
            tool_name = tools[0]['name'] if tools else "Unknown"
            timeout = 90.0 if tool_name == 'tactical_analysis_tool' or tool_name == 'recruitment_recommendation_tool' else 30.0

            response = call_claude_api(
                api_key=self.anthropic_api_key,
                model=self.default_model,
                max_tokens=self.max_tokens,
                timeout=timeout,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                tools=tools,
                tool_choice={"type": "tool", "name": tools[0]['name']}
            )
            
            return response
        
        except Exception as e:
            print(f"Erro ao chamar API de IA: {str(e)}")
            return f"Erro na geração de conteúdo: {str(e)}"

    def _format_tactical_fit(self, tactical_fit):
        """Formatar informações de adequação tática para o prompt"""
        from models.analysis import TacticalFitAnalysis, TacticalProfileFit
        if isinstance(tactical_fit, TacticalFitAnalysis):
            best_fits = tactical_fit.best_fits          
            if not best_fits:
                return "Dados não disponíveis"
                
            formatted_text = "Compatibilidade com sistemas táticos:\n"
            for i in range(3):
                formatted_text += f"{i+1}. {best_fits[i].profile} ({best_fits[i].score}% de compatibilidade)\n"
        
            return formatted_text
        else:
            return "Dados não disponíveis"
    
    def generate_recruitment_recommendation(self, player_id, technical_analysis, historical_data: PlayerData):
        from models.analysis import RecruitmentDecisionMatrix
        """Generate recruitment recommendation with detailed acquisition evaluation"""
        # Extract player information
        player_info = find_player_by_id(player_id)
        if player_info is None:
            raise ValueError("Player data not found.")
        # Extract positions safely
        position_list = player_info.get('positions', [])
        position_names = self._extract_position_names(position_list)
        
        # Get market value data
        market_value = "Não disponível"
        contract_until = player_info['contract'].get('contractExpiration', 'Não disponível')
        if historical_data and historical_data.market_value_history:
            market_values = historical_data.market_value_history
            if market_values and len(market_values) > 0:
                latest = market_values[-1]
                if latest.market_value:
                    market_value = latest.market_value


        # Get tactical fit data
        tactical_fit = technical_analysis.tactical_fit
        swot = technical_analysis.swot
        
        # Create system prompt
        system_prompt = """
        Você é um diretor de recrutamento de um clube de futebol de elite.
        Analise o perfil completo de um jogador e forneça uma recomendação 
        estratégica detalhada sobre sua contratação, avaliando viabilidade, 
        encaixe técnico-tático, perfil de desenvolvimento, e estratégia de aquisição.
        """
        recruitment_prompts = {
    "en": f"""
        # Recruitment Recommendation
        
        ## Player Data
        
        NAME: {player_info.get('name', 'Not available')}
        AGE: {player_info.get('age', 'Not available')}
        POSITION: {', '.join(position_names)}
        CONTRACT UNTIL: {contract_until}
        MARKET VALUE: {market_value}
        
        ## Technical-Tactical Fit
        {self._format_tactical_fit(tactical_fit)}
        
        ## Strengths
        {self._format_swot_strengths(swot)}
        
        ## Weaknesses
        {self._format_swot_weaknesses(swot)}
        
        ## Identified Opportunities
        {self._format_swot_opportunities(swot)}
        
        Based on the data above, provide a complete recruitment assessment including:
        
        1. Evaluate acquisition feasibility (scale 1-10) considering market value and contractual situation
        2. Evaluate technical-tactical fit (scale 1-10) considering player profile
        3. Evaluate age/development profile (scale 1-10) considering potential
        4. Provide a final recommendation (Monitor, Acquire, Prioritize, Avoid)
        5. Suggest an acquisition strategy and integration plan if contracted
        
        Be specific and strategic in your analysis, considering risk factors and potential return.
        """,
    
    "pt": f"""
        # Recomendação de Recrutamento
        
        ## Dados do Jogador
        
        NOME: {player_info.get('name', 'Não disponível')}
        IDADE: {player_info.get('age', 'Não disponível')}
        POSIÇÃO: {', '.join(position_names)}
        CONTRATO ATÉ: {contract_until}
        VALOR DE MERCADO: {market_value}
        
        ## Encaixe Técnico-Tático
        {self._format_tactical_fit(tactical_fit)}
        
        ## Pontos Fortes 
        {self._format_swot_strengths(swot)}
        
        ## Pontos Fracos
        {self._format_swot_weaknesses(swot)}
        
        ## Oportunidades Identificadas
        {self._format_swot_opportunities(swot)}
        
        Baseado nos dados acima, forneça uma avaliação completa de recrutamento que inclua:
        
        1. Avalie a viabilidade de aquisição (escala 1-10) considerando valor de mercado e situação contratual
        2. Avalie o encaixe técnico-tático (escala 1-10) considerando perfil do jogador
        3. Avalie o perfil de idade/desenvolvimento (escala 1-10) considerando potencial
        4. Forneça uma recomendação final (Monitorar, Adquirir, Priorizar, Evitar)
        5. Sugira uma estratégia de aquisição e um plano de integração caso seja contratado
        
        Seja específico e estratégico em sua análise, considerando fatores de risco e retorno potencial.
        """,
    
    "es": f"""
        # Recomendación de Reclutamiento
        
        ## Datos del Jugador
        
        NOMBRE: {player_info.get('name', 'No disponible')}
        EDAD: {player_info.get('age', 'No disponible')}
        POSICIÓN: {', '.join(position_names)}
        CONTRATO HASTA: {contract_until}
        VALOR DE MERCADO: {market_value}
        
        ## Encaje Técnico-Táctico
        {self._format_tactical_fit(tactical_fit)}
        
        ## Fortalezas
        {self._format_swot_strengths(swot)}
        
        ## Debilidades
        {self._format_swot_weaknesses(swot)}
        
        ## Oportunidades Identificadas
        {self._format_swot_opportunities(swot)}
        
        Basado en los datos anteriores, proporcione una evaluación completa de reclutamiento que incluya:
        
        1. Evalúe la viabilidad de adquisición (escala 1-10) considerando el valor de mercado y la situación contractual
        2. Evalúe el encaje técnico-táctico (escala 1-10) considerando el perfil del jugador
        3. Evalúe el perfil de edad/desarrollo (escala 1-10) considerando el potencial
        4. Proporcione una recomendación final (Monitorizar, Adquirir, Priorizar, Evitar)
        5. Sugiera una estrategia de adquisición y un plan de integración en caso de ser contratado
        
        Sea específico y estratégico en su análisis, considerando factores de riesgo y retorno potencial.
        """,
    
    "bg": f"""
        # Препоръка за Рекрутиране
        
        ## Данни за Играча
        
        ИМЕ: {player_info.get('name', 'Не е налично')}
        ВЪЗРАСТ: {player_info.get('age', 'Не е налична')}
        ПОЗИЦИЯ: {', '.join(position_names)}
        ДОГОВОР ДО: {contract_until}
        ПАЗАРНА СТОЙНОСТ: {market_value}
        
        ## Техническо-Тактическо Съответствие
        {self._format_tactical_fit(tactical_fit)}
        
        ## Силни Страни
        {self._format_swot_strengths(swot)}
        
        ## Слаби Страни
        {self._format_swot_weaknesses(swot)}
        
        ## Идентифицирани Възможности
        {self._format_swot_opportunities(swot)}
        
        Въз основа на горните данни, предоставете пълна оценка за рекрутиране, която включва:
        
        1. Оценете осъществимостта на придобиването (скала 1-10), имайки предвид пазарната стойност и договорната ситуация
        2. Оценете техническо-тактическото съответствие (скала 1-10), имайки предвид профила на играча
        3. Оценете профила на възраст/развитие (скала 1-10), имайки предвид потенциала
        4. Предоставете крайна препоръка (Мониторинг, Придобиване, Приоритизиране, Избягване)
        5. Предложете стратегия за придобиване и план за интеграция, ако бъде нает
        
        Бъдете конкретни и стратегически в анализа си, като вземете предвид рисковите фактори и потенциалната възвръщаемост.
        """
}
        # Create user prompt

        user_prompt = recruitment_prompts.get(self.language, recruitment_prompts["pt"])
        # Define tool schema for structured output
        tools = [{
            "name": "recruitment_recommendation_tool",
            "description": "Generate comprehensive recruitment recommendation for a football player",
            "input_schema": RecruitmentDecisionMatrix.model_json_schema()
        }]
        
        response = self._call_ai_with_tool(system_prompt, user_prompt, tools)
        
        tool_input = response.content[0].input

        if isinstance(tool_input, str):
                try:
                    # Attempt to parse the string as JSON
                    import json
                    parsed_input = json.loads(tool_input)
                    args = parsed_input
                except json.JSONDecodeError as e:
                    print(f"ERROR - Failed to parse tool_input as JSON: {e}")
                    raise ValueError(f"Claude API returned an invalid response format: {tool_input}")
        else:
                # It's already a dict
            args = tool_input
        recommendation = args

        return recommendation
                
        
    
    def _call_ai(self, system_prompt, user_prompt, tools=None):
        """Chamar API de IA com os prompts fornecidos"""
        try:
            response = call_claude_api(
                api_key=self.anthropic_api_key,
                model=self.default_model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]

            )
            
            # Extrair texto da resposta
            if hasattr(response, 'content') and len(response.content) > 0:
                return response.content[0].text
            
            return "Não foi possível gerar o conteúdo solicitado."
        
        except Exception as e:
            print(f"Erro ao chamar API de IA: {str(e)}")
            return f"Erro na geração de conteúdo: {str(e)}"
    
    # Métodos auxiliares para formatação de dados nos prompts
    
    def _format_swot_strengths(self, swot):
        strengths = swot.get('strengths', []) if isinstance(swot, dict) else getattr(swot, 'strengths', [])
        result = []
        
        for s in strengths:
            if isinstance(s, dict):
                result.append(f"- {s.get('stat_name')}: {s.get('percentile')}º percentil")
            else:
                result.append(f"- {getattr(s, 'stat_name', 'N/A')}: {getattr(s, 'percentile', 'N/A')}º percentil")
        
        return "\n".join(result)
    
    def _format_swot_weaknesses(self, swot):
        weaknesses = swot.get('weaknesses', []) if isinstance(swot, dict) else getattr(swot, 'weaknesses', [])
        result = []
        
        for w in weaknesses:
            if isinstance(w, dict):
                result.append(f"- {w.get('stat_name')}: {w.get('percentile')}º percentil")
            else:
                result.append(f"- {getattr(w, 'stat_name', 'N/A')}: {getattr(w, 'percentile', 'N/A')}º percentil")
        
        return "\n".join(result)
    
    def _format_swot_opportunities(self, swot):
        opportunities = swot.get('opportunities', []) if isinstance(swot, dict) else getattr(swot, 'opportunities', [])
        result = []
        
        for o in opportunities:
            if isinstance(o, dict):
                result.append(f"- {o.get('insight')}")
            else:
                result.append(f"- {getattr(o, 'insight', 'N/A')}")
        
        return "\n".join(result)
    
    def _format_tactical_styles(self, tactical_styles):
        """Format tactical styles data for prompts"""
        if not tactical_styles or not isinstance(tactical_styles, dict):
            return "Dados de estilo tático não disponíveis"
            
        best_fits = tactical_styles.get('best_fits', [])
        if not best_fits:
            return "Estilos táticos não identificados"
            
        formatted_text = "Compatibilidade com estilos táticos:\n"
        for i, fit in enumerate(best_fits, 1):
            style_name = fit.get('style_name', 'N/A')
            style_score = fit.get('style_score', 0)
            style_description = fit.get('style_description', '')
            
            formatted_text += f"{i}. {style_name} ({style_score}% de compatibilidade)\n"
            formatted_text += f"   {style_description}\n"
            
            # Add key metrics if available
            key_metrics = fit.get('key_metrics', [])
            if key_metrics:
                formatted_text += "   Métricas relevantes: "
                metrics_text = ", ".join([m.get('display_name', 'N/A') for m in key_metrics[:3]])
                formatted_text += f"{metrics_text}\n"
                
        return formatted_text
    

    def _format_tactical_functions(self, tactical_fit):
        by_position = tactical_fit.get('by_position', {}) if isinstance(tactical_fit, dict) else getattr(tactical_fit, 'by_position', {})
        if not by_position:
            return "Dados não disponíveis"
            
        result = []
        for pos, data in by_position.items():
            if isinstance(data, dict):
                result.append(f"- {pos}: {data.get('best_fit', 'N/A')} ({data.get('best_score', 0)}%)")
            else:
                result.append(f"- {pos}: {getattr(data, 'best_fit', 'N/A')} ({getattr(data, 'best_score', 0)}%)")
        
        return "\n".join(result)
    
    def _format_function_details(self, tactical_fit):
        # Implementação simplificada - na versão real você extrairia detalhes específicos
        return "Dados detalhados de funções não disponíveis neste exemplo."
    
    def generate_all_sessions(self, player_id, technical_analysis, historical_data):
        """Gerar todas as sessões do relatório de scouting"""
        executive_summary = self.generate_executive_summary(player_id, technical_analysis)
        tactical_analysis = self.generate_tactical_analysis(player_id, technical_analysis)
        recruitment_recommendation = self.generate_recruitment_recommendation(player_id, technical_analysis, historical_data)
        
        return {
            "executive_summary": executive_summary,
            "tactical_analysis": tactical_analysis,
            "recruitment_recommendation": recruitment_recommendation
        }

    # Method to safely extract position names (moved inside class)
    def _extract_position_names(self, positions_list):
        """Extract position names from a list of position objects or dictionaries"""
        position_names = []
        
        # Process each position entry which might be a dictionary
        for pos in positions_list:
            if isinstance(pos, dict):
                # Try different common position dictionary structures
                if "name" in pos:
                    position_names.append(pos["name"])
                elif "position" in pos and isinstance(pos["position"], dict):
                    if "name" in pos["position"]:
                        position_names.append(pos["position"]["name"])
                    elif "code" in pos["position"]:
                        position_names.append(pos["position"]["code"])
                else:
                    # Add a fallback description if structure is unknown
                    position_names.append("Posição não especificada")
            else:
                # If it's already a string, use directly
                position_names.append(str(pos))
        
        # If no positions were found, use default
        if not position_names:
            position_names = ['Não disponível']
            
        return position_names