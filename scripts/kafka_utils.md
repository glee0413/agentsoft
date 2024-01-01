# kafka管理
## topic管理
```
# 查看topic
kafka-topics.sh --list --bootstrap-server localhost:9092
# 删除topic
kafka-topics.sh --delete --topic office.df5cf027-dc95-488c-96c8-7d18c99bf960 --bootstrap-server localhost:9092
# 查看topic中的消息
kafka-console-consumer.sh --topic lancer.123 --bootstrap-server localhost:9092 --from-beginning
```