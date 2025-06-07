from typing import Optional

from pydantic import BaseModel, Field


class Quotation(BaseModel):
    units: int = Field(..., description="Целая часть числа")
    nano: int = Field(..., description="Дробная часть числа в наносекундах")


class MoneyValue(BaseModel):
    currency: str = Field(..., description="Валюта")
    units: int = Field(..., description="Целая часть суммы")
    nano: int = Field(..., description="Дробная часть суммы в наносекундах")


class PortfolioPositionDTO(BaseModel):
    figi: str = Field(..., description="FIGI-идентификатор инструмента")
    instrument_type: str = Field(..., description="Тип инструмента (например, 'share')")
    quantity: Quotation = Field(..., description="Количество инструмента в портфеле в штуках")
    average_position_price: MoneyValue = Field(..., description="Средневзвешенная цена позиции")
    expected_yield: Quotation = Field(..., description="Текущая рассчитанная доходность позиции")
    current_nkd: MoneyValue = Field(..., description="Текущий НКД (накопленный купонный доход)")
    average_position_price_pt: Quotation = Field(..., description="Средняя цена позиции в пунктах (deprecated)")
    current_price: MoneyValue = Field(..., description="Текущая цена за 1 инструмент")
    average_position_price_fifo: MoneyValue = Field(..., description="Средняя цена позиции по методу FIFO")
    quantity_lots: Quotation = Field(..., description="Количество лотов в портфеле (deprecated)")
    blocked: bool = Field(..., description="Заблокировано на бирже")
    blocked_lots: Quotation = Field(..., description="Количество бумаг, заблокированных выставленными заявками")
    position_uid: str = Field(..., description="Уникальный идентификатор позиции")
    instrument_uid: str = Field(..., description="Уникальный идентификатор инструмента")
    var_margin: MoneyValue = Field(..., description="Вариационная маржа")
    expected_yield_fifo: Quotation = Field(..., description="Текущая рассчитанная доходность позиции по FIFO")
    daily_yield: Optional[MoneyValue] = Field(None, description="Рассчитанная доходность позиции за день")
    ticker: Optional[str] = Field(None, description="Тикер инструмента")

