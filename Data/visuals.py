import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd

def plot_candlestick(symbol: str, interval: str, period: int = 30):
    """
    Plotea un gráfico de velas (candlestick) para el símbolo y periodo especificados.
    Argumentos:
    symbol: str - El símbolo de la acción o activo financiero.
    interval: str - El intervalo de tiempo para los datos intradía.
    period: str - El periodo de tiempo para el cual se descargaron los datos.
    units: int - Número de unidades a mostrar en el gráfico.
    """
    # Carga los datos
    data = pd.read_csv(f"{symbol}_{interval}.csv", index_col=0, parse_dates=True)
    print(data)

    # Toma los últimos n datos del arreglo
    data_last = data.tail(period)

    fig = mpf.plot(data_last,
                   type='candle',  # Especifica el tipo de gráfico como velas
                   style='yahoo',  # Estilo gráfico
                   title=f'Gráfico de Velas de {symbol}, en tramos de {interval}',  # Título del gráfico
                   ylabel='Precio',  # Etiqueta del eje Y principal
                   ylabel_lower='Volumen',  # Etiqueta del eje Y del volumen
                   figscale=1.5  # Opcional: Escala el tamaño de la figura
                   )
    plt.show()


#sección de pruebas
if __name__ == "__main__":
    # Prueba de la función plot_candlestick
    symbol = "BTC-USD"
    interval = "5m"
    period = 15
    plot_candlestick(symbol, interval, period)
