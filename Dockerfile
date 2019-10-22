FROM python:3

WORKDIR /app

ADD . /app

RUN pip install pandas
RUN pip install geopy
RUN pip install Transform
RUN pip install graphviz
RUN pip install matplotlib
RUN pip install proj
RUN pip install pyproj
RUN pip install xlrd
RUN pip install XlsxWriter
RUN pip install GDAL
RUN pip install sklearn
RUN pip install rasterio

CMD [ "python", "main.py" ]

