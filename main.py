# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import sqlite3 as lite
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


def create_db(conn):
	cur = conn.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS stocks
               (date text, trans text, symbol text, qty real, price real)''')
	conn.commit()

def get_portfolio():
	conn = lite.connect('stock.db')
	create_db(conn)
	cur = conn.cursor()
	stocks = []
	for row in cur.execute('SELECT * FROM stocks'):
		stocks.append(row[2])
	conn.close()
	return stocks



@st.cache
def load_data(ticker,START,TODAY):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


def update_portfolio(stock,datebought,quantity,prc):
	conn = lite.connect('stock.db')
	create_db(conn)
	cur = conn.cursor()
	query = '''INSERT INTO stocks VALUES ({date} ,'BUY',{symbol} ,{qty} ,{price})'''
	formatted = query.format(symbol=stock,date=datebought,qty=quantity,price=prc)
	print(formatted)
	#cur.execute(formatted)
	cur.execute('''INSERT INTO stocks VALUES('2021-08-26','BUY','AAPL',90,26.7)''')
	conn.commit()
	conn.close()


# Plot raw data
def plot_raw_data(data):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
def main():
	START = "2020-01-01"
	TODAY = date.today().strftime("%Y-%m-%d")

	st.title('Stock Portfolio Manager')
	###stock form


	form = st.form(key='my_form')
	stock =form.text_input(label='Stock symbol')
	datebought=form.text_input(label='Date bought')
	qty=form.text_input(label='Quantity')
	price=form.text_input(label='Price')

	submit = form.form_submit_button(label='Submit')
	if(submit):
		update_portfolio(stock,datebought,qty,price)

	##stock display
	stocks = get_portfolio()
	
	selected_stock = st.selectbox('Select stock from portfolio', stocks)

	#n_years = st.slider('Years of prediction:', 1, 4)
	#period = n_years * 365

	data_load_state = st.text('Loading data...')
	data = load_data(selected_stock,START,TODAY)
	data_load_state.text('Loading data... done!')

	st.subheader('Raw data')
	st.write(data.tail())
	plot_raw_data(data)

if __name__ == "__main__":
    main()
