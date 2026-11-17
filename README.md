# Webhook Retry Dead Letter Queue Simulation

This example demonstrates a webhook retry strategy using a simulated message queue and a dead-letter queue. It shows how messages are retried a configurable number of times before being moved to a dead-letter queue if processing consistently fails, mimicking patterns used with services like AWS SQS or Azure Service Bus for reliable event delivery.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [Azure Service Bus ve AWS SQS ile Webhook Yeniden Deneme Stratejileri](https://fatihsoysal.com/blog/azure-service-bus-ve-aws-sqs-ile-webhook-yeniden-deneme-stratejileri/).

## License

MIT — see [LICENSE](LICENSE).
