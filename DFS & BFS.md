DFS & BFS

어떤 식으로 탐색을 수행할 수 있는지 코드 자체가 정형화 되어 있으니 코드를 외우고 있는 것이 중요하다. 파이썬에서 구현하기 위해서는 큐를 구현해야 함. deque를 사용

visited 리스트를 사용하여 방문한 노드는 다시 방문하지 않도록 구현

 DFS

​	이론적으로는 stack을 사용해서 구현 / but 실제로는 재귀 함수를 이용해서 간단하게 구현

```python
def dfs(v):
    print(v, end=" ")
    visited[v]= True
    for i in adj[v]:
        if not visited[i]:
            dfs(i)
```

​	DFS를 재귀 형태로 구현을 해 보았다. 시작 노드 v를 입력받아 v부터 재귀적으로 방문을 하지 않은 	노드를 탐색한다.

BFS

​	deque를 사용해서 구현 / deque는 double-ended queue의 줄임말로, 양방향에서 데이터를 처리할 	수 있는 queue 자료 구조

​	반복문을 통해서 구현

```python
def bfs(v):
    q= deque([v])

    while q:
        v= q.popleft()
        if not visited[v]:
            visited[v]= True
            print(v, end=" ")
            for i in adj[v]:
                if not visited[i]:
                    q.append(i)
```

deque를 선언해서 queue에서 맨 앞에 있는 원소를 pop해서 v에 넣어주고 방문하지 않았다면 방문했다고 변경을 해 준 뒤 이 정점과 연결되어 있는 정점들을 순차적으로 queue에 넣어준다. 이를  queue가 비어 있을 때까지 반복을 한다.





 