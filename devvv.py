import schedule

def job_1():
    print('Foo')

def job_2():
    print('Bar')

schedule.every().monday.at("12:40").do(job_1)
schedule.every().tuesday.at("16:40").do(job_2)

schedule.run_all()

# Add the delay_seconds argument to run the jobs with a number
# of seconds delay in between.
schedule.run_all(delay_seconds=2)
