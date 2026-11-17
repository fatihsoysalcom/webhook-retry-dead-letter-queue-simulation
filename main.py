import time
import random
from collections import deque

# --- Configuration ---
MAX_RETRIES = 3
SIMULATED_WEBHOOK_FAIL_RATE = 0.6 # 60% chance of failure for demonstration
SIMULATED_PROCESSING_DELAY = 0.1 # seconds

# --- Simulated Queues (mimicking AWS SQS/Azure Service Bus) ---
# Main queue for messages awaiting processing
main_queue = deque()
# Dead-Letter Queue for messages that failed after MAX_RETRIES
dead_letter_queue = deque()

# --- Simulated Webhook Endpoint ---
def simulate_webhook_endpoint(payload):
    """
    Simulates an external webhook endpoint that sometimes fails.
    In a real scenario, this would be an HTTP POST request to an external URL.
    """
    print(f"  Attempting to send webhook for: {payload['id']}...")
    time.sleep(SIMULATED_PROCESSING_DELAY) # Simulate network latency/processing
    if random.random() < SIMULATED_WEBHOOK_FAIL_RATE:
        print(f"  Webhook for {payload['id']} FAILED.")
        return False # Simulate HTTP 5xx or network error
    else:
        print(f"  Webhook for {payload['id']} SUCCEEDED.")
        return True

# --- Webhook Sender (Producer) ---
def send_webhook_message(payload):
    """
    Sends a new webhook message to the main queue.
    Each message includes its payload and a retry_count.
    """
    message = {
        "payload": payload,
        "retry_count": 0
    }
    main_queue.append(message)
    print(f"Producer: Message {payload['id']} sent to main queue.")

# --- Webhook Processor (Consumer) ---
def process_webhook_messages():
    """
    Continuously processes messages from the main queue.
    Implements retry logic and moves failed messages to DLQ.
    """
    print("\nConsumer: Starting to process messages...")
    while main_queue: # Process until main queue is empty for this demo
        message = main_queue.popleft() # Get message from the front of the queue
        payload = message["payload"]
        retry_count = message["retry_count"]

        print(f"\nConsumer: Processing message {payload['id']} (Retry: {retry_count})...")

        # Attempt to deliver the webhook
        if simulate_webhook_endpoint(payload):
            print(f"Consumer: Message {payload['id']} successfully processed and acknowledged.")
            # In a real system, this would be a message deletion from the queue.
        else:
            # Webhook delivery failed
            retry_count += 1
            if retry_count < MAX_RETRIES:
                # Re-queue for retry (simulate delay/visibility timeout by just adding it back)
                message["retry_count"] = retry_count
                main_queue.append(message) # Add back to the end for simplicity, real systems might use delay queues
                print(f"Consumer: Message {payload['id']} failed, re-queueing (attempt {retry_count}/{MAX_RETRIES}).")
            else:
                # Max retries reached, move to Dead-Letter Queue
                dead_letter_queue.append(message)
                print(f"Consumer: Message {payload['id']} failed after {MAX_RETRIES} retries. Moving to DLQ.")

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Webhook Retry Strategy Simulation ---")

    # Simulate sending a few webhook messages
    for i in range(1, 6):
        send_webhook_message({"id": f"property_update_{i}", "data": f"status_changed_{i}"})
    print("\n--- All initial messages sent ---")

    # Process messages until the main queue is empty (or until all retries are exhausted)
    process_webhook_messages()

    print("\n--- Simulation Complete ---")
    print(f"Final Main Queue size: {len(main_queue)}")
    print(f"Final Dead-Letter Queue size: {len(dead_letter_queue)}")
    if dead_letter_queue:
        print("Messages in DLQ:")
        for msg in dead_letter_queue:
            print(f"  - {msg['payload']['id']} (Failed after {msg['retry_count']} retries)")
