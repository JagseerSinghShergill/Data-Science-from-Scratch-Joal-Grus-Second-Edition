# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:20:43 2022

@author: ITER
"""

from matplotlib import pyplot as plt

##########################
#                        #
# FINDING KEY CONNECTORS #
#                        #
##########################

users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" },
    { "id": 10, "name": "Jen" }
]

friendship_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]


# first give each user an empty list
friendships ={user['id']: [] for user in users}

# and then populate the lists with friendships
for i,j in friendship_pairs:
    # this works because users[i] is the user whose id is i
    friendships[j].append(i) # add i as a friend of j
    friendships[i].append(j) # add j as a friend of i
print("Frienship data:\n",friendships)

def number_of_friends(user):
    """how many friends does _user_ have?"""
    user_id = user['id']
    friend_ids = friendships[user_id]
    return len(friend_ids)

total_connections = sum(number_of_friends(user)
                        for user in users) # 24

num_users = len(users)
avg_connections = total_connections / num_users # 2.4
print("Average Number of connection:",avg_connections)
"""Create a list(user_id, number_of_friends)"""
num_friends_by_id = [(user["id"],number_of_friends(user))for user in users]
print("Friends of each individual:\n",num_friends_by_id)
num_friends_by_id.sort(key=lambda id_and_friends: id_and_friends[1], reverse=True)
print("Friends of each individual in sorted form:\n",num_friends_by_id)

################################
#                              #
# DATA SCIENTISTS YOU MAY KNOW #
#                              #
################################

def foaf_ids_bad(user):
    # "foaf" is short for "friend of a friend"
    return [foaf_id
            for friend_id in friendships[user["id"]]# for each of user's friends
            for foaf_id in friendships[friend_id]] # get each of _their_ friends
print(foaf_ids_bad(users[1]))
from collections import Counter # not loaded by default



def friends_of_friends(user):
    user_id = user["id"]
    return Counter(
            foaf_id
            for friend_id in friendships[user_id] # For each of my friends,
            for foaf_id in friendships[friend_id] # find their friends
            if foaf_id != user_id # who aren't me
            and foaf_id not in friendships[user_id] # and aren't my friends.
)
print("Foaf of 3 :",friends_of_friends(users[3])) # Counter({0: 2, 5: 1})


interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")]

def data_scientists_who_like(target_interest):
    """Find the ids of all users who like the target interest."""
    return [user_id
            for user_id, user_interest in interests
            if user_interest == target_interest]
print("Data scientists like Java: ",data_scientists_who_like("Java"))
from collections import defaultdict

"""Keys are interests, values are lists of user_ids with that interest"""
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# keys are user_ids, values are lists of interests for that user_id
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

def most_common_interests_with(user):
    return Counter(
        interested_user_id
        for interest in interests_by_user_id[user["id"]]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user["id"])

###########################
#                         #
# SALARIES AND EXPERIENCE #
#                         #
###########################

salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
                        (48000, 0.7), (76000, 6),
                        (69000, 6.5), (76000, 7.5),
                        (60000, 2.5), (83000, 10),
                        (48000, 1.9), (63000, 4.2)]

def make_chart_salaries_by_tenure():
    tenures = [tenure for salary, tenure in salaries_and_tenures]
    salaries = [salary for salary, tenure in salaries_and_tenures]
    plt.scatter(tenures, salaries)
    plt.xlabel("Years Experience")
    plt.ylabel("Salary")
    plt.show()
make_chart_salaries_by_tenure()
# keys are years
# values are the salaries for each tenure
salary_by_tenure = defaultdict(list)

for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)
print('tenure and salary :\n',salary_by_tenure)
average_salary_by_tenure = {
    tenure : sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()}
print('average salary by tenure :\n',average_salary_by_tenure)
def tenure_bucket(tenure):
    if tenure < 2: return "less than two"
    elif tenure < 5: return "between two and five"
    else: return "more than five"

salary_by_tenure_bucket = defaultdict(list)

for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

average_salary_by_bucket = {
  tenure_bucket : sum(salaries) / len(salaries)
  for tenure_bucket, salaries in salary_by_tenure_bucket.items()}
print('average salary by bucket :\n',average_salary_by_bucket)

#################
#               #
# PAID_ACCOUNTS #
#               #
#################

def predict_paid_or_unpaid(years_experience):
  if years_experience < 3.0: return "paid"
  elif years_experience < 8.5: return "unpaid"
  else: return "paid"

######################
#                    #
# TOPICS OF INTEREST #
#                    #
######################

words_and_counts = Counter(word
                           for user, interest in interests
                           for word in interest.lower().split())
print("Most_common function:\n",words_and_counts.most_common())
print("Words and Counts\n")
for word, count in words_and_counts.most_common():
    if count > 1:
        print(word,"-", count,end="|")