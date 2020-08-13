FROM python:3.7-slim AS builder
ADD ./code /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
#RUN apt-get update
#RUN apt-get install libxml2-dev libxslt-dev python3-dev gcc -y
RUN pip3 install --target=/app Cython
RUN pip3 install --target=/app requests==2.21.0
#RUN pip3 install --target=/app lxml==4.1.1
RUN pip3 install --target=/app beautifulsoup4==4.6.0
RUN pip3 install --target=/app Jinja2==2.10
RUN pip3 install --target=/app joblib==0.13.2
RUN pip3 install --target=/app numpy==1.19.1
RUN pip3 install --target=/app scipy==1.5.1
RUN pip3 install --target=/app "scikit-learn==0.20.2"
RUN pip3 install --target=/app gensim==3.8.3

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/configuration.py"]
