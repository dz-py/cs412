# voter_analytics/models.py
# Defines the Voter model and a function to load voter data from a CSV file into the database.

from django.db import models

class Voter(models.Model):
    '''Encapsulate the data of a registered voter'''
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()
    dob = models.TextField()  # Date of Birth
    dor = models.TextField()  # Date of Registration
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    
    # Election participation fields
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    
    # Voter participation score
    voter_score = models.IntegerField()
    
    def __str__(self):
        '''String representation of a voter'''
        return f"{self.first_name} {self.last_name}"
    

def load_data():
    '''
    Process the CSV data file and load Voter records into the database
    '''
    file_path='/Users/dechengzheng/Desktop/django/voter_analytics/newton_voters.csv'

    f = open(file_path, 'r')

    # Discard header
    f.readline()

    for line in f:
        try:
            fields = line.strip().split(',')
            # Example fields
            # fields[0] = 10KSA1343001 - Discard ID
            # fields[1] = KIGGEN
            # fields[2] = SHEILA
            # fields[3] = 193
            # fields[4] = OAK ST
            # fields[5] = 103E
            # fields[6] = 02464
            # fields[7] = 1943-10-13
            # fields[8] = 2016-02-10
            # fields[9] = D 
            # fields[10] = 1
            # fields[11] = TRUE
            # fields[12] = TRUE
            # fields[13] = FALSE
            # fields[14] = TRUE
            # fields[15] = FALSE
            # fields[16] = 3
            
            result = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                dob=fields[7],
                dor=fields[8],
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10],
                v20state=fields[11],
                v21town=fields[12],
                v21primary=fields[13],
                v22general=fields[14],
                v23town=fields[15],
                voter_score=int(fields[16])
            )
            result.save()
            # print(f'Created Voter {result}')
        except:
            print(f"Something went wrong at line {line}")
    print(f"Finished creating {len(Voter.objects.all())} voters")
    
    f.close()