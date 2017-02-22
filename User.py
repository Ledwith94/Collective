#!/usr/bin/python
from Movie import Movie

class User(object):
    usercount = 0

    def __init__(self, num):
        self.user_id = num
        self.rating_dic = {}
        self.num_rating = 0
        self.highest_rating = 0
        User.usercount += 1
        self.neighbors = {}
        self.mean_item = {}

    def add_rating(self, movie, rating):
        self.rating_dic[movie] = rating
        self.num_rating += 1
        if rating > self.highest_rating:
            self.highest_rating = rating

    def get_rating_for(self, movie):
        return self.rating_dic.get(movie)

    def get_rating_count(self):
        return self.num_rating

    def get_highest_rating(self):
        return self.num_rating

    def has_rating_for(self, movie):
        return self.rating_dic.has_key(movie)

    def set_mean_item(self,key, val):
        self.mean_item[key] = val

    def add_neighbor(self, key, val):
        self.neighbors[key] = val

    def has_neighbor(self, user):
        return self.neighbors.has_key(user)
