class TacticalAnalysisDataExtractor:
    """Extrator de dados para análise tática de jogadores"""
    
    def __init__(self):
        """Inicializar extrator com categorias e métricas"""
        # Definir métricas por categoria
        self.passing_metrics = [
            {"name": "Precisão de passe", "stat": "successfulPasses", "total_stat": "passes", "is_percentage": True},
            {"name": "Passes criativos", "stat": "successfulSmartPasses", "total_stat": "smartPasses", "is_percentage": True},
            {"name": "Passes para o terço final", "stat": "successfulPassesToFinalThird", "total_stat": "passesToFinalThird", "is_percentage": True},
            {"name": "Passes progressivos", "stat": "successfulProgressivePasses", "total_stat": "progressivePasses", "is_percentage": True},
            {"name": "Passes-chave", "stat": "keyPasses", "total_stat": None, "is_percentage": False}
        ]
        
        self.offensive_metrics = [
            {"name": "Gols", "stat": "goals", "total_stat": None, "is_percentage": False},
            {"name": "Finalização no alvo", "stat": "shotsOnTarget", "total_stat": "shots", "is_percentage": True},
            {"name": "Toques na área", "stat": "touchInBox", "total_stat": None, "is_percentage": False},
            {"name": "Expected Goals", "stat": "xgShot", "total_stat": None, "is_percentage": False},
            {"name": "Dribles bem-sucedidos", "stat": "successfulDribbles", "total_stat": "dribbles", "is_percentage": True}
        ]
        
        self.defensive_metrics = [
            {"name": "Interceptações", "stat": "interceptions", "total_stat": None, "is_percentage": False},
            {"name": "Recuperações em contrapressão", "stat": "counterpressingRecoveries", "total_stat": None, "is_percentage": False},
            {"name": "Duelos defensivos ganhos", "stat": "defensiveDuelsWon", "total_stat": "defensiveDuels", "is_percentage": True},
            {"name": "Recuperações no campo adversário", "stat": "opponentHalfRecoveries", "total_stat": "recoveries", "is_percentage": True},
            {"name": "Carrinhos bem-sucedidos", "stat": "successfulSlidingTackles", "total_stat": "slidingTackles", "is_percentage": True}
        ]
        
        self.physical_metrics = [
            {"name": "Duelos ganhos", "stat": "duelsWon", "total_stat": "duels", "is_percentage": True},
            {"name": "Duelos aéreos ganhos", "stat": "aerialDuelsWon", "total_stat": "aerialDuels", "is_percentage": True},
            {"name": "Corridas progressivas", "stat": "progressiveRun", "total_stat": None, "is_percentage": False},
            {"name": "Acelerações", "stat": "accelerations", "total_stat": None, "is_percentage": False},
            {"name": "Faltas sofridas", "stat": "foulsSuffered", "total_stat": None, "is_percentage": False}
        ]
        
        # Todos os grupos de métricas para processamento em lote
        self.all_metric_groups = [
            {"name": "Passes", "metrics": self.passing_metrics},
            {"name": "Ataque", "metrics": self.offensive_metrics},
            {"name": "Defesa", "metrics": self.defensive_metrics},
            {"name": "Físico", "metrics": self.physical_metrics}
        ]
    
    def extract_player_metrics(self, player_data):
        """
        Extrai métricas táticas de um jogador
        
        Args:
            player_data: Dicionário com dados do jogador
            
        Returns:
            Dicionário com métricas formatadas por categoria
        """
        result = {}
        
        # Obter estatísticas totais e médias
        total_stats = player_data.get("total", {})
        average_stats = player_data.get("average", {})
        percent_stats = player_data.get("percent", {})
        
        # Processar cada grupo de métricas
        for group in self.all_metric_groups:
            group_name = group["name"]
            result[group_name] = []
            
            for metric in group["metrics"]:
                metric_name = metric["name"]
                stat_name = metric["stat"]
                total_stat_name = metric["total_stat"]
                is_percentage = metric["is_percentage"]
                
                # Obter valor da estatística
                value = total_stats.get(stat_name, 0)
                
                # Formatar conforme o tipo de métrica
                if is_percentage and total_stat_name:
                    total_value = total_stats.get(total_stat_name, 0)
                    percentage = percent_stats.get(f"{stat_name.replace('successful', '')}", 0)
                    
                    # Às vezes o percentual já está calculado na API
                    if percentage:
                        formatted_metric = {
                            "name": metric_name,
                            "value": value,
                            "total": total_value,
                            "percentage": percentage,
                            "per90": average_stats.get(stat_name, 0)
                        }
                    else:
                        # Calcular percentual manualmente se não estiver disponível
                        percentage = (value / total_value * 100) if total_value > 0 else 0
                        formatted_metric = {
                            "name": metric_name,
                            "value": value,
                            "total": total_value,
                            "percentage": round(percentage, 2),
                            "per90": average_stats.get(stat_name, 0)
                        }
                else:
                    # Métrica simples sem percentual
                    formatted_metric = {
                        "name": metric_name,
                        "value": value,
                        "per90": average_stats.get(stat_name, 0)
                    }
                
                result[group_name].append(formatted_metric)
        
        return result
    
    def format_for_prompt(self, metrics_by_category):
        """
        Formata as métricas para uso em prompt de IA
        
        Args:
            metrics_by_category: Dicionário com métricas por categoria
            
        Returns:
            Texto formatado para uso em prompts
        """
        prompt_text = ""
        
        for category, metrics in metrics_by_category.items():
            prompt_text += f"\n### {category}\n"
            
            for metric in metrics:
                name = metric["name"]
                value = metric["value"]
                per90 = metric["per90"]
                
                # Verificar se é uma métrica percentual
                if "percentage" in metric:
                    total = metric["total"]
                    percentage = metric["percentage"]
                    prompt_text += f"- {name}: {value}/{total} ({percentage}%) | {per90:.2f} por 90 min\n"
                else:
                    prompt_text += f"- {name}: {value} | {per90:.2f} por 90 min\n"
        
        return prompt_text
    


if __name__ == '__main__':
    extractor = TacticalAnalysisDataExtractor()
    try:
        
        player_data = {
        "playerId": 372255,
        "competitionId": 524,
        "seasonId": 188994,
        "positions": [
            {
                "position": {
                    "name": "Striker",
                    "code": "cf"
                },
                "percent": 100
            }
        ],
        "total": {
            "matches": 33,
            "matchesInStart": 31,
            "matchesSubstituted": 13,
            "matchesComingOff": 2,
            "minutesOnField": 2844,
            "minutesTagged": 2844,
            "goals": 24,
            "assists": 1,
            "shots": 98,
            "headShots": 19,
            "yellowCards": 5,
            "redCards": 0,
            "directRedCards": 0,
            "penalties": 3,
            "linkupPlays": 238,
            "duels": 587,
            "duelsWon": 228,
            "defensiveDuels": 118,
            "defensiveDuelsWon": 21,
            "offensiveDuels": 278,
            "offensiveDuelsWon": 135,
            "aerialDuels": 68,
            "aerialDuelsWon": 31,
            "fouls": 46,
            "passes": 768,
            "successfulPasses": 613,
            "smartPasses": 23,
            "successfulSmartPasses": 10,
            "passesToFinalThird": 75,
            "successfulPassesToFinalThird": 51,
            "crosses": 23,
            "successfulCrosses": 6,
            "forwardPasses": 158,
            "successfulForwardPasses": 103,
            "backPasses": 203,
            "successfulBackPasses": 184,
            "throughPasses": 22,
            "successfulThroughPasses": 7,
            "keyPasses": 11,
            "successfulKeyPasses": 11,
            "verticalPasses": 227,
            "successfulVerticalPasses": 191,
            "longPasses": 40,
            "successfulLongPasses": 20,
            "dribbles": 90,
            "successfulDribbles": 56,
            "interceptions": 77,
            "defensiveActions": 207,
            "successfulDefensiveAction": 153,
            "attackingActions": 234,
            "successfulAttackingActions": 107,
            "freeKicks": 0,
            "freeKicksOnTarget": 0,
            "directFreeKicks": 0,
            "directFreeKicksOnTarget": 0,
            "corners": 0,
            "successfulPenalties": 2,
            "successfulLinkupPlays": 179,
            "accelerations": 15,
            "pressingDuels": 236,
            "pressingDuelsWon": 0,
            "looseBallDuels": 123,
            "looseBallDuelsWon": 41,
            "missedBalls": 32,
            "shotAssists": 26,
            "shotOnTargetAssists": 11,
            "recoveries": 110,
            "opponentHalfRecoveries": 64,
            "dangerousOpponentHalfRecoveries": 16,
            "losses": 319,
            "ownHalfLosses": 88,
            "dangerousOwnHalfLosses": 5,
            "xgShot": 17.87,
            "xgAssist": 2.77,
            "xgSave": 0,
            "receivedPass": 642,
            "touchInBox": 167,
            "progressiveRun": 44,
            "offsides": 10,
            "clearances": 8,
            "secondAssists": 3,
            "thirdAssists": 0,
            "shotsBlocked": 2,
            "foulsSuffered": 60,
            "progressivePasses": 72,
            "counterpressingRecoveries": 62,
            "slidingTackles": 12,
            "goalKicks": 0,
            "dribblesAgainst": 28,
            "dribblesAgainstWon": 11,
            "goalKicksShort": 0,
            "goalKicksLong": 0,
            "shotsOnTarget": 45,
            "successfulProgressivePasses": 54,
            "successfulSlidingTackles": 9,
            "successfulGoalKicks": 0,
            "fieldAerialDuels": 68,
            "fieldAerialDuelsWon": 31,
            "gkCleanSheets": 0,
            "gkConcededGoals": 0,
            "gkShotsAgainst": 0,
            "gkExits": 0,
            "gkSuccessfulExits": 0,
            "gkAerialDuels": 0,
            "gkAerialDuelsWon": 0,
            "gkSaves": 0,
            "newDuelsWon": 253,
            "newDefensiveDuelsWon": 64,
            "newOffensiveDuelsWon": 117,
            "newSuccessfulDribbles": 46,
            "lateralPasses": 227,
            "successfulLateralPasses": 191
        },
        "average": {
            "passLength": 15.41,
            "longPassLength": 23.96,
            "dribbleDistanceFromOpponentGoal": 34.97,
            "ballRecoveries": 3.48,
            "duels": 18.58,
            "defensiveDuels": 3.73,
            "offensiveDuels": 8.8,
            "aerialDuels": 2.15,
            "fouls": 1.46,
            "goals": 0.76,
            "assists": 0.03,
            "passes": 24.3,
            "smartPasses": 0.73,
            "passesToFinalThird": 2.37,
            "crosses": 0.73,
            "dribbles": 2.85,
            "shots": 3.1,
            "headShots": 0.6,
            "interceptions": 2.44,
            "successfulDefensiveAction": 4.84,
            "yellowCards": 0.16,
            "redCards": 0,
            "directRedCards": 0,
            "successfulAttackingActions": 3.39,
            "freeKicks": 0,
            "directFreeKicks": 0,
            "corners": 0,
            "penalties": 0.09,
            "accelerations": 0.47,
            "looseBallDuels": 3.89,
            "missedBalls": 1.01,
            "forwardPasses": 5,
            "backPasses": 6.42,
            "throughPasses": 0.7,
            "keyPasses": 0.35,
            "verticalPasses": 7.18,
            "longPasses": 1.27,
            "shotAssists": 0.82,
            "shotOnTargetAssists": 0.35,
            "linkupPlays": 7.53,
            "opponentHalfRecoveries": 2.03,
            "dangerousOpponentHalfRecoveries": 0.51,
            "ballLosses": 0,
            "losses": 10.09,
            "ownHalfLosses": 2.78,
            "dangerousOwnHalfLosses": 0.16,
            "duelsWon": 7.22,
            "defensiveDuelsWon": 0.66,
            "offensiveDuelsWon": 4.27,
            "successfulPasses": 19.4,
            "successfulSmartPasses": 0.32,
            "successfulCrosses": 0.19,
            "successfulForwardPasses": 3.26,
            "successfulBackPasses": 5.82,
            "successfulThroughPasses": 0.22,
            "successfulKeyPasses": 0.35,
            "successfulVerticalPasses": 6.04,
            "successfulLongPasses": 0.63,
            "successfulDribbles": 1.77,
            "defensiveActions": 6.55,
            "attackingActions": 7.41,
            "freeKicksOnTarget": 0,
            "directFreeKicksOnTarget": 0,
            "successfulPenalties": 0.06,
            "successfulLinkupPlays": 5.66,
            "looseBallDuelsWon": 1.3,
            "successfulPassesToFinalThird": 1.61,
            "xgShot": 0.57,
            "xgAssist": 0.09,
            "xgSave": 0,
            "receivedPass": 20.32,
            "touchInBox": 5.28,
            "progressiveRun": 1.39,
            "offsides": 0.32,
            "clearances": 0.25,
            "secondAssists": 0.09,
            "thirdAssists": 0,
            "foulsSuffered": 1.9,
            "progressivePasses": 2.28,
            "counterpressingRecoveries": 1.96,
            "slidingTackles": 0.38,
            "goalKicks": 0,
            "shotsBlocked": 0.06,
            "shotsOnTarget": 1.42,
            "successfulProgressivePasses": 1.71,
            "successfulSlidingTackles": 0.28,
            "successfulGoalKicks": 0,
            "dribblesAgainst": 0.89,
            "dribblesAgainstWon": 0.35,
            "goalKicksShort": 0,
            "goalKicksLong": 0,
            "fieldAerialDuels": 2.15,
            "fieldAerialDuelsWon": 0.98,
            "gkConcededGoals": 0,
            "gkShotsAgainst": 0,
            "gkExits": 0,
            "gkAerialDuels": 0,
            "gkSaves": 0,
            "gkSuccessfulExits": 0,
            "gkAerialDuelsWon": 0,
            "newDuelsWon": 8.01,
            "newDefensiveDuelsWon": 2.03,
            "newOffensiveDuelsWon": 3.7,
            "newSuccessfulDribbles": 1.46,
            "lateralPasses": 7.18,
            "successfulLateralPasses": 6.04
        },
        "percent": {
            "duelsWon": 38.84,
            "defensiveDuelsWon": 17.8,
            "offensiveDuelsWon": 48.56,
            "aerialDuelsWon": 45.59,
            "successfulPasses": 79.82,
            "successfulSmartPasses": 43.48,
            "successfulPassesToFinalThird": 68,
            "successfulCrosses": 26.09,
            "successfulDribbles": 62.22,
            "shotsOnTarget": 45.92,
            "headShotsOnTarget": 47.37,
            "goalConversion": 24.49,
            "directFreeKicksOnTarget": 0,
            "penaltiesConversion": 66.67,
            "win": 81.3,
            "successfulForwardPasses": 65.19,
            "successfulBackPasses": 90.64,
            "successfulThroughPasses": 31.82,
            "successfulKeyPasses": 100,
            "successfulVerticalPasses": 84.14,
            "successfulLongPasses": 50,
            "successfulShotAssists": 42.31,
            "successfulLinkupPlays": 75.21,
            "yellowCardsPerFoul": 10.9,
            "successfulProgressivePasses": 75,
            "successfulSlidingTackles": 75,
            "successfulGoalKicks": 0,
            "dribblesAgainstWon": 39.29,
            "fieldAerialDuelsWon": 45.59,
            "gkSaves": 0,
            "gkSuccessfulExits": 0,
            "gkAerialDuelsWon": 0,
            "newDuelsWon": 43.1,
            "newDefensiveDuelsWon": 54.24,
            "newOffensiveDuelsWon": 42.09,
            "newSuccessfulDribbles": 51.11,
            "successfulLateralPasses": 84.14
        },
        "roundId": 0,
        "wyId": 372255,
        "height": 174,
        "weight": 72,
        "birthDate": "1997-08-22",
        "birthArea": {
            "id": 32,
            "alpha2code": "AR",
            "alpha3code": "ARG",
            "name": "Argentina"
        },
        "passportArea": {
            "id": 32,
            "alpha2code": "AR",
            "alpha3code": "ARG",
            "name": "Argentina"
        },
        "role": {
            "name": "Forward",
            "code2": "FW",
            "code3": "FWD"
        },
        "foot": "right",
        "currentTeamId": 3161,
        "currentNationalTeamId": 12274,
        "gender": "male",
        "status": "active",
        "imageDataURL": "https://cdn5.wyscout.com/photos/players/public/g404462_100x130.png",
        "contract": {
            "contractExpiration": "2029-06-30",
            "agencies": [
                "Footfeel ISM"
            ]
        },
        "age": 27,
        "name": "Lautaro Javier Mart\u00ednez"
    }
        if player_data:
            metrics = extractor.extract_player_metrics(player_data)
            formatted_prompt = extractor.format_for_prompt(metrics)
            print(formatted_prompt)
        else:
            print("Jogador não encontrado.")
    except ImportError:
        print("Erro ao importar o módulo de serviço de dados. Verifique se o caminho está correto.")


