import datetime


def timestamptoDateConverter(timestampValue: str) -> datetime.datetime:
    """
    Converts input timestamp to date-teime
    """
    epochStartingPoint = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestampValue))
    return (epochStartingPoint + delta).replace(tzinfo=datetime.timezone.utc).astimezone()
