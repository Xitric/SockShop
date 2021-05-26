# Scenario 4
Changes from previous scenario:

- user
    - replicas: 4
    - cpu: 250m
    - memory: 128Mi

The Web Shop is now capable of responding to clients in around 50 ms. Operators investigate a series of spans and observe that the checkout workflow continues to run for a long time in the background after a response has been returned to the user. While this does not impact the service response times, it is an inefficiency which must be optimized.
