# Scenario 2
Changes from previous scenario:

- user
    - cpu: 150m
    - memory: 128Mi

After having improved the performance of the third-party user service, the amount of errors drops to near-zero, but response times of 14 seconds are still unacceptable. Upon investigation, the operators realize that a thread pool inside the SockShop orders service is becoming increasingly backlogged, because it cannot keep up with the request rate (_Failure to call service_).
