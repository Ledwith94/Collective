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
        self.neighbours = {}

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

    def find_neighbours(self):
        for key, val in self.rating_dic.items():
            for users, rating in key.ratings.items():
                if self.neighbours.get(users) is None:
                    self.neighbours[users] = 0
                new_val = int(self.neighbours[users].get()) - val
                self.neighbours[users] = new_val
