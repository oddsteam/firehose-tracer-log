import datetime
import json
import os
import pika


if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", 5672)
    queue_name = os.getenv("QUEUE_NAME", "firehose")

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host, port=port))
    channel = connection.channel()
    
    queue_name = queue_name
    result = channel.queue_declare(queue=queue_name, exclusive=False)
        
    channel.queue_bind(exchange='amq.rabbitmq.trace',
                       queue=queue_name,
                       routing_key="#")
    
    print(' [*] Waiting for logs. To exit press CTRL+C')
    
    def callback(ch, method, properties, body):
        with open('logs/log.txt', 'a') as f:
            body_serialized = serializing_message(body.decode())
            log = json.dumps({"timestamp": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f"),"body":body_serialized, "method": method.routing_key, "routing_keys": properties.headers["routing_keys"]})
            f.write(log + "\n")
    
    def serializing_message(message):
        try:
            json_dict = json.loads(message)
            if("app_secret" in json_dict):
                del json_dict["app_secret"]
            if("appSecret" in json_dict):
                del json_dict["appSecret"]
            return json.dumps(json_dict)
        except:
            return message
    
    channel.basic_consume(on_message_callback=callback,
                          queue=queue_name,
                          auto_ack=True)
    
    channel.start_consuming()