import _pickle
import logging

dudes = []  # list of dudes
pickle_path = './persistence/dudes.pk'

prs_logger = logging.getLogger("wednesday.persistence")
prs_logger.setLevel(logging.INFO)


def load_dudes():
    """
    Loads user ids from the serialized dudes.pk file into dudes
    """
    try:
        with open(pickle_path, 'rb') as f:
            global dudes
            dudes = _pickle.load(f)
            prs_logger.info("Pickle loaded dudes.pk")
    except EOFError:
        prs_logger.warning("pickle.load failed")


def is_dude(uid):
    """
    Checks if a user id exists in dudes
    If not, adds it
    :param uid: Id to look for
    :return: True if exists, False if added
    """
    if uid in dudes:
        return True  # was already a dude
    else:
        dudes.append(uid)
        dump()
        prs_logger.info("Added " + str(uid) + " to dudes.pk")
        return False  # is now a dude


def un_dude(uid):
    """
    removes a dude
    :param uid: no longer our dude
    """
    if uid in dudes:
        dudes.remove(uid)
        prs_logger.info("Removed " + str(uid) + " from dudes.pk")
    else:
        prs_logger.info(str(uid) + "? This guy was NEVER a dude")
    dump()


def dump():
    with open(pickle_path, 'wb') as f:
        _pickle.dump(dudes, f)
