#!/usr/bin/python
import argparse
import csv

import datetime

from User import User
from Movie import Movie
from Rating import Rating
import math


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
            self.movies[movie].add_rating(user, rating)
            self.users[user].add_rating(movie, rating)

    def coverage(self, outname):
        test_data = 0.0
        cant_test = 0.0
        rmse_list = []
        outfile = open(outname, 'w')
        outfile.write("user_id, item_id, Actual Rating, Predicted Rating, RMSE\n")
        wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        for key, val in self.movies.items():
            film = val
            mean = film.rating_count()
            user_id = film.get_random_user()
            actual = self.users[user_id].get_rating_for(key)
            prediction = 0
            for user, rate in film.ratings.items():
                if user is user_id:
                    test_data += 1
                    continue
                else:
                    prediction += int(rate)
            prediction /= mean
            error = self.rmse(prediction, actual, mean)
            if prediction == 0:
                cant_test += 1
            else:
                rmse_list.append(error)
                wr.writerow([user_id, key, actual, prediction, error])
        full_err = 0
        for x in rmse_list:
            full_err += x
        percentage_covered = ((test_data - cant_test)/test_data) * 100.0
        print "Percentage Covered:" + str(percentage_covered)
        print "Average root mean squared error : " + str(full_err/len(rmse_list))

    def rmse(self, predictions, targets, mean):
            differences = predictions - int(targets)
            differences_squared = differences ** 2
            mean_of_differences_squared = float(differences_squared)/float(mean)
            rmse_val = math.sqrt(mean_of_differences_squared)
            return rmse_val


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
print "Time taken: " + str(datetime.datetime.now() - startTime)
