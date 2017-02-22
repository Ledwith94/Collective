#!/usr/bin/python
import argparse
import csv

import datetime
import heapq
import time
from User import User
from Movie import Movie
from Rating import Rating
from math import*


class Main:
    def __init__(self, file_name):
        self.users = {}
        self.movies = {}
        self.ratings = {}
        for x in range(1, 6):
            self.ratings[str(x)] = Rating(str(x))
        self.data_file = file_name

    def data(self):
        data_file = open(self.data_file, 'r')
        for line in data_file:
            user = str(line).split(',')[0]
            movie = str(line).split(',')[1]
            rating = str(line).split(',')[2]
            if self.users.get(user) is None:
                self.users[user] = User(user)
            if self.movies.get(movie) is None:
                self.movies[movie] = Movie(movie)
            self.ratings[rating].add_movie_to_user(movie, user)
            self.ratings[rating].add_user_to_movie(movie, user)
            self.movies[movie].add_rating(user, int(rating))
            self.users[user].add_rating(movie, int(rating))

    def mean_item_rating(self):
        for key, val in self.movies.items():
            add = sum(val.ratings.itervalues())
            mean = len(val.ratings)-1
            for user, obj in self.users.items():
                if mean == 0:
                    continue
                elif val.ratings.has_key(user):
                    sub = obj.get_rating_for(key)
                    add -= sub
                    obj.set_mean_item(key, float(add)/float(mean))
                    add += sub

    def coverage(self, outname):
        self.mean_item_rating()
        test_data = 0.0
        cant_test = 0.0
        rmse_list = []
        outfile = open(outname, 'w')
        outfile.write("user_id, item_id, Actual Rating, Predicted Rating, RMSE\n")
        wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        for user, obj in self.users.items():
            for movie, rating in obj.rating_dic.items():
                test_data += 1
                if obj.mean_item.get(movie) is None:
                    cant_test += 1
                else:
                    error = self.rmse(obj.mean_item.get(movie), rating, self.movies[movie].rating_count() - 1)
                    rmse_list.append(error)
                    wr.writerow([user, movie, rating, obj.mean_item.get(movie), error])
        full_err = 0
        for x in rmse_list:
            full_err += x
        percentage_covered = ((test_data - cant_test)/test_data) * 100.0
        print "Percentage Covered:" + str(percentage_covered)
        print "Average root mean squared error : " + str(full_err/len(rmse_list))

    def rmse(self, predictions, targets, mean):
            differences = int(predictions) - int(targets)
            differences_squared = differences ** 2
            mean_of_differences_squared = float(differences_squared)/float(mean)
            rmse_val = sqrt(mean_of_differences_squared)
            return rmse_val

    def neighbours(self):
        for user_id, user in self.users.items():
            userSet = set(user.rating_dic)
            counter = 0
            for user_id2, user2 in self.users.items():
                x = []
                y = []

                if user == user2:
                    continue
                elif user.has_neighbor(user_id2):
                    continue
                else:
                    user2Set = set(user2.rating_dic)
                    for i in userSet.intersection(user2Set):
                        x.append(user.get_rating_for(i))
                        y.append(user2.get_rating_for(i))
                    if x and y:
                        cosin = self.cosine_similarity(x, y)
                        if len(user.neighbors) >= 100:
                            if cosin > int(user.neighbors.get(min(user.neighbors, key=user.neighbors.get))):
                                del user.neighbors[min(user.neighbors, key=user.neighbors.get)]
                                user.add_neighbor(user_id2, cosin)
                            if len(user2.neighbors) >= 100:
                                if cosin > int(user2.neighbors.get(min(user2.neighbors, key=user2.neighbors.get))):
                                    del user2.neighbors[min(user2.neighbors, key=user2.neighbors.get)]
                                    user2.add_neighbor(user_id, cosin)
                                user2.add_neighbor(user_id, cosin)
                        else:
                            user.add_neighbor(user_id2, cosin)
                            user2.add_neighbor(user_id, cosin)
                            counter += 1

    def square_rooted(self, x):
        return round(sqrt(sum([int(a) * int(a) for a in x])), 3)

    def cosine_similarity(self, x, y):
        numerator = sum(int(a) * int(b) for a, b in zip(x, y))
        denominator = round(sqrt(sum([int(a) * int(a) for a in x])), 3) * round(sqrt(sum([int(b) * int(b) for b in y])), 3)
        return round(numerator / float(denominator), 3)


argparser = argparse.ArgumentParser(
    description='Collaborative Filtering Recommender System')
argparser.add_argument(
    '-f', '--file',
    dest='data_file',
    action="store",
    type=str,
    default=None,
    required=True,
    help='File name containing relevant data'
)
args = argparser.parse_args()
startTime = datetime.datetime.now()
main = Main(args.data_file)
main.data()
main.coverage("Colab.csv")
main.neighbours()
print "Time taken: " + str(datetime.datetime.now() - startTime)
