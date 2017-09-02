import random
import math

class QLearn:
    def __init__(self, actions, temp=5,
                 epsilon=0.1, alpha=0.2, gamma=0.9):
        
        self.q = {}

        self.states = set()
        self.statesRE = {}
        self.aveSRE = 1.0

        self.temp = temp

        self.epsilon = epsilon  # exploration constant
        self.alpha = alpha  # discount constant
        self.gamma = gamma
        self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

    def learnQ(self, state, action, reward, value):
        '''
            Q-learning:
                Q(s, a) += alpha * (reward(s,a) + max(Q(s')) - Q(s,a))
        '''

        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)
        '''
            update Residual Entropy of this state (stateRE) and the
                   Average Residual Entropy of the agent (aveSRE)
            (optimized using dynamic programming (DP))

            Learning Residual Entropy, 'I(S)', for a state 'S':
                'I(S)' is defined as follows:
                    I(S) = - SUM( [ p(S, a) * log(p(S, a)) for all a in A] ) / log(|a|)
                where:
                    'A' is a set of actions possible in state 'S'
                    'a' is an action in set 'A'
                    'p(S, a)' is the probability of selecting action 'a' in state 'S'; and
                    '|a|' is the number of possible actions

                In an unlearned case:
                    p(S, a) = p(S, a1) = p(S, a2) = p(S, a3) = ...
                    p(S, a) = 1 / |a|
                    SUM( p(S, a) * log(p(S, a)) ) = |a| * (1 / |a|) * log(1 / |a|)
                                                  = - log(|a|); therefore,
                    I(S) = log(|a|) / log(|a|) = 1

                In a fully learned case:
                    p(S, a) = 1;
                    SUM( p(S, a) * log(p(S, a)) ) = SUM( 1 * log(1) )
                                                  = SUM( 1 * 0 )
                                                  = 0; therefore,
                    I(S) = 0.0 / log(|a|) = 0

                unlearned                                   fully learned
                    1  >----------------------------------------> 0

            Average of 'I(S)', 'I', in episode 'E':
                'I' is defined as follows:
                    I = SUM( [ I(S) for all S in E ] ) / |E|
                where:
                    '|E|' is the number of states included in 'E'

            In this implementation:
                stateRE[S] := I(S)
                aveSRE     := I

            Sources:
                "Automatic Adaptive Space Segmentation for Reinforcement Learning"
                    Komori, Y., Notsu, A., Honda, K., & Ichihashi, H.
                "Speeding up Multi-Agent Reinforcement Learning Coarse-
                Graining of Perception Hunter Game as an Example"
                    Ito, A. & Kanabuchi, M.
        '''
        
        if state in self.states:
            eprobs = self.getEProbs(state)
            newSRE = -sum(
                [eprob * math.log10(eprob) for eprob in eprobs]) \
                / math.log10(len(self.actions)
            )
            delta = newSRE - self.statesRE[state]

            self.statesRE[state] = newSRE
            self.aveSRE += delta / len(self.states)
        else:
            self.states.add(state)

            eValue = math.exp(reward / self.temp)
            eSum = len(self.actions) - 1 + eValue
            eX = eValue / eSum  # eprob when Q(S,a) == reward
            e1 = 1 / eSum  # eprob when Q(S,a) == 0

            self.statesRE[state] = \
                - ((len(self.actions) - 1) * (e1 * math.log10(e1)) \
                + (eX * math.log10(eX))) / math.log10(len(self.actions))
            self.aveSRE = (self.aveSRE * (len(self.states) - 1) \
                        + self.statesRE[state]) / len(self.states)

    def chooseAction(self, state, type=1):
        # Greedy Epsilon
        if type == 0:
            action = 0
            if random.random() < self.epsilon:
                action = random.choice(self.actions)
            else:
                q = [self.getQ(state, a) for a in self.actions]
                maxQ = max(q)

                # In case there're several state-action max values
                # we select a random one among them
                maxCount = q.count(maxQ)
                if maxCount > 1:
                    best = [
                        i for i in range(len(self.actions)) 
                        if q[i] == maxQ
                    ]
                    i = random.choice(best)
                else:
                    i = q.index(maxQ)
            return action

        # Boltzmann
        elif type == 1:
            eprobs = self.getEProbs(state, ignore_walls=True)

            ran = random.random()
            #print(eprobs, ran)

            for a in self.actions:
                if ran > eprobs[a]:
                    ran -= eprobs[a]
                else:
                    action = a
                    break

            # print(action, eprobs[a])
            return action

        # Mod Random
        elif type == 2:
            q = [self.getQ(state, a) for a in self.actions]
            maxQ = max(q)

            if random.random() < self.epsilon:
                # action = random.choice(self.actions)
                minQ = min(q)
                mag = max(abs(minQ), abs(maxQ))
                # add random values to all action, recalculate maxQ
                q = [
                    q[i] + random.random() * mag - 0.5 * mag
                    for i in range(len(self.actions))
                ]
                maxQ = max(q)

            # In case there're several state-action max values
            # we select a random one among them
            count = q.count(maxQ)
            if count > 1:
                best = [ 
                    i for i in range(len(self.actions)) 
                    if q[i] == maxQ
                ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
            return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, \
                    reward + self.gamma * maxqnew)

    '''
        return the probabilities of selecting each action
        using the boltzmann distribution:

        eValue(state, action) = e ^ (Q(state, action) / temp)

                               eValue(state, action)
        eProb(state, action) = ---------------------
                               (sum of all eValues)
    '''
    
    def is_wall(self, action):
        cell = self.agent.world.getPointInDirection(self.agent.cell.x, self.agent.cell.y, action)
        return self.agent.world.get_cell(cell[0], cell[1]).wall
        
    def getEProbs(self, state, ignore_walls=False):
        eValues = []
        for action in self.actions:
            if ignore_walls and self.is_wall(action):
                eValues.append(0)
            else:
                eValues.append(math.exp(self.getQ(state, action) / self.temp)) 
        total = sum(eValues)
        return [eValue / total for eValue in eValues]


def ff(f, n):
    fs = "{:f}".format(f)
    if len(fs) < n:
        return ("{:" + n + "s}").format(fs)
    else:
        return fs[:n]
