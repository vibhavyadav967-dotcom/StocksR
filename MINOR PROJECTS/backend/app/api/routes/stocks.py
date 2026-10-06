from fastapi import APIRouter

router = APIRouter(prefix='/api', tags=['stocks'])


@router.get('/stocks')
def list_stocks():
    return {'symbols': ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN']}
