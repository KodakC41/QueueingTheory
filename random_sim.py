import order
import barista
import patron


def Random_simulation(K, rounds, div, stopGenAt, howMantToGenEachRound, cost, realloc,queue_active,use_beta,beta) -> None:
    x = 0
    N = []
    if use_beta == True and queue_active == True:
        howMantToGenEachRound += beta
    if not realloc:
        while x <= rounds:
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genPatronsRandom(
                        div, howMantToGenEachRound, i, x, cost,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N, K):
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
    if realloc:
        while x < rounds:
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genPatronsRandom(
                        div, howMantToGenEachRound, i, x, cost,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x) == True:
                        n.setBeingServed(True)
        while has_unserved_patron(N):
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x) == True:
                        n.setBeingServed(True)