from collections import defaultdict, Counter

from airflow.models import BaseOperator

from airflowbook.hooks.MovielensHook import MovielensHook


class MovielensPopularityOperator(BaseOperator):
    def __init__(
            self,
            conn_id,
            start_date,
            end_date,
            min_ratings=4,
            top_n=5,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date
        self._min_ratings = min_ratings
        self._top_n = top_n

    def execute(self, context):
        rating_sums = defaultdict(Counter)
        averages = defaultdict(float)
        mlh = MovielensHook(conn_id=self._conn_id)
        ratings = mlh.get_ratings(start_date=self._start_date, end_date=self._end_date)

        for rating in ratings:
            mid = rating["movieId"]
            mrating = rating["rating"]
            rating_sums[mid].update(
                count=1,
                rating=mrating
            )
        for movie_id, rating_sum in rating_sums.items():
            rsr = rating_sum["rating"]
            rsc = rating_sum["count"]
            if rsc >= self._min_ratings:
                ratio = rsr / rsc
                averages[movie_id] = ratio
        result = sorted(averages.items(), key=lambda x: averages.get(x), reverse=True)[: self._top_n]
        return result
