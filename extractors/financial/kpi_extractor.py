
# KPI Extractor : Converts a FinancialResult into individual FinancialMetric objects.


from models.financial_metric import FinancialMetric


class KPIExtractor:

    def extract(self, financial_result):

        metrics = []

        metric_map = {

            "Revenue": financial_result.revenue,

            "Gross Profit": financial_result.gross_profit,

            "Operating Profit": financial_result.operating_profit,

            "Net Profit": financial_result.net_profit,

            "EPS": financial_result.eps,

        }

        for name, value in metric_map.items():

            if value is None:
                continue

            metrics.append(

                FinancialMetric(
                    announcement_id = financial_result.announcement_id,
                    company_name =  financial_result.company_name,
                    stock_code = financial_result.stock_code,
                    metric_name=name,
                    current_value=value,
                    currency=financial_result.currency,
                    reporting_period=financial_result.reporting_period

                )

            )

        return metrics