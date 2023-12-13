from django.core.management.base import BaseCommand, CommandError

from tasks.models import User, Team, Task, Invite, Achievement

import pytz
from faker import Faker
from random import randint, random

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe', 'teams': 'BronzeBulls', 'is_superuser': True, 'is_staff': True},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe', 'teams': 'BronzeBulls', 'is_superuser': False, 'is_staff': False},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson', 'teams': 'BronzeBulls', 'is_superuser':False, 'is_staff': False},
]

team_fixture = [
    {'name': 'BronzeBulls', 'description': 'We are the bulls'}
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    #number of random teams in addition to the base 1 team for every 6 users
    RANDOM_TEAM_COUNT = 100
    #number of users to be seeded
    USER_COUNT = 300
    DEFAULT_PASSWORD = 'Password123'
    TEAM_ASSIGNMENT = None
    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.generate_teams_fixture()
        self.create_users()
        self.users = User.objects.all()
        self.create_random_teams()
        self.create_tasks()
        self.create_invites()
    
    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user(user_count)
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self, user_count):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        if (user_count % 6 == 0) or (user_count == 3):
            name = self.faker.word()
            team =  Team.objects.create(
                        name=name,
                        description=self.faker.sentence(),
                    )
            self.TEAM_ASSIGNMENT = team
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'is_superuser': False, 'is_staff': False})
       
    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_superuser=data['is_superuser'],
            is_staff=data['is_staff']
            )
        user = User.objects.get(username=data['username'])
        user.teams.add(self.TEAM_ASSIGNMENT)
        user.save()
        self.TEAM_ASSIGNMENT.members.add(user)
        self.TEAM_ASSIGNMENT.save()

    def create_random_teams(self):
        team_count = Team.objects.count()
        team_requirement = Team.objects.count() + self.RANDOM_TEAM_COUNT
        while  team_count < (team_requirement):
            print(f"Seeding random teams {team_count}/{team_requirement}", end='\r')
            self.generate_team()
            team_count = Team.objects.count()
        print("Team seeding complete.      ")

    def generate_team(self):
        name = self.faker.word()
        description = self.faker.sentence()
        self.try_create_teams({'name': name, 'description': description})

    def try_create_teams(self, data):
        try:
            self.create_team(data)
        except:
            pass

    def generate_teams_fixture(self):
        for data in team_fixture:
            if (data['name'] == 'BronzeBulls'):
                self.TEAM_ASSIGNMENT = Team.objects.create(
                                        name=data['name'],
                                        description=data['description'],
                                    )
            else:
                self.try_create_teams(data) 

    def create_team(self, data):
        team = Team.objects.create(
                    name=data['name'],
                    description=data['description']
                )
        for _ in range(randint(1,9)):
            index = randint(0,self.users.count()-1)
            user = self.users[index]
            user = User.objects.get(username=user.username)
            team.members.add(user)
            user.teams.add(team)
            user.save()
        team.save()

        

    def create_tasks(self):
        for team in Team.objects.all():
            for user in team.members.all():
                #number of tasks for each member of a team
                for _ in range(randint(0,5)):
                    self.generate_task(user, team)
                
        print("Task seeding complete.      ")

    def generate_task(self, user, team):
        title = self.faker.sentence()
        description = self.faker.paragraph()
        due_date = self.faker.future_datetime(end_date='+30d', tzinfo=None)
        self.try_create_task({'title': title, 'description': description, 'assigned_users': [user], 'team': team, 'due_date': due_date})

    def try_create_task(self, data):
        try:
            self.create_task(data)
        except:
            pass

    def create_task(self, data):
        assigned_users = data['assigned_users']
        team = data['team']
        task = Task.objects.create(
            title=data['title'],
            description=data['description'],
            team=team,
            due_date=data['due_date']
        )
        task.assigned_users.set(assigned_users)


    def create_invites(self):
        for team in Team.objects.all():
            for user in team.members.all():
                #chance a user made a pending invite
                randNum = randint(1,5)
                if (randNum == 5):
                    self.create_invite(team, user)
        print("Invite seeding complete.      ")

    def create_invite(self, team, user):
        non_team_members = User.objects.exclude(teams = team)
        index = randint(0,non_team_members.count()-1)
        recipient = non_team_members[index]
        Invite.objects.create(
            sender = user,
            recipient = recipient,
            team = team,
            status = 'pending'
        )


def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'