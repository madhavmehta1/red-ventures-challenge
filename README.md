# BOT-O-MAT
This application collects a name and robot type from a given list. With this information, it creates a robot of the specified type and assigns a set of five random tasks. These tasks have estimated times of completion in milliseconds, so the robots "perform" these tasks by waiting for the specified estimated times.

Application features:
  - Create Robots
  - Assign and Perform Tasks
  - View Leaderboard
    - Robots are only given credit for completing tasks if their robot type is allowed to perform these tasks.
  - View Completed Tasks

## Tasks
Tasks have a description and an estimated time to complete.

```
[
  {
    description: 'do the dishes',
    eta: 1000,
  },{
    description: 'sweep the house',
    eta: 3000,
  },{
    description: 'do the laundry',
    eta: 10000,
  },{
    description: 'take out the recycling',
    eta: 4000,
  },{
    description: 'make a sammich',
    eta: 7000,
  },{
    description: 'mow the lawn',
    eta: 20000,
  },{
    description: 'rake the leaves',
    eta: 18000,
  },{
    description: 'give the dog a bath',
    eta: 14500,
  },{
    description: 'bake some cookies',
    eta: 8000,
  },{
    description: 'wash the car',
    eta: 20000,
  },
]
```

## Types
```
{ 
  UNIPEDAL: 'Unipedal',
  BIPEDAL: 'Bipedal',
  QUADRUPEDAL: 'Quadrupedal',
  ARACHNID: 'Arachnid',
  RADIAL: 'Radial',
  AERONAUTICAL: 'Aeronautical'
}
```

# How to Set Up
Python3 and MongoDB were used to develop this application.

## Python Installation
Please follow these links to install Python on your system:
- [Windows](https://docs.python-guide.org/starting/install3/win/)
- [Linux](https://docs.python-guide.org/starting/install3/linux/)
- [Mac OS](https://docs.python-guide.org/starting/install3/osx/)

Dependencies:
- [PyMongo](https://api.mongodb.com/python/current/) was used to provide an interface to communicate with the MongoDB cluster.
- [dnspython](http://www.dnspython.org/) was needed in order to connect to the MongoDB cluster because the connection string leverages DNS seedlist.
- [PrettyTable](https://pypi.org/project/PrettyTable/) was used to create the output tables

To install the Python dependencies for this project, you can do either of the following:
- Use the requirements.txt file. Navigate to the root of this project's directory. Linux/Mac OS users should open a terminal session within the directory and Windows users should open a power shell session within the directory and type the following command:
  ```
  pip install -r requirements.txt
  ```
- Manually install the dependencies. Enter the following commands:
  ```
  pip install pymongo
  pip install dnspython
  pip install PrettyTable
  ```

## MongoDB Setup
MongoDB Atlas was used as the storage solution for this application. It lets users set up free MongoDB clusters with a cloud provider (AWS, Azure, GCP). [Follow this link to set up a free cluster.](https://docs.atlas.mongodb.com/getting-started/)
The interface will provide a checklist of essential things to configure for the cluster - it is important to follow this checklist. Keep note of the user, password, and Python connection string created during this process.

This is the configuration used for this application:
- Cloud Provider & Region: AWS, N.Virginia (us-east-1)
- Cluster Tier: M0 Sandbox (Shared RAM, 512 MB Storage) Encrypted
- Additional Settings MongoDB 4.2, No backup
[INSERT IMAGE]

After the cluster is setup, create a database called "robots" and two collections called "robotlist" and "tasklist".
[INSERT IMAGE]

Finally, configure the "db.py" file by inserting the connection string that was provided for Python appplications. Insert the user and password fields within the connection string.
