import logging
import calendar
from datetime import datetime, timedelta
from enum import Enum

from pymongo import MongoClient
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from config import settings


class TimePeriod(str, Enum):
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"


class DataBase:
    def __init__(
        self,
        database_name: str,
        collection_name: str,
    ) -> None:
        self.db_name: str = database_name
        self.coll_name: str = collection_name
        self.coll: Collection | None = None
        self.__connect()  # connect to MongoDB and init collection

    def get_statistic_data(
        self,
        dt_from: datetime,
        dt_upto: datetime,
        group_type: str,
    ) -> dict[str, list]:

        assert self.coll is not None

        group_types = {
            TimePeriod.HOUR: "%Y-%m-%dT%H",
            TimePeriod.DAY: "%Y-%m-%d",
            TimePeriod.MONTH: "%Y-%m",
        }

        dt_format = group_types[group_type]

        query = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": dt_format, "date": "$dt"}},
                    "period_sum": {"$sum": "$value"},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        cursor = self.coll.aggregate(query)

        labels = []
        data = []

        iso_types = {
            TimePeriod.HOUR: ":00:00",
            TimePeriod.DAY: "T00:00:00",
            TimePeriod.MONTH: "-01T00:00:00",
        }

        iso_format = iso_types[group_type]

        for doc in cursor:
            dt_raw = datetime.fromisoformat(doc["_id"] + iso_format)
            dt_iso = datetime.isoformat(dt_raw)
            labels.append(dt_iso)
            data.append(doc["period_sum"])

        result_data = []
        result_labels = []

        current_date = dt_from

        while current_date <= dt_upto:

            if group_type == TimePeriod.HOUR:
                delta = timedelta(hours=1)
            elif group_type == TimePeriod.DAY:
                delta = timedelta(days=1)
            else:  # TimePeriod.MONTH:
                _, days_in_month = calendar.monthrange(
                    current_date.year, current_date.month
                )
                delta = timedelta(days=days_in_month)

            result_labels.append(datetime.isoformat(current_date))

            if datetime.isoformat(current_date) not in labels:
                result_data.append(0)
            else:
                value_index = labels.index(datetime.isoformat(current_date))
                result_data.append(data[value_index])

            current_date += delta

        return {"dataset": result_data, "labels": result_labels}

    def __connect(self) -> None:
        try:
            mongo_client: MongoClient = MongoClient(
                host=settings.MONGO_HOST,
                port=settings.MONGO_PORT,
                username=settings.MONGO_USER,
                password=settings.MONGO_PASS,
            )
            if mongo_client.list_databases():
                mongo_client = mongo_client[self.db_name]
                self.coll = mongo_client[self.coll_name]
        except errors.ServerSelectionTimeoutError:
            logging.error("Failed to Connect DB")
        except errors.ConnectionFailure:
            logging.error("Connection Failure")
        except errors.ConfigurationError:
            logging.error("Configurarion Error")
