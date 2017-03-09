#!/usr/bin/python
from math import*


class User(object):
    usercount = 0

    def __init__(self, num):
        self.user_id = num
        self.rating_dic = {}
        self.num_rating = 0
        self.mean_rating = 0
        self.highest_rating = 0
        User.usercount += 1
        self.neighbours = {}
        self.mean_item = {}
        self.n_mean_item = {}

    def add_rating(self, movie, rating):
        self.rating_dic[movie] = rating
        self.num_rating += 1
        if rating > self.highest_rating:
            self.highest_rating = rating

    def get_mean_rating(self):

        return self.mean_rating

    def get_median(self):
        median_list = self.rating_dic.values()
        median_list.sort()
        if (len(median_list)/2) % 2 == 0:
            return median_list[(len(median_list)/2)]
        else:
            self.median = median_list[int(len(median_list)/2)]
            return self.median

    def set_mean_rating(self):
        add = sum(self.rating_dic.values())
        self.mean_rating = add/self.num_rating

    def get_rating_for(self, movie):
        return self.rating_dic.get(movie)

    def get_rating_count(self):
        return self.num_rating

    def get_highest_rating(self):
        return self.num_rating

    def has_rating_for(self, movie):
        if movie in self.rating_dic:
            return True
        else:
            return False

    def set_mean_item(self, key, val):
        self.mean_item[key] = val

    def get_deviation_rating(self):
        sqErr = 0
        for r in self.rating_dic.values():
            sqErr += (self.mean_rating - r) * (self.mean_rating - r)
        return sqrt(sqErr) / (self.num_rating - 1)

    def add_neighbour(self, val):
        for x in val:
            self.neighbours[x[0]] = x[1]

    def has_neighbour(self, user):
        if user in self.neighbours:
            return True
        else:
            return False

    def get_common_movies(self, user):
        group = []
        for r in self.rating_dic.keys():
            if user.has_rating_for(r):
                group.append(r)
        return group

    def small_value(self):
        small_val = self.neighbours.values()[0]
        small_key = None
        for key, val in self.neighbours.items():
            if val <= small_val:
                small_val = val
                small_key = key
        return small_key