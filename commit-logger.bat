# bash git-logger.sh
# git-log.json유효한지 확인

# cp git-commit-logger.py dubbo/git-commit-logger.py
cd dubbo
python git-commit-logger.py 100
cd ..
cd kafka
python git-commit-logger.py 100
cd ..
cd skywa
python skywalking/git-commit-logger.py 100
cd ..
cd flink
python flink/git-commit-logger.py flink 100
cd ..
cd rocketmq
python rocketmq/git-commit-logger.py 100
cd ..
cd shardingshpere
python shardingsphere/git-commit-logger.py 100
cd ..
cd hadoop
python hadoop/git-commit-logger.py 100
cd ..
cd pulsar
python pulsar/git-commit-logger.py 100
cd ..
cd druid
python druid/git-commit-logger.py 100
cd ..
cd zookeeper
python zookeeper/git-commit-logger.py 100
cd ..

# commits에 올바르게 만들어졌는지 확인
