#!/usr/bin/python
import random


class Movie(object):
    moviecount = 0

    def __init__(self, movie):
        self.name = movie
        self.ratings = {}
        self.mean = 0
        self.median = 0
        self.mode = None
        self.lowest_rating = None
        self.highest_rating = None
        Movie.moviecount += 1

    def add_rating(self, user, rating):
        self.ratings[user] = rating
        if rating > self.highest_rating or self.highest_rating is None:
            self.highest_rating = rating
        if rating < self.lowest_rating or self.lowest_rating is None:
            self.lowest_rating = rating

    def get_rating(self):
        return self.ratings

    def get_mean(self):
        for val in self.ratings.values():
            self.mean += int(val)
        self.mean /= len(self.ratings)
        return self.mean

    def rating_count(self):
        return len(self.get_rating())

    def get_median(self):
        median_list = self.ratings.values()
        median_list.sort()
        if (len(median_list)/2) % 2 == 0:
            return median_list[(len(median_list)/2)]
        else:
            self.median = median_list[(len(median_list)/2)+0.5] + median_list[(len(median_list)/2)-0.5]
            return self.median

    def get_mode(self):
        for i in range(1, 5):
            if self.get_rating_group(i) > self.mode:
                self.mode = self.get_rating_group(i)
            elif self.get_rating_group(i) == self.mode:
                self.mode = None
        return self.mode

    def get_rating_group(self, rating):
        if 0 > rating > 5:
            return "Rating between 1 and 5"
        i = 0
        for key, val in self.ratings.items():
            if val == rating:
                i += 1
        return i

    def mean_item_rating(self):
        return random.choice(self.ratings.keys())
