

class Vote:

    def __init__(self, ranks):
          # candidate index, vote order
        self._rank = {}
        for n, rank in enumerate(ranks): 
            try:
                self._rank[n] = int(rank)
            except ValueError:
                pass

    def candidate_rankings(self):
        return [xx[0] for xx in sorted(self._rank.items(), key=lambda x: x[1])]


class VoteTable:

    def __init__(self, vote_fn, candidates):
        self._candidates = candidates
        self._num_candidates = len(candidates)

        self._all_candidates = [n for n in range(self._num_candidates)]

        self._votes = []
        with open(vote_fn, 'r') as fid:
            lines = fid.readlines()

            self._num_voters = len(lines)

            for l in lines:
                self._votes.append(Vote(l.split('\t')))

    def vote(self):

        candidates = self._all_candidates  # will remove candidates as they show up in last place

        round = 1
        while True:
            votes = {c: 0 for c in candidates}
            for v in self._votes:
                for r in v.candidate_rankings():
                    if r in candidates:
                        votes[r] += 1
                        break

            print(f"Votes after round {round}", {self._candidates[c]: v for c, v in votes.items()})
            if max(votes.values()) > self._num_voters*.5:
                # we're done
                winner = next(c for c in candidates if votes[c] == max(votes.values()))
                return self._candidates[winner]
            else:
                # eliminate candidates with the least votes
                lowest_vote = min(votes.values())
                candidates = [c for c in candidates if votes[c] != lowest_vote]
                print("new candidates", [self._candidates[c] for c in candidates])
                if len(candidates) == 1:
                    # we're done
                    winner = self._candidates[candidates[0]]
                    return winner
                elif len(candidates) == 0:
                    # Also done, but with multiple winners
                    print("multiple winners")
                    return [self._candidates[c] for c in votes.keys()]
            print()
            round += 1

        return None  # how'd we get here????

    def vote_multiple(self, num=8):
        results = []
        for _ in range(num):
            print("\n***** Vote iteration")
            winner = self.vote()
            self._all_candidates.remove(winner)
            results.append(winner)
        return results


if __name__ == '__main__':
    candidates = ['Joe', 'Fred', 'Frank']
    # Votes file formated as tab separated file.  Columns corrispond to the candidates (should be same length as candidate list). 
    # Rows corrispond to each vote submitted. 

    table = VoteTable('votes_sample.txt', candidates)
