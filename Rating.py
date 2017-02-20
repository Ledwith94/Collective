#!/usr/bin/python

class Rating(object):
    def __init__(self, num):
        self.users = {}
        self.movies = {}

    def add_movie_to_user(self, movie, user):
        movielist = []
        if self.movies.get(movie) is not None:
            movielist = self.movies.get(movie)
        movielist.append(user)
        self.movies[movie] = movielist

    def add_user_to_movie(self, movie, user):
        userlist = []
        if self.users.get(user) is not None:
            userlist = self.users.get(user)
        userlist.append(movie)
        self.users[user] = userlist

    def users_gave_movie(self, movie):
        return self.movies.get(movie)

    def movies_got_users(self, user):
        return self.users.get(user)
