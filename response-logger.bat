# bash git-logger.sh
# git-log.json유효한지 확인

python dubbo/git-commit-logger.py 100
python kafka/git-commit-logger.py 100
python skywalking/git-commit-logger.py 100
python flink/git-commit-logger.py flink 100
python rocketmq/git-commit-logger.py 100
python shardingsphere/git-commit-logger.py 100
python hadoop/git-commit-logger.py 100
python pulsar/git-commit-logger.py 100
python druid/git-commit-logger.py 100
python zookeeper/git-commit-logger.py 100

# commits에 올바르게 만들어졌는지 확인
