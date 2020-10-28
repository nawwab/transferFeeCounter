import functools
import sys

#Program untuk mengkalkulasi cicilan dan mencari ongkos kirim paling minimum

class Node():
    def __init__(self, state, parent, action, distanceFromStart, distanceFromGoal):
        self.state = state
        self.parent = parent
        self.action = action
        self.distanceFromStart = distanceFromStart #g(n)
        self.distanceFromGoal = distanceFromGoal #h(n)
        self.calculatedDistance = self.distanceFromStart + self.distanceFromGoal

#A*ImplementationGoesHere
class AStarFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    #state represented as transferred money (int)
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("frontier kosong")
        else: #perbandingan g(n) + h(n) goes here
            chosen = functools.reduce(lambda a,b: a if a.calculatedDistance < b.calculatedDistance else b, self.frontier)

            for idx, node in enumerate(self.frontier):
                if node == chosen:
                    return self.frontier.pop(idx)

class problem():
    def __init__(self):
        print("=========== Program Minimal Biaya Transfer ==========")
        self.startingPoint = int(input("Masukkan biaya awal/biaya yang sudah dibayarkan (tanpa titik):Rp. "))
        self.goal = int(input("Masukkan harga yang akan dicicil (tanpa titik):Rp. "))
        self.transferCost = int(input("Masukkan ongkos untuk sekali kirim:Rp. "))
        print()

        self.actionCandidates = set()

        while(True):
            action = input("Masukkan nominal transaksi yang disanggupi (tekan enter untuk menyudahi): Rp.")

            if action == "":
                print("input disudahi.")
                break
            elif int(action) < 0:
                print("nilai cicilan invalid")
            elif int(action) >= self.goal:
                print("kenapa tidak bayar langsung tunai?")
            else:
                self.actionCandidates.add( int(action) )
    
    def neighbors(self, state): # state == transferred(int)
        candidate = []
        for action in self.actionCandidates:
            newAction = f"Rp.{action},00"
            newState = state + action
            candidate.append((newAction, newState))
        
        return candidate

    def solve(self):
        self.num_explored = 0
        self.exploredState = set()

        startNode = Node(self.startingPoint, None, None, 0, self.goal - self.startingPoint)
        frontier = AStarFrontier()
        frontier.add(startNode)

        while True:

            if frontier.empty():
                raise Exception("no solution")

            currentNode = frontier.remove()
            self.num_explored += 1
        
            if currentNode.state >= self.goal:
                excess = currentNode.state - self.goal
                actionsToGoal = []
                stateToGoal = []
                charges = []

                while currentNode.parent is not None:
                    actionsToGoal.append(currentNode.action)
                    stateToGoal.append(currentNode.state)
                    charges.append(currentNode.distanceFromStart)
                    currentNode = currentNode.parent
                
                actionsToGoal.reverse()
                stateToGoal.reverse()
                charges.reverse()
                self.solution = (actionsToGoal, stateToGoal, charges, excess if excess > 0 else 0)
                return
    
            self.exploredState.add(currentNode.state)

            for action, state in self.neighbors(currentNode.state):
                if not frontier.contains_state(state) and state not in self.exploredState:
                    child = Node(state, currentNode, action, currentNode.distanceFromStart + self.transferCost, self.goal - state)
                    frontier.add(child)
        
    def conclusions(self, detailedMode=False):
        if detailedMode:
            print()
            print("advanced mode on...")
            actions, states, charges, excess = self.solution

            for i, action in enumerate(actions):
                print(f"{i}.[+{action}, paid={states[i]}, charges={charges[i]}]")

            print(f"explored state = {self.num_explored}")
            print("advanced mode end...")
            print()

        print("Berikut kesimpulan kami untuk meminimalisir ongkos kirim:")
        print(f"anda bisa mengambil cicilan {len(actions)} kali ({actions[0]}/transaksi)")
        print(f"dengan total ongkos kirim = Rp.{charges[-1]},00")
        if excess > 0:
            print(f"kembalian di transaksi terakhir: Rp.{excess},00")


p = problem()
p.solve()
p.conclusions(True if sys.argv[1] == "-a" or sys.argv[1] == "--Advanced" else False)

    
