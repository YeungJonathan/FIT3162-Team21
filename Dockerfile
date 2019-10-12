FROM python:3
RUN pip install GDAL
RUN pip install geopy
RUN pip install graphviz
RUN pip install matplotlib
RUN pip install pandas
RUN pip install proj
RUN pip install pyproj
RUN pip install rasterio
RUN pip install sklearn
RUN pip install Transform
RUN pip install xlrd
RUN pip install XlsxWriter
CMD [ "python", "./main.py" ]

