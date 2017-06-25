```shell
sudo apt-get install python-dateutil
```

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup_exercise_1_puppies import Base, Shelter, Puppy
from sqlalchemy import desc
import datetime
from dateutil.relativedelta import relativedelta

engine             = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession          = sessionmaker(bind = engine)
session            = DBSession()
```

1. Query all of the puppies and return the results in ascending alphabetical order
```python
puppies = session.query(Puppy).order_by(Puppy.name)
for puppy in puppies:
  print puppy.name
```

2. Query all of the puppies that are less than 6 months old organized by the youngest first
```python
today          = datetime.date.today()
six_months_ago = today + relativedelta(months = -6)

puppies = session.query(Puppy.name, Puppy.date_of_birth, Puppy.date_of_birth < six_months_ago).order_by(desc(Puppy.date_of_birth))
for puppy in puppies:
  print puppy.name + " : " + str(puppy.date_of_birth)
```

3. Query all puppies by ascending weight
```python
puppies = session.query(Puppy).order_by(Puppy.weight)
for puppy in puppies:
  print puppy.name + " : " + str(puppy.weight)
```

4. Query all puppies grouped by the shelter in which they are staying
```python
puppies = session.query(Puppy, Shelter).filter_by(Puppy.shelter_id == Shelter.id).order_by(Shelter.name)
for puppy in puppies:
  print puppy.Puppy.name + " : " + puppy.Shelter.name
```