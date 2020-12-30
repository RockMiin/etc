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



++ 2020.12.30 추가

BFS 코드 구성할 시 주의할 점

BOJ 4963. 섬의 개수

```python
def bfs(v):

    q= deque([v])
    while q:
        x, y= q.popleft()
				# visited[x][y]= 1
        tmp= [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for tmp_x, tmp_y in tmp:
            dx, dy= x+tmp_x, y+tmp_y
            if 0<=dx<h and 0<=dy<w and arr[dx][dy] and not visited[dx][dy]:
                q.append([dx, dy])
                visited[dx][dy] = 1 # append를 할 때 방문 처리를 해줘야 중복이 발생 x
```

처음에 코드를 구성할 때 위에 주석을 단 것과 같이 q에서 pop을 할 때 방문 처리를 해주었더니 **시간 초과**가 발생하였다. 즉 불필요한 탐색을 한다는 의미였는데 append를 할 시에 방문 처리를 해주면 해결이 된다. 이유는 tmp 반복문을 돌 때 방문 처리를 해주지 않으면 q에서 pop되기 전에는 방문 처리가 되지 않으므로 중복된 x, y가 들어가기 때문이다. 

 