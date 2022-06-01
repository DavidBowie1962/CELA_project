import datetime

import tinvest
import sys
import creds
from tinkoff.invest import Client, InstrumentIdType, Instrument
#from tinkoff.invest.token import TOKEN


def main() -> int:
    with Client(creds.token) as client:
        # info about account
        r = client.users.get_accounts()
        #get_portfolio
        p = client.operations.get_portfolio(account_id=creds.account_id)
        #список операций за период
        m = client.operations.get_operations(
            account_id=creds.account_id,
            from_= datetime.datetime(2019,1,1),
            to=datetime.datetime.now()
        )
        # информация по акции
        #figi = 'BBG006L8G4H1'
        ticker = 'USDFIXME'
        a = client.instruments.share_by(
            id=ticker,
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
            class_code = creds.class_code_shares)

        #информация по инструменту
        figi="BBG000N9MNX3"
        #ticker="SU29013RMFS8"
        k = client.instruments.share_by(
            id=figi,
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            #class_code = creds.class_code_spb
        )
        print(a)

    return 0


if __name__ == "__main__":
    sys.exit(main())