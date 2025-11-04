# RPA Project

This is a project done using [Python](https://www.python.org/) that will analyze a provided [Excel file](./Sales.xlsx) and generate some reports about some of its statistics.

## How to use the app

You need to have the following libraries installed:

- [Pandas](https://pandas.pydata.org/)
- [Twilio](http://twilio.com/) (Including a Twilio Account)
- [ReportLab](https://docs.reportlab.com/)
- [Matplotlib](https://matplotlib.org/)

On [main.py](./main.py) you can configure the correct parameters for your [Twilio](http://twilio.com/) account, you will also need to install [ngrok](https://ngrok.com/) in order to send the reports to a WhatsApp number with Twilio.

To run this program, follow these steps:

1. Open a terminal inside the ['Reports'](./Reports/) folder, and run the ['host_files.py'](./Reports/host_files.py) script with the following command:

```
python host_files.py
```

2. On another terminal, run the following command to expose your local Python server to the Internet:

```
ngrok http 8000
```

You should see a URL be generated here, copy it for later.

3. In [main.py](./main.py), configure the Twilio parameters with the ones from your own [Twilio](http://twilio.com/) account.
4. In [main.py](./main.py), on line 48, paste the ngrok URL you copied earlier.
5. Now, you can run the [main.py](./main.py) script to generate your reports and later send them to a WhatsApp number:

```
python main.py
```