from ninja_extra.router import Router
from datetime import date
from typing import Optional

from .service import SalesReportGenerator
router = Router()


@router.get("sales/",url_name="sales")
def download_sales_report(request, fecha_min: str = None, fecha_max: str = None):
    """
    Endpoint to download sales report.
    """
    filters = {
        "start_date": fecha_min,
        "end_date": fecha_max
    }
    print("Filters", filters)
    result = SalesReportGenerator(filters).generate_report()
    return result
  