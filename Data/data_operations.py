import pandas as pd
import yfinance as yf
from typing import Optional
import os

def get_data(symbol: str, interval: str = '5m', period: str = "60d") -> Optional[pd.DataFrame]:
    """
    Descarga datos intradía de Yahoo Finance para un símbolo específico.
    Argumentos:
    symbol: str - El símbolo de la acción o activo financiero.
    interval: str - El intervalo de tiempo para los datos intradía (ej. '1m', '5m', '15m', '30m', '60m').
    period: str - El periodo de tiempo para el cual se desean los datos (ej. '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max').

    Returns:
        Un DataFrame de pandas con los datos históricos si la descarga es exitosa
        y el DataFrame no está vacío, de lo contrario, retorna None.
    """

    data_intraday = None
    try:
        data_intraday = yf.download(tickers=symbol, period=period, interval=interval)
        if not data_intraday.empty:
            print(f"Datos intradía ({interval}) para {symbol} descargados.")
            print(data_intraday.head())
            print(f"Número total de puntos de datos: {len(data_intraday)}")
        else:
            print(
                f"No se pudieron descargar datos intradía ({interval}) para {symbol} en el rango/periodo especificado.")
            print(
                "Esto suele ocurrir porque Yahoo Finance no proporciona datos históricos intradía amplios de forma gratuita.")
    except Exception as e:
        print(f"Ocurrió un error durante la descarga: {e}")
        return None
    data_intraday.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in
                             data_intraday.columns.values]
    data_intraday.rename(
        columns={'Open_' + symbol: 'Open', 'High_' + symbol: 'High', 'Low_' + symbol: 'Low', 'Close_' + symbol: 'Close',
                 'Volume_' + symbol: 'Volume'}, inplace=True)
    return data_intraday


def save_data(symbol: str, interval: str, period: str) -> bool:
    """
    Guarda los datos descargados en un archivo CSV.
    Argumentos:
    symbol: str - El símbolo de la acción o activo financiero.
    interval: str - El intervalo de tiempo para los datos intradía.
    period: str - El periodo de tiempo para el cual se descargaron los datos.
    """

    # Verifica si puede descargar la información
    data = get_data(symbol, interval, period)
    # En caso de no poder, cancela el guardado
    if data is None:
        return False
    filename = f"{symbol}_{interval}.csv"

    #Verifica si el archivo ya existe
    if os.path.exists(filename):
        # Si el archivo ya existe, lo lee
        existing_data = pd.read_csv(filename, index_col=0, parse_dates=True)
        # Combina los datos existentes con los nuevos
        data = pd.concat([existing_data, data])
        # Elimina duplicados
        data = data[~data.index.duplicated(keep='last')]
        # Elimina el archivo existente
        os.remove(filename)
        # Crea uno con el mismo nombre y guarda los datos combinados
        data.to_csv(filename)
        print(f"Datos combinados guardados en {filename}.")
    else:
        # Si el archivo no existe, lo crea y guarda los datos
        data.to_csv(filename)
        print(f"Datos guardados en {filename}.")

    return True

if __name__ == "__main__":
    # Pruebas
    symbol = "BTC-USD"
    interval = "5m"
    period = "60d"
    save_data(symbol, interval, period)
    #actual_data = pd.read_csv(f"{symbol}_{interval}.csv")
    #print(actual_data)