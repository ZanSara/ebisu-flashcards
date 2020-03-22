from typing import Union, Mapping

import csv
from collections import OrderedDict
from datetime import datetime, timedelta
import ebisu


HALF_LIFE_UNIT = timedelta(hours=1)


class CardModel:

    def __init__(self, alpha: float=3.0, beta: float=3.0, half_life: Union[float, timedelta] = 1.0, last_review: Union[str, datetime]=None):
        self.alpha: float = float(alpha)
        self.beta: float = float(beta)
        
        if isinstance(half_life, timedelta):
            self.half_life: float = half_life / HALF_LIFE_UNIT
        else:
            self.half_life: float = float(half_life)

        if isinstance(last_review, datetime):
            self.last_review: str = last_review.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.last_review: str = last_review or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return "CardModel object (a:{} b:{} half_life:{} last_review:{})".format(self.alpha, self.beta, self.half_life, self.last_review) 

    def last_review_as_time(self):
        return datetime.strptime(self.last_review, "%Y-%m-%d %H:%M:%S")

    def to_ebisu_model(self):
        return (self.alpha, self.beta, self.half_life*HALF_LIFE_UNIT)


class Card:

    def __init__(self, row: OrderedDict):
        self.id: int = int(row["id"])
        self.question: str = row["question"]
        self.answer: str = row["answer"]
        self.successful_reviews: int = 0
        self.versions: List[CardModel] = [CardModel(row["alpha"], row["beta"], row["half_life"], row["last_review"])]

    def __repr__(self):
        return "Card object (id:{} - question:{} - answer:{} - versions:{})".format(self.id, self.question, self.answer, len(self.versions)) 

    def store_test_result(self, test_result) -> None:
        previous_model = self.versions[-1]
        time_from_last_review = datetime.now() - previous_model.last_review_as_time()
        reviews_in_this_session = len(self.versions)
        self.successful_reviews += int(test_result)

        try:
            alpha, beta, half_life = ebisu.updateRecall(prior=previous_model.to_ebisu_model(), 
                                                        successes=test_result, 
                                                        total=reviews_in_this_session, 
                                                        tnow=time_from_last_review)
        except AssertionError as ae:
            print("Card was not updated: Failed too many times!")

        new_version = CardModel(alpha, beta, half_life, datetime.now())
        self.versions.append(new_version)  
        print("Card n.", self.id, " - new version: ", new_version)      
        return

    def recall_probability(self) -> float:
        card_model = self.versions[-1]
        time_from_last_review = datetime.now() - card_model.last_review_as_time()
         # The exact flag normalizes the output to a real probability. Useful for debugging but not in production.
        recall_probability = ebisu.predictRecall(prior=card_model.to_ebisu_model(), 
                                                 tnow=time_from_last_review, 
                                                 exact=True)
        print("Card n.", self.id, " - recall prob: {:.2f}".format(recall_probability*100))
        return recall_probability

    def amend_last_update(self, new_test_result) -> None:
        self.versions = self.versions[-1]  # Delete version to amend
        self.store_test_result(new_test_result)  # Recompute and store the new result

    def to_dict(self) -> Mapping[str, str]:
        last_version = self.versions[-1]
        dic = {}
        dic["id"] = str(self.id)
        dic["question"] = self.question
        dic["answer"] = self.answer
        dic["alpha"] = str(last_version.alpha)
        dic["beta"] = str(last_version.beta)
        dic["half_life"] = str(last_version.half_life)
        dic["last_review"] = last_version.last_review
        return dic


class Deck:

    def __init__(self, name):
        self.name: str = name
        self.cards: Mapping[int, Card] = None
        self.cards_studied_count: int = 0
        self.card_being_tested: Card = None
        self.last_reviewed_card: Card = None
        self.load()

    def __repr__(self):
        return "Deck object (name:{} - n. cards:{})".format(self.name, len(self.cards)) 

    def load(self) -> None:
        with open('{}.csv'.format(self.name)) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            self.cards = [Card(row) for row in reader]
        print("Loaded cards: ", self.cards)

    def save(self) -> None:
        if len(self.cards) < 1:
            print("Not saving: there are no cards in the deck.")
            return

        self.cards = sorted(self.cards, key=lambda card: card.id )
        with open('{}.csv'.format(self.name), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=self.cards[0].to_dict().keys())
            writer.writeheader()
            for card in self.cards:
                writer.writerow(card.to_dict())
                print("Writing ", card.to_dict())

    def next_card_to_review(self) -> int:
        self.cards = sorted(self.cards, key=lambda card: card.recall_probability() )

        self.last_reviewed_card = self.card_being_tested
        self.card_being_tested = self.cards[0]
        self.cards_studied_count += 1
        return self.card_being_tested

    def last_reviewed_card(self) -> int:
        return self.last_reviewed_card