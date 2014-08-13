# Initialize the required users in the system

from django.contrib.auth.models import User

# Check that the correct users are set up
def run():
    print 'Checking for users:'

    # Make sure there is one Super User
    if len(User.objects.filter(username='SuperUser'))!=1:
        print 'Bad super user config'
    else:
        print '   Super user - OK'

    # Make sure there is one Test Robot user
    if len(User.objects.filter(username='TestRobot'))!=1:
        print 'Create TestRobot user'
        name = 'TestRobot'
        email = 'mark.b.seaman+TestRobot@gmail.com'
        pw =  'x'
        user = User.objects.create_user(name, email, pw)
    if len(User.objects.filter(username='TestRobot'))==1:
        print '   Test Robot - OK'

    # Make sure there is one Test Robot user
    if len(User.objects.filter(username='seaman'))!=1:
        print 'Create seaman user'
        name = 'seaman'
        email = 'mark.b.seaman+brain@gmail.com'
        pw =  'x'
        user = User.objects.create_user(name, email, pw)
    if len(User.objects.filter(username='seaman'))==1:
        print '   seaman - OK'
