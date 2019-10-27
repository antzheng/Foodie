class User:
    def __init__(self, bodyweight, height, age, sex, activityLevel):
        self.bodyweight = bodyweight        ## a float (lbs)
        self.height = height                ## a float (inches)
        self.age = age                      ## a float (years)
        self.sex = sex                      ## a string ('M' or 'F')
        self.activityLevel = activityLevel  ## activity level (1.2, 1.375, 1.55, 1.725)
        self.caloriesNeeded = round(self.calculateCalories(bodyweight, height, age, sex, activityLevel), 2)

    def calculateCalories(self, weight, height, age, sex, activityLevel):
        if sex == 'F':
            return ((weight * 4.35) + (height * 4.7) - (age * 4.7) + 655) * activityLevel
        else:
            return ((weight * 6.23) + (height * 12.7) - (age * 6.8) + 66) * activityLevel
    