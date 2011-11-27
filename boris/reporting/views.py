from boris.reporting.reports.monthly_stats import MonthlyStats
from boris.reporting.core import ReportResponse


def monthly_stats(request):
    return ReportResponse(MonthlyStats, 2011)
