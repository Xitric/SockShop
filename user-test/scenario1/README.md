# Scenario 1
The Web Shop has seen a drastic increase in popularity, and as a result is returning internal server errors to most clients in the checkout workflow (_Significant service error increase_). Operators are unsure of the cause to these internal server errors, and decide to investigate distributed traces to identify the cause. Upon investigation, they realize that the third-party user service is unable to keep up with the increased load causing timeouts (_3rd party failure_).