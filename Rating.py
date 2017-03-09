#!/usr/bin/python


class Rating(object):
    def __init__(self, num):
        self.users = {} #list of users and the items they rated in with this rating
        self.movies = {} #list of items and the users that rated each item with this rating

    def add_movie_to_user(self, movie, user): #adds to movies dictionary
        movielist = []
        if self.movies.get(movie) is not None:
            movielist = self.movies.get(movie)
        movielist.append(user)
        self.movies[movie] = movielist

    def add_user_to_movie(self, movie, user): #adds to users dictionary
        userlist = []
        if self.users.get(user) is not None:
            userlist = self.users.get(user)
        userlist.append(movie)
        self.users[user] = userlist

    def users_gave_movie(self, movie): #retuns all users that gave an item the rating in the object
        return self.movies.get(movie)

    def movies_got_users(self, user): #retuns all items that gave a user gave the rating in the object
        return self.users.get(user)
