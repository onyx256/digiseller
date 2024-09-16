from datetime import datetime
from enum import Enum


class Currency(Enum):
    WMR = 'WMR'
    WMZ = 'WMZ'
    WME = 'WME'


class OperationType(Enum):
    AGENT_ACCURALS = 'agent_accurals'
    PRODUCT_SALES = 'product_sales'
    ADD_FUNDS = 'add_funds'
    EXCHANGE_RESPONSE = 'exchange_response'
    EXCHANGE_REQUEST = 'exchange_request'
    REFUND = 'refund'
    ADV_GOOD = 'adv_goods'
    EXTERNAL_COMMISSIONS = 'external_commissions'
    HARD_DISK_RENT = 'hard_disk_rent'
    EXTRA_PARTNER_SPACE = 'extra_partner_space'
    GIFT_CERTIFICATES = 'gift_certificates'
    TRANSFER_TO_WALLET = 'transfer_to_wallet'


class CodeFilter(Enum):
    ONLY_WAITING_CHECK_CODE = 'only_waiting_check_code'
    HIDE_WAITING_CODE_CHECK = 'hide_waiting_code_check'


class AllowType(Enum):
    EXCLUDE = 'exclude'
    ONLY = 'only'


class Operations:
    def __init__(self, digiseller) -> None:
        self.digiseller = digiseller

    def get_operations(self,
                       page: int = 1,
                       count: int = 10,
                       currency: Currency | str | None = None,
                       operation_type: OperationType | str | None = None,
                       code_filter: CodeFilter | str | None = None,
                       allow_type: AllowType | str | None = None,
                       date_start: datetime = datetime(2000, 1, 1, 0, 0, 0).strftime('%Y-%m-%dT%H:%M'),
                       date_finish: datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')):
        resp = self.digiseller.request(
            'get', 'sellers/account/receipts',
            page=page,
            count=count,
            currency=currency.value if isinstance(currency, Currency) else currency,
            type=operation_type.value if isinstance(operation_type, OperationType) else operation_type,
            codeFilter=code_filter.value if isinstance(code_filter, CodeFilter) else code_filter,
            allowType=allow_type.value if isinstance(allow_type, AllowType) else allow_type,
            start=date_start,
            finish=date_finish
        )
        data = resp.json()
        items = data['content']['items']
        print(items)
