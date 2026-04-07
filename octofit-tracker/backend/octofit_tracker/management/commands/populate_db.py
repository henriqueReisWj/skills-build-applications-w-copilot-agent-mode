from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

from djongo import models as djongo_models

# Models for direct population (if not using Django models)
from bson.objectid import ObjectId

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Direct access to MongoDB via Djongo connection
        db = connection.cursor().db_conn.client['octofit_db']

        # Clean up collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel_id = ObjectId()
        dc_id = ObjectId()
        teams = [
            {'_id': marvel_id, 'name': 'Marvel'},
            {'_id': dc_id, 'name': 'DC'}
        ]
        db.teams.insert_many(teams)

        # Users
        users = [
            {'_id': ObjectId(), 'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_id},
            {'_id': ObjectId(), 'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'_id': ObjectId(), 'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
            {'_id': ObjectId(), 'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'_id': ObjectId(), 'user_email': 'spiderman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'_id': ObjectId(), 'user_email': 'ironman@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'_id': ObjectId(), 'user_email': 'batman@dc.com', 'activity': 'Swimming', 'duration': 25},
            {'_id': ObjectId(), 'user_email': 'wonderwoman@dc.com', 'activity': 'Yoga', 'duration': 60},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'_id': ObjectId(), 'name': 'Full Body', 'suggested_for': 'Marvel'},
            {'_id': ObjectId(), 'name': 'Strength', 'suggested_for': 'DC'},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'_id': ObjectId(), 'user_email': 'spiderman@marvel.com', 'points': 100},
            {'_id': ObjectId(), 'user_email': 'ironman@marvel.com', 'points': 90},
            {'_id': ObjectId(), 'user_email': 'batman@dc.com', 'points': 95},
            {'_id': ObjectId(), 'user_email': 'wonderwoman@dc.com', 'points': 110},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Unique index on email
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
