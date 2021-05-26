# Scenario 3
Changes from previous scenario:

- orders
    - replicas: 12
    - cpu: 200m
    - memory: 500Mi

After having scaled the orders service horizontally, internal server errors have ceased to occur, and response times have dropped to 2 seconds which is still unacceptable. Upon investigation, operators find that since the orders service is now capable of handling a higher throughput, the load on the third-party service has once again increased, making it the new bottleneck (_Slow service response_).
