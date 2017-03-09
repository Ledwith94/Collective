#!/usr/bin/python

import csv
import datetime

import argparse

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
        self.min_diff = -0.65
        self.max_diff = 0.65
        self.neighbourhood_size = 200
        self.stats_dict = {}
        self.csv_name = None

    def data(self): #Task 1
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
        for x in self.users.values():
            x.set_mean_rating()

    def mean_item_rating(self): #Task 1
        for key, val in self.movies.items():
            add = sum(val.ratings.itervalues())
            mean = len(val.ratings) - 1
            for user, obj in self.users.items():
                if mean == 0:
                    continue
                elif user in val.ratings:
                    sub = obj.get_rating_for(key)
                    add -= sub
                    obj.set_mean_item(key, float(add) / float(mean))
                    add += sub

    def n_mean_item_rating(self, user):
        for key in user.rating_dic.keys():
            add = 0
            mean = 0
            for x in user.neighbours:
                if key in x.rating_dic:
                    add += x.get_rating_for(key)
                    mean += 1
            if mean is not 0 or add is not 0:
                user.n_mean_item[key] = (float(add) / float(mean))

    def coverage(self, outname, group): #Task 2
        test_data = 0.0
        cant_test = 0.0
        rmse_list = 0
        outfile = open(outname+str(self.csv_name)+".csv", 'w')
        outfile.write("user_id, item_id, Actual Rating, Predicted Rating, RMSE\n")
        wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        if group is "Task3":
            for user, obj in self.users.items():
                self.n_mean_item_rating(obj)
                for movie, rating in obj.rating_dic.items():
                    test_data += 1
                    if obj.n_mean_item.get(movie) is None:
                        cant_test += 1
                    else:
                        error = self.rmse(obj.n_mean_item.get(movie), rating)
                        rmse_list += error
                        wr.writerow([user, movie, rating, obj.n_mean_item.get(movie), error])
        elif group is "Task2":
            for user, obj in self.users.items():
                for movie, rating in obj.rating_dic.items():
                    test_data += 1
                    if obj.mean_item.get(movie) is None:
                        cant_test += 1
                    else:
                        error = self.rmse(obj.mean_item.get(movie), rating)
                        rmse_list += error
                        wr.writerow([user, movie, rating, obj.mean_item.get(movie), error])
        elif group is "Task4":
            for user, obj in self.users.items():
                for movie, rating in obj.rating_dic.items():
                    test_data += 1
                    if obj.mean_item.get(movie) is None:
                        cant_test += 1
                    else:
                        res = self.resnicsks(obj, movie)
                        if res == 0:
                            cant_test += 1
                        else:
                            error = self.rmse(res, rating)
                            rmse_list += error
                            wr.writerow([user, movie, rating, res, error])
        outfile.close()
        percentage_covered = ((test_data - cant_test)/test_data) * 100.0
        mean_rmse = rmse_list / (test_data - cant_test)
        if group is "Task2":
            print "\n" + group
        else:
            print group+" " +str(outname)
        print "Coverage: " + str(percentage_covered)
        print "Mean RMSE: " + str(mean_rmse) + "\n"
        self.stats_dict[group+" " +str(self.csv_name)] = [str(percentage_covered), str(mean_rmse)]

    def rmse(self, predictions, targets): #Task 2
            differences = float(predictions) - float(targets)
            differences_squared = differences ** 2
            rmse_val = sqrt(differences_squared)
            return rmse_val

    def cosine_similarity(self, x, y): #task 3
        common = x.get_common_movies(y)
        if len(common) == 0:
            return 0
        numerator = 0
        denominatorx = 0
        denominatory = 0
        for movies in common:
            numerator += int(x.get_rating_for(movies)) * int(y.get_rating_for(movies))
            denominatorx += x.get_rating_for(movies) ** 2
            denominatory += y.get_rating_for(movies) ** 2
        return numerator / float(sqrt(denominatorx)) * float(sqrt(denominatory))

    def resnicsks(self, user, movie): #task 4
        mean = user.mean_rating
        add = 0.0
        sim = 0.0
        for neigh, val in user.neighbours.items():
            if neigh.has_rating_for(movie):
                add += (neigh.get_rating_for(movie) - neigh.get_mean_rating()) * val
                sim += abs(val)
        if add is 0.0:
            return 0
        else:
            return mean + add / sim

    def pearsons(self, x, y): #task 3
        common = x.get_common_movies(y)
        x_mean = x.get_mean_rating()
        y_mean = y.get_mean_rating()
        top = 0
        bottom_x = 0
        bottom_y = 0
        for movie in common:
            ad = x.get_rating_for(movie) - x_mean
            bd = y.get_rating_for(movie) - y_mean
            top += (ad * bd)
            bottom_x += (ad * ad)
            bottom_y += (bd * bd)
        bottom = sqrt(bottom_x * bottom_y)
        if bottom > 0:
            if len(common) < 20:
                return (len(common) * 1.0 / 20) * (top / bottom)
            else:
                return top / bottom
        else:
            return 0

    def neighbours(self, function, size): #Task 3
        if size <= 1:
            self.min_diff = -size
            self.max_diff = size

        else:
            self.neighbourhood_size = size
        self.csv_name = size
        for user1 in self.users.values():
            user1.set_mean_rating()
            for user2 in self.users.values():
                if user1 == user2 or user1 in user2.neighbours:
                    continue
                else:
                    if function == "pearsons":
                        similarity = self.pearsons(user1, user2)
                        if similarity > self.max_diff or similarity < self.min_diff:
                            user1.neighbours[user2] = similarity
                            user2.neighbours[user1] = similarity

                    elif function == "cosine":
                        similarity = self.cosine_similarity(user1, user2)
                        if len(user1.neighbours) > self.neighbourhood_size:
                            small_key = user1.small_value()
                            if similarity > user1.neighbours.get(small_key):
                                del(user1.neighbours[small_key])
                                user1.neighbours[user2] = similarity
                                user2.neighbours[user1] = similarity
                        else:
                            user1.neighbours[user2] = similarity
                            user2.neighbours[user1] = similarity

    def stats(self): #task 1
        for user in self.users.values():
            print "\nUser ID: " + str(user.user_id)
            print "Films Rated: " + str(user.get_rating_count())
            print "Mean Rating: " + str(user.get_mean_rating())
            print "Median Rating: " + str(user.get_median())
            print "Deviation: " + str(user.get_deviation_rating()) + "\n"
        for key, val in self.stats_dict.items():
            print "\n" + str(key)
            print "Percentage Covered:" + val[0]
            print "Average root mean squared error : " + val[1] + "\n"

    def reset(self):
        for user in self.users.values():
            user.neighbours.clear()


argparser = argparse.ArgumentParser(
    description='Make Recommendations Based on 4 different techniques')
argparser.add_argument(
    '-d', '--data',
    dest='data',
    action="store",
    type=str,
    default="Colab_data",
    required=True,
    help='Specify data file name'
)
argparser.add_argument(
    '-c', '--cosine',
    dest='cosine',
    action="store",
    type=int,
    default=None,
    required=False,
    help='Use cosine technique. Enter value greater than 1.'
)
argparser.add_argument(
    '-p', '--pearsons',
    dest='pearsons',
    action="store",
    type=float,
    default=None,
    required=False,
    help='Use pearsons technique. Enter value between 0 and 1.'
)
argparser.add_argument(
    '-r', '--resnick',
    dest='resnick',
    action="store_true",
    default=False,
    required=False,
    help='Use resnicks technique. Must use -p.'
)
argparser.add_argument(
    '-s', '--stats',
    dest='stats',
    action="store_true",
    default=False,
    required=False,
    help='Give stats on all users.'
)
args = argparser.parse_args()


main = Main(args.data)
main.data()
main.mean_item_rating() #task 1
main.coverage("Colab", "Task2") #task 2
startTime = datetime.datetime.now()
#
# if args.cosine is not None:
#     main.reset()
#     main.neighbours("cosine", args.cosine)
#     main.coverage("Colab_n" + str(args.cosine) + "_cosine", "Task3")
#
# if args.pearsons is not None:
#     main.reset()
#     main.neighbours("pearsons", args.pearsons)
#     main.coverage("Colab_n"+str(args.pearsons)+"_pearsons", "Task3")
#
# if args.pearsons is not None and args.resnick:
#     main.coverage("Colab_n"+str(args.pearsons)+"_resnicks", "Task4")
# elif args.pearsons is None and args.resnick:
#     print "Must use -p with a value between 0 and 1 (exclusive) to use resnicks"
#
# if args.stats is True:
#     main.stats()
#
# print "Time taken: " + str(datetime.datetime.now() - startTime)


# Below contains all code used to produce graphs
# in the final report. Comment out to run


# main = Main("Colab_data")
# main.data() #task 1
# main.mean_item_rating() #task 1
# main.coverage("Colab.csv", "Task2") #task 2
# #main.neighbours("pearsons") #task 3
# # main.neighbours("cosine", 100) #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# main.stats() #task 1
#
# startTime = datetime.datetime.now()

# main.neighbours("cosine", 25) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken  n = 25: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 50) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken  n = 50: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 75) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken n = 75: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 100) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken  n = 100: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 125) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken  n = 125: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 150) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken n = 150: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 175) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken n = 175: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 200) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken n = 200: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 250) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken n = 250: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 300) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken n = 300: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()
#
# main.neighbours("cosine", 400) #task 3
# main.coverage("Colab_n", "Task3") #task 3
# #main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
# print "Time taken n = 400: " + str(datetime.datetime.now() - startTime)
# main.reset()
#
# startTime = datetime.datetime.now()

# main.stats() #task 1

main.neighbours("pearsons", .5) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken  n = .5: " + str(datetime.datetime.now() - startTime)
main.reset()
startTime = datetime.datetime.now()

main.neighbours("pearsons", .55) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken n = .55: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .6) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken  n = .6: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .65) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken  n = .65: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .7) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken n = .7: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .75) #task 3
main.coverage("Colab_n100.csv", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken n = .75: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .8) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken n = .8: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .85) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken n = .85: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .9) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken n = .9: " + str(datetime.datetime.now() - startTime)
main.reset()

startTime = datetime.datetime.now()

main.neighbours("pearsons", .95) #task 3
main.coverage("Colab_n", "Task3") #task 3
main.coverage("Colab_n100_resnicks.csv", "Task4") #task 4
print "Time taken n = .95: " + str(datetime.datetime.now() - startTime)
