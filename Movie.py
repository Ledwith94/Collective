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

    def add_rating(self, user, rating): #adds a user-rating pair to the ratings dictionary
        self.ratings[user] = rating
        if rating > self.highest_rating or self.highest_rating is None:
            self.highest_rating = rating
        if rating < self.lowest_rating or self.lowest_rating is None:
            self.lowest_rating = rating

    def get_rating(self): #returns all ratings
        return self.ratings

    def get_mean(self): #gets the mean rating over all ratings for the given item
        for val in self.ratings.values():
            self.mean += int(val)
        self.mean /= len(self.ratings)
        return self.mean

    def rating_count(self): #counts all ratings given to the item
        return len(self.ratings)

    def get_median(self): #gets the median rating over all ratings for the given item
        median_list = self.ratings.values()
        median_list.sort()
        if (len(median_list)/2) % 2 == 0:
            return median_list[(len(median_list)/2)]
        else:
            self.median = median_list[(len(median_list)/2)+0.5] + median_list[(len(median_list)/2)-0.5]
            return self.median

    def get_mode(self): #gets the mode of ratings over all ratings for the given item
        for i in range(1, 5):
            if self.get_rating_group(i) > self.mode:
                self.mode = self.get_rating_group(i)
            elif self.get_rating_group(i) == self.mode:
                self.mode = None
        return self.mode

    def get_rating_group(self, rating): #returns number of times item is given a rating
        if 0 > rating > 5:
            return "Rating between 1 and 5"
        i = 0
        for key, val in self.ratings.items():
            if val == rating:
                i += 1
        return i
