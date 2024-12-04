import uuid
from django.db import models

class GradeLevel(models.Model):
    PREKINDERGARTEN = 'Prekindergarten'
    KINDERGARTEN = 'Kindergarten'
    FIRST_GRADE = '1st Grade'
    SECOND_GRADE = '2nd Grade'
    THIRD_GRADE = '3rd Grade'
    FOURTH_GRADE = '4th Grade'
    FIFTH_GRADE = '5th Grade'
    SIXTH_GRADE = '6th Grade'
    SEVENTH_GRADE = '7th Grade'
    EIGHTH_GRADE = '8th Grade'
    NINTH_GRADE = '9th Grade'
    TENTH_GRADE = '10th Grade'
    ELEVENTH_GRADE = '11th Grade'
    TWELFTH_GRADE = '12th Grade'

    GRADE_CHOICES = [
        (PREKINDERGARTEN, 'Prekindergarten'),
        (KINDERGARTEN, 'Kindergarten'),
        (FIRST_GRADE, '1st Grade'),
        (SECOND_GRADE, '2nd Grade'),
        (THIRD_GRADE, '3rd Grade'),
        (FOURTH_GRADE, '4th Grade'),
        (FIFTH_GRADE, '5th Grade'),
        (SIXTH_GRADE, '6th Grade'),
        (SEVENTH_GRADE, '7th Grade'),
        (EIGHTH_GRADE, '8th Grade'),
        (NINTH_GRADE, '9th Grade'),
        (TENTH_GRADE, '10th Grade'),
        (ELEVENTH_GRADE, '11th Grade'),
        (TWELFTH_GRADE, '12th Grade'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grade_level = models.CharField(max_length=50, choices=GRADE_CHOICES, unique=True)

    def __str__(self):
        return self.grade_level
