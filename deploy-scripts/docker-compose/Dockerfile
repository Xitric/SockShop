FROM scratch

ADD otelcontribcol_linux_amd64 /otelcontribcol_linux_amd64
EXPOSE 8888 9411 13133 14250 14268 55679 55680

ENTRYPOINT [ "/otelcontribcol_linux_amd64" ]
CMD ["--config=/etc/config/otel-collector-config.yaml"]
