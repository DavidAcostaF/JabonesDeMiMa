from ninja_extra.router import Router
from datetime import date
from typing import Optional

from .service import SalesReportGenerator
router = Router()


@router.get("sales/",url_name="sales")
def download_sales_report(request, start_date: date = None, end_date: date = None):
    """
    Endpoint to download sales report.
    """
    filters = {
        "start_date": start_date,
        "end_date": end_date
    }
    result = SalesReportGenerator(filters).generate_report()
    print(result)
    return result
  