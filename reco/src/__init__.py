from reco.src.base import Recommender
from reco.src.heuristic import HeuristicRecommender


def get_recommender(reco_type: str = "heuristic") -> Recommender:
    """
    Factory method to get the requested recommender.
    """
    return HeuristicRecommender()
