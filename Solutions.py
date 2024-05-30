import heapq
from Node import Node
from collections import deque

class Solutions:
    
    @staticmethod
    def a_star_search(initial_state, goal_state):
        def manhattan_distance(state, goal):
            distance = 0
            for i in range(3):
                for j in range(3):
                    if state[i][j] != 0:
                        x, y = divmod(state[i][j] - 1, 3)
                        distance += abs(x - i) + abs(y - j)
            return distance

        def get_neighbors(state):
            neighbors = []
            size = len(state)
            zero_pos = next((i, j) for i in range(size) for j in range(size) if state[i][j] == 0)
            x, y = zero_pos
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    new_state = [row[:] for row in state]
                    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                    neighbors.append(Node(state=new_state, parent=None, action=(x, y, nx, ny), cost=0))
            return neighbors

        start_node = Node(state=initial_state, cost=0, heuristic=manhattan_distance(initial_state, goal_state))
        frontier = deque([(start_node.heuristic, start_node)])
        explored = set()

        iterations = 0
        print()
        print('ITERATIONS')
        while frontier:
            iterations += 1
            frontier = deque(sorted(frontier, key=lambda x: x[0]))  # sort to simulate priority queue
            _, current_node = frontier.popleft()
            if current_node.state == goal_state:
                print("Goal reached!")
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent
                return path[::-1], iterations

            explored.add(tuple(map(tuple, current_node.state)))
            neighbors = get_neighbors(current_node.state)
            
            for neighbor in neighbors:
                neighbor.parent = current_node
                neighbor.cost = current_node.cost + 1
                neighbor.heuristic = manhattan_distance(neighbor.state, goal_state)
                total_cost = neighbor.cost + neighbor.heuristic

                if tuple(map(tuple, neighbor.state)) not in explored:
                    frontier.append((total_cost, neighbor))

            open_nodes = [node for _, node in frontier]
            closed_nodes = list(explored)

            
            print()
            print(f"Iteration {iterations}:")
            rows = "\n".join(str(row) for row in current_node.state)
            print(f"Current state:\n{rows}")
            print(f"Cost: {current_node.cost}, Heuristic: {current_node.heuristic}")
            print(f"Open nodes: {len(open_nodes)}, Closed nodes: {len(closed_nodes)}")

        print("No solution found.")
        return None, iterations
    
    @staticmethod
    def beam_search(initial_state, goal_state, beam_width=2):
        def manhattan_distance(state, goal):
            distance = 0
            for i in range(3):
                for j in range(3):
                    if state[i][j] != 0:
                        x, y = divmod(state[i][j] - 1, 3)
                        distance += abs(x - i) + abs(y - j)
            return distance

        def get_neighbors(state):
            neighbors = []
            size = len(state)
            zero_pos = next((i, j) for i in range(size) for j in range(size) if state[i][j] == 0)
            x, y = zero_pos
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    new_state = [row[:] for row in state]
                    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                    neighbors.append(Node(state=new_state, parent=None, action=(x, y, nx, ny), cost=0))
            return neighbors

        current_node = Node(state=initial_state, cost=0, heuristic=manhattan_distance(initial_state, goal_state))
        open_list = deque([(current_node.heuristic, current_node)])
        closed_set = set()

        iterations = 0
        print()
        print('ITERATIONS')
        while open_list:
            iterations += 1
            open_list = deque(sorted(open_list, key=lambda x: x[0]))  # sort to simulate priority queue
            open_list = deque(list(open_list)[:beam_width])

            new_open_list = deque()
            for _, current_node in open_list:
                if current_node.state == goal_state:
                    path = []
                    while current_node:
                        path.append(current_node)
                        current_node = current_node.parent
                    return path[::-1], iterations

                closed_set.add(tuple(map(tuple, current_node.state)))

                neighbors = get_neighbors(current_node.state)
                for neighbor in neighbors:
                    if tuple(map(tuple, neighbor.state)) not in closed_set:
                        neighbor.parent = current_node
                        neighbor.heuristic = manhattan_distance(neighbor.state, goal_state)
                        new_open_list.append((neighbor.heuristic, neighbor))

            if not new_open_list:
                break
            open_list = new_open_list
            
            print()
            print(f"Iteration {iterations}:")
            rows = "\n".join(str(row) for row in current_node.state)
            print(f"Current state:\n{rows}")
            print(f"Cost: {current_node.cost}, Heuristic: {current_node.heuristic}")
            print(f"Open nodes: {len(open_list)}, Closed nodes: {len(closed_set)}")

        return None, iterations
    
    @staticmethod
    def best_first_search(initial_state, goal_state):
        def manhattan_distance(state, goal):
            distance = 0
            for i in range(3):
                for j in range(3):
                    if state[i][j] != 0:
                        x, y = divmod(state[i][j] - 1, 3)
                        distance += abs(x - i) + abs(y - j)
            return distance

        def get_neighbors(state):
            neighbors = []
            size = len(state)
            zero_pos = next((i, j) for i in range(size) for j in range(size) if state[i][j] == 0)
            x, y = zero_pos
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    new_state = [row[:] for row in state]
                    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                    neighbors.append(Node(state=new_state, parent=None, action=(x, y, nx, ny), cost=0))
            return neighbors

        current_node = Node(state=initial_state, cost=0, heuristic=manhattan_distance(initial_state, goal_state))
        open_list = deque([(current_node.heuristic, current_node)])
        closed_set = set()

        iterations = 0
        print()
        print('ITERATIONS')
        while open_list:
            iterations += 1
            open_list = deque(sorted(open_list, key=lambda x: x[0]))  # sort to simulate priority queue
            _, current_node = open_list.popleft()

            if current_node.state == goal_state:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent
                return path[::-1], iterations

            closed_set.add(tuple(map(tuple, current_node.state)))

            neighbors = get_neighbors(current_node.state)
            for neighbor in neighbors:
                if tuple(map(tuple, neighbor.state)) not in closed_set:
                    neighbor.parent = current_node
                    neighbor.heuristic = manhattan_distance(neighbor.state, goal_state)
                    open_list.append((neighbor.heuristic, neighbor))
                    
            print()
            print(f"Iteration {iterations}:")
            rows = "\n".join(str(row) for row in current_node.state)
            print(f"Current state:\n{rows}")
            print(f"Cost: {current_node.cost}, Heuristic: {current_node.heuristic}")
            print(f"Open nodes: {len(open_list)}, Closed nodes: {len(closed_set)}")

        return None, iterations