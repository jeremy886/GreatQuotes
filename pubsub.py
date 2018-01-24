"""Simple message publisher/subscriber service


    Data structure deque() is preferred over list() because it supports appendleft()

    defaultdict() with deque() simplifies per-user accumulation of posts


    Features:
    * Users make posts
    * Let one user follow another
    * Followers subscribe to the posts they are interested in.
    * Newer posts are more relevant.
    * Display posts by a user, posts for a user, or posts matching a search request.
    * Display followers of a user.
    * Display those followed by a user.
    * Store the user account information with hashed passwords.

    Features:
    * Move data models to databases

"""
import sys
assert sys.version_info[:3] >= (3, 6, 1), 'Requires Python 3.6.1 or late'


import hashlib
import random
import secrets
from bisect import bisect
from heapq import merge
from itertools import islice
from typing import NamedTuple, Deque, DefaultDict, Set, Optional, List, Tuple, Dict
from collections import deque, defaultdict
import time
from sys import intern


User = str
Timestamp = Optional[float]
HashAndSalt = Tuple[bytes, bytes]


class Post(NamedTuple):
    """using typing module

        without typing module:
        Post = namedtuple('Post', ['timestamp', 'user', 'text']) # use collection.namedtuple
    """
    timestamp: Timestamp
    user: User
    text: str


class UserInfo(NamedTuple):
    displayname: str
    email: str
    hashed_password: HashAndSalt
    bio: str
    photo: str


posts: Deque[Post] = deque()  # Posts from newest to oldest
user_posts: DefaultDict[User, Deque] = defaultdict(deque)  # accumulate data
following: DefaultDict[User, Set[User]] = defaultdict(set)
followers: DefaultDict[User, Set[User]] = defaultdict(set)
user_info: Dict[User, UserInfo] = {}


def post_message(user: User, text: str, timestamp: Timestamp=None) -> None:
    user = intern(user)
    timestamp = timestamp or time.time()  # short-circuiting
    post = Post(timestamp, user, text)
    posts.appendleft(post)
    user_posts[user].appendleft(post)


def follow(user: User, followed_user: User) -> None:
    user, followed_user = intern(user), intern(followed_user)
    following[user].add(followed_user)
    followers[followed_user].add(user)


def posts_by_user(user: User, limit: Optional[int] = None) -> List[Post]:
    return list(islice(user_posts[user], limit))


def posts_for_user(user: User, limit: Optional[int] = None) -> List[Post]:
    relevant = merge(*[user_posts[followed_user] for followed_user in following[user]], reverse=True)
    return list(islice(relevant, limit))


def search(phrase: str, limit: Optional[int]=None) -> List[Post]:
    """
    Todo ideas:

    add pre-indexing to speed-up search
    add time sensitive caching of search
    """
    return list(islice((post for post in posts if phrase in post.text), limit))  # generator


def hash_password(password: str, salt: Optional[bytes] = None) -> HashAndSalt:
    pepper = b'we do not see things as they are we see them as we are'
    salt = salt or secrets.token_bytes(16)
    salted_pass = salt + password.encode('utf-8')
    return hashlib.pbkdf2_hmac('sha512', salted_pass, pepper, 100000), salt


def set_user(user: User, displayname: str, email: str, password: str, bio: Optional[str] = None,
             photo: Optional[str] = None) -> None:
    user = intern(user)
    hashed_password = hash_password(password)
    user_info[user] = UserInfo(displayname, email, hashed_password, bio, photo)


def check_user(user: User, password: str) -> bool:
    hashpass, salt = user_info[user].hashed_password
    target_hash_pass = hash_password(password, salt)[0]
    time.sleep(random.expovariate(10))
    return secrets.compare_digest(hashpass, target_hash_pass)


def get_user(user: User) -> UserInfo:
    return user_info[user]


time_unit_cuts: List[int] = [60, 3600, 3600*24]
time_units: List[Tuple[int, str]] = [(1, 'second'), (60, 'minute'), (3600, 'hour'), (3600*24, 'day')]


def age(post: Post) -> str:
    seconds = time.time() - post.timestamp
    divisor, unit = time_units[bisect(time_unit_cuts, seconds)]
    units = seconds // divisor
    return '%d %s' % (units, unit + ('' if units == 1 else 's'))
