# humancoin_chat
humancoin chat


- 参考： https://github.com/limboy/chat/blob/master/src/app.py

## 系统设计
- 基于redis的有序集合(sorted set)实现
- 聊天室key:  room_id
  - value:  json字符串
    - 用户id
    - 消息内容
    - 创建时间: 时间戳
    - 消息序号: 基于聊天室的 `incr roomid_key`
  - score: 时间戳
- 如何匹配？
    > https://blog.51cto.com/u_16175451/7248859
  - 使用无需集合作为`匹配队列`存储待匹配的 `人类用户`
  - 匹配的时候, 在程序中 生成 `1~100`的随机数`x`:
    - 如果`x < 5`, 即 `5%`的概率匹配到人类:
      - 把该用户加入匹配队列: `SADD key member`
      - 如果上面的`匹配队列中`的人类用户数大于 `>= 1` :
        - 随机取出`1`个人 : `SPOP key`
      - 否则, 轮询`匹配队列`的数量`10s`, 如果还没有人类用户，则匹配失败, 需要用户重新匹配
    - 如果 `x >= 5`, 那么则匹配AI:
      - 休眠5s
      - 匹配一个AI机器人
  - 如何增加随机性?
    - 使用无序集合的 `SRANDMEMBER key [count]`

- 如果区分聊天是`人类vs人类`还是`人类vsAI`？
  - 在redis的key加以标识？
  - 在消息json中的user加以标识

- 如何指定谁先发消息？
  - 使用概率， 0.5的概率 ， 从[0, 1] 随机取一个数，作为数组索引，
  - 如果是AI先开始，如何让AI主动问问题？
    - 让AI主动问一个问题
    - 从数据库中随机抽取一个问题，作为AI的发起问题

- 如何判断胜负？
  - 可以提前结束游戏
  - 通过接口  `/finishgame` 来结束游戏
    - 参数 `human`:
      - `0`: 不是人类
      - `1`: 是人类


## 接口设计

- 开始匹配 `/startChat`
  - `POST`
  - 请求参数:
    - user_id
  - 响应参数:
    - user_id
    - room_id
    - first
- 向聊天室发送消息 `/sendChatMsg`
  - `POST`
  - 请求参数:
    - user_id
    - room_id
    - msg
  - 响应参数：
    - user_id
    - room_id
    - msg_id
- 获取聊天记录 `/queryChat`
  - `POST`
  - 请求参数:
    - room_id
    - user_id
  - 响应参数:
    - room_id
    - msgs
    - create_timestamp
    - finish_timestamp
- 结束聊天 `/finishChat`
  - `POST`
  - 请求参数：
    - room_id
    - human
  - 响应参数：
    - win
    - points