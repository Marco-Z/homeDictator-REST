# homeDictator_rest

in folder `RESTful` there is the REST web service that is used to communicate with the database and retrieve the resources representations returned in JSON format.

in `webApp` folder there is the web app that is used by the user to interact with the web service.



## GET APIs


-------------------------------
### /⟨int:group_id⟩
Given a group id encoded in the URL, returns a JSON string containing the information about the group:
-   `id` of the group
-   `name` of the group
-   array of `members` of the group as described in next section.

example:

```JSON
{   "name": "12/B",
    "members": [
        {   "balance": 10.20,
            "name": "Alice",
            "points": 78,
            "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
            "id": 11
        },
        {   "balance": -5.50,
            "name": "Bob",
            "points": 85,
            "password": "pbkdf2:sha1:1000$DNJRmIj1$a66745add16ee270639affd47cfa8ad7afbc40c9",
            "id": 12
        },
        {...}
    ],
    "id": 1
}
```

-------------------------------
### /⟨int:group_id⟩/⟨int:user_id⟩

Given a group id and a user id encoded in the URL, returns a JSON string containing the information about the user:
-   `id` of the user
-   `name` of the user
-   `password` of the user
-   `points` of the user
-   `balance` of the user

example:

```JSON
{   
    "balance": 10.20,
    "name": "Alice",
    "points": 78,
    "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
    "id": 11
}
```

-------------------------------
### /⟨int:group_id⟩/⟨int:user_id⟩/journal

Given a group id and a user id encoded in the URL, returns a JSON string containing the information about the user's cleaning activities:
-   `id` of the activity
-   name of the `user`
-   name of the `task`
-   `date` when the activity has been carried out
-   `description` of the activity (can be null)

example:

```JSON
[
    {
        "date": "2017-07-30",
        "user": "Alice",
        "task": "vacuum cleaner",
        "description": null,
        "id": 5
    },
    {
        "date": "2017-07-20",
        "user": "Alice",
        "task": "wash wc",
        "description": null,
        "id": 15
    },
    {...}
]
```

-------------------------------
### /⟨int:group_id⟩/finance/list

Given a group id encoded in the URL, returns a JSON string containing the information about the financial movements within a group ordered by date in descending order:
-   `id` of the user
-   `balance` of the user
-   `name` of the user

It can take two arguments:
-   `offset`: the offset of the entries in the database
-   `count`: the number of entries to retrieve


example:

```JSON
{
    "activities": [
        {
            "description": "shopping at Coop",
            "user": 11,
            "date": "2017-07-30",
            "id": 6,
            "amount": 10.32
        },
        {
            "description": "shopping at Poli",
            "user": 12,
            "date": "2017-08-01",
            "id": 7,
            "amount": 12.12
        },
        {...}
    ]
}
```

-------------------------------
### /⟨int:group_id⟩/journal/⟨int:_type⟩

Given a group id and a task id encoded in the URL, returns a JSON string containing the information about the activities of that type within a group ordered by date in descending order:
-   `id` of the activity
-   name of the `user`
-   name of the `task`
-   `date` when the activity has been carried out
-   `description` of the activity (can be null)

It can take two arguments:
-   `offset`: the offset of the entries in the database
-   `count`: the number of entries to retrieve
example:

```JSON
[
    {
        "date": "2017-07-30",
        "user": "Alice",
        "task": "vacuum cleaner",
        "description": null,
        "id": 5
    },
    {
        "date": "2017-07-31",
        "user": "Bob",
        "task": "clean pantries",
        "description": null,
        "id": 15
    },
    {...}
]
```

-------------------------------
### /⟨int:group_id⟩/journal/last

Given a group id encoded in the URL, returns a JSON string containing the information about the last activity of each that type within a group:
-   `id` of the activity
-   name of the `user`
-   name of the `task`
-   `date` when the activity has been carried out
-   `description` of the activity (can be null)

example:

```JSON
[
    {
        "date": "2017-07-30",
        "user": "Alice",
        "task": "vacuum cleaner",
        "description": null,
        "id": 5
    },
    {
        "date": "2017-07-31",
        "user": "Bob",
        "task": "clean pantries",
        "description": null,
        "id": 15
    },
    {...}
]
```


-------------------------------
### /⟨int:group_id⟩/journal/list

Given a group id encoded in the URL, returns a JSON string containing the information about the activities of that type within a group ordered by date in descending order:
-   `id` of the activity
-   name of the `user`
-   name of the `task`
-   `date` when the activity has been carried out
-   `description` of the activity (can be null)

It can take two arguments:
-   `offset`: the offset of the entries in the database
-   `count`: the number of entries to retrieve
example:

```JSON
[
    {
        "date": "2017-07-30",
        "user": "Alice",
        "task": "vacuum cleaner",
        "description": null,
        "id": 5
    },
    {
        "date": "2017-07-31",
        "user": "Bob",
        "task": "clean pantries",
        "description": null,
        "id": 15
    },
    {...}
]
```

-------------------------------
### /⟨int:group_id⟩/shopping/read

Given a group id encoded in the URL, it returns a string containing the shopping list for that group.

-------------------------------
### /⟨int:group_id⟩/tasks/list

Given a group id encoded in the URL, returns a JSON string containing the information about the tasks of that group:
-   `id` of the task
-   `name` of the task
-   `group` in which the task is valid
-   `frequency` with which the task has to be completed
-   `value` of that task

example:

```JSON
[
    {
        "value": 3,
        "frequency": 4,
        "group": 1,
        "name": "vacuum cleaner",
        "id": 1
    },
    {
        "value": 5,
        "frequency": 10,
        "group": 1,
        "name": "mop",
        "id": 2
    },
    {...}
]
```





## POST APIs


-------------------------------
### /⟨int:group_id⟩/⟨int:user_id⟩/gist

Given a group id and a user id encoded in the URL, it returns a JSON string containing the gist information about the user activities:
-   `date` of the activities
-   `points` that the user collected that date

example:

```JSON
{
    "user": 1,
    "gist": [
        {
            "points": 3,
            "date": "2017-07-30"
        },
        {
            "points": 2,
            "date": "2017-07-31"
        },
        {
            "points": 5,
            "date": "2017-08-01"
        },
        {...}
    ]
}
```

-------------------------------
### /⟨int:group_id⟩/⟨int:user_id⟩/destroy

Given a group id and a user id encoded in the URL, deletes the user entry from the database.
It returns a JSON string containing the information about the deleted user:
-   `id` of the user
-   `name` of the user
-   `password` of the user
-   `group` of the user
-   `balance` of the user

example:

```JSON
{   "balance": 10.20,
    "name": "Alice",
    "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
    "id": 11,
    "group": 1
}
```

-------------------------------
### /⟨int:group_id⟩/⟨int:user_id⟩/update

Given a group id and a user id encoded in the URL, and the following parameters as form values:
-   `name`: optional, new name of the user
-   `password`: optional, new password of the user
it updates the user entry in the database.
It returns a JSON string containing the updated information about the user:
-   `id` of the user
-   `name` of the user
-   `password` of the user
-   `group` of the user
-   `balance` of the user

example:

```JSON
{   "balance": 10.20,
    "name": "Alice",
    "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
    "id": 11,
    "group": 1
}
```

-------------------------------
### /⟨int:group_id⟩/⟨int:user_id⟩/update_balance

Given a group id and a user id encoded in the URL, and the following parameters as form values:
-   `delta`: mandatory, the amount to add to the balance (can be negative)
it updates the user entry in the database.
It returns a JSON string containing the updated information about the user:
-   `id` of the user
-   `name` of the user
-   `password` of the user
-   `group` of the user
-   `balance` of the user

example:

```JSON
{   "balance": 10.20,
    "name": "Alice",
    "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
    "id": 11,
    "group": 1
}
```

-------------------------------
### /⟨int:group_id⟩/create_user

Given a group id encoded in the URL, and the following parameters as form values:
-   `name`: mandatory, name of the user
-   `password`: mandatory, password of the user
it creates the user entry in the database.
It returns a JSON string containing the information about the new user:
-   `id` of the user
-   `name` of the user
-   `password` of the user
-   `group` of the user
-   `balance` of the user

example:

```JSON
{   "balance": 0.00,
    "name": "Charlie",
    "password": "pbkdf2:sha1:1000$n5ENeoo3$bddbda1b0513edcba60fbd1b4e1210256c615c2a",
    "id": 15,
    "group": 1
}
```

-------------------------------
### /⟨int:group_id⟩/destroy

Given a group id encoded in the URL, it deletes the group entry from the database.
It returns a JSON string containing the information about the deleted group:

-   `id` of the group
-   `name` of the group
-   `members` of the group

example:

```JSON
{   "name": "12/B",
    "id": 1,
    "members": [
        {   "balance": 10.20,
            "name": "Alice",
            "points": 78,
            "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
            "id": 11
        },
        {   "balance": -5.50,
            "name": "Bob",
            "points": 85,
            "password": "pbkdf2:sha1:1000$DNJRmIj1$a66745add16ee270639affd47cfa8ad7afbc40c9",
            "id": 12
        },
        {...}
    ]
}
```


-------------------------------
### /⟨int:group_id⟩/finance/create

Given a group id encoded in the URL, and the following parameters as form values:
-   `user`: mandatory, name of the user
-   `amount`: mandatory, amount of the movement
-   `date`: mandatory, date of the movement
-   `description`: mandatory, description of the movement
it creates the movement entry in the database.
It returns a JSON string containing the information about the new movement:
-   `id` of the movement
-   name of the `user`
-   `amount` of the movement
-   `date` of the movement
-   `description` of the movement

example:

```JSON
{
    "description": "shopping at Poli",
    "user": 12,
    "date": "2017-07-30",
    "id": 7,
    "amount": 12.12
}
```

-------------------------------
### /⟨int:group_id⟩/finance/destroy

Given a group id encoded in the URL, it deletes the movement entry from the database.
It returns a JSON string containing the information about the deleted movement:
-   `id` of the movement
-   name of the `user`
-   `amount` of the movement
-   `date` of the movement
-   `description` of the movement

example:

```JSON
{
    "description": "shopping at Poli",
    "user": 12,
    "date": "2017-07-30",
    "id": 7,
    "amount": 12.12
}
```

-------------------------------
### /⟨int:group_id⟩/journal/create

Given a group id encoded in the URL, and the following parameters as form values:
-   `user`: mandatory, id of the user
-   `task`: mandatory, id of the task
-   `date`: optional, date of activity
it creates the activity entry in the database.
It returns a JSON string containing the information about the new activity:
-   `id` of the activity
-   id of the `user`
-   id of the `task`
-   `date` when the activity has been carried out

example:

```JSON
{
    "date": "2017-07-31",
    "user": 12,
    "task": 2,
    "id": 15
}
```

-------------------------------
### /⟨int:group_id⟩/shopping/write

Given a group id encoded in the URL, and the following parameters as form values:
-   `list`: mandatory, shopping list
it updates the shopping in the database.
It returns a string containing the updated shopping list for that group.

-------------------------------
### /⟨int:group_id⟩/tasks/create

Given a group id encoded in the URL, and the following parameters as form values:
-   `name`: mandatory, name of the task
-   `frequency`: mandatory, frequency with which the task has to be completed
-   `value`: mandatory, value of that task
it creates the task entry in the database.
It returns a JSON string containing the information about the new task:
-   `id` of the task
-   `name` of the task
-   `group` in which the task is valid
-   `frequency` with which the task has to be completed
-   `value` of that task

example:

```JSON
{
    "value": 5,
    "frequency": 10,
    "group": 1,
    "name": "mop",
    "id": 2
}
```

-------------------------------
### /⟨int:group_id⟩/tasks/destroy

Given a group id encoded in the URL, it deletes the task entry from the database.
It returns a JSON string containing the information about the deleted task:
-   `id` of the task
-   `name` of the task
-   `group` in which the task is valid
-   `frequency` with which the task has to be completed
-   `value` of that task

example:

```JSON
{
    "value": 5,
    "frequency": 10,
    "group": 1,
    "name": "mop",
    "id": 2
}
```

-------------------------------
### /⟨int:group_id⟩/tasks/update

Given a group id encoded in the URL, and the following parameters as form values:
-   `name`: optional, name of the task
-   `frequency`: optional, frequency with which the task has to be completed
-   `value`: optional, value of that task
it updates the task entry in the database.
It returns a JSON string containing the updated information about the task:
-   `id` of the task
-   `name` of the task
-   `group` in which the task is valid
-   `frequency` with which the task has to be completed
-   `value` of that task

example:

```JSON
{
    "value": 5,
    "frequency": 7,
    "group": 1,
    "name": "mop",
    "id": 2
}
```

-------------------------------
### /⟨int:group_id⟩/update

Given a group id encoded in the URL, and the following parameters as form values:
-   `name`: optional, name of the group
it updates the group entry in the database.
It returns a JSON string containing the updated information about the group:
-   `id` of the group
-   `name` of the group
-   `members` of the group


example:

```JSON
{
    "name": "13/A",
    "id": 1,
    "members": [
        {   "balance": 10.20,
            "name": "Alice",
            "points": 78,
            "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
            "id": 11
        },
        {   "balance": -5.50,
            "name": "Bob",
            "points": 85,
            "password": "pbkdf2:sha1:1000$DNJRmIj1$a66745add16ee270639affd47cfa8ad7afbc40c9",
            "id": 12
        },
        {...}
    ]
}
```

-------------------------------
### /create_group

Given the following parameters as form values:
-   `name`: optional, name of the group
it creates the group entry in the database.
It returns a JSON string containing the information about the new group:
-   `id` of the group
-   `name` of the group
-   `members` of the group (that would be an empty list)


example:

```JSON
{
    "name": "25/C",
    "id": 2,
    "members": []
}
```


-------------------------------
### /search

Given the following parameters as form values:
-   `name`: mandatory, name of the user to look for
it searches the user entry in the database.
It returns a JSON string containing the information about the found user:
-   `id` of the user
-   `name` of the user
-   `password` of the user
-   `points` of the user
-   `balance` of the user

example:

```JSON
{   
    "balance": 10.20,
    "name": "Alice",
    "points": 78,
    "password": "pbkdf2:sha1:1000$4mYgPAhx$95506b27ab6e8923fd2ddee47c226e420bd43b06",
    "id": 11
}
```
