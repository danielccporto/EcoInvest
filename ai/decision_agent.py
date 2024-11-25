import pandas as pd

class DecisionAgent:
    def __init__(self, esg_data, financial_data):
        """
        Inicializa o agente com dados ESG e financeiros.
        """
        self.esg_data = esg_data
        self.financial_data = financial_data

    def analyze_data(self):
        """
        Analisa os dados ESG e financeiros para identificar empresas
        com alta pontuação ESG e bom desempenho financeiro.
        """
        try:
            # Combinar os dados ESG e financeiros com base na empresa
            combined_data = pd.merge(self.esg_data, self.financial_data, on="Empresa")

            # Filtrar empresas com alta pontuação ESG e crescimento financeiro
            recommendations = combined_data[
                (combined_data["Pontuação ESG"] >= 80) &
                (combined_data["Crescimento (%)"] >= 5)
            ]
            return recommendations.to_dict(orient="records")
        except Exception as e:
            return {"error": f"Erro ao analisar os dados: {str(e)}"}

    def suggest_actions(self):
        """
        Gera recomendações baseadas nos padrões identificados nos dados.
        """
        recommendations = self.analyze_data()
        if "error" in recommendations:
            return recommendations

        actions = [
            {
                "Empresa": rec["Empresa"],
                "Recomendação": "Investir" if rec["Crescimento (%)"] >= 10 else "Monitorar"
            }
            for rec in recommendations
        ]
        return actions
