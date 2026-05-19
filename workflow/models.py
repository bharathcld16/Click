from django.db import models


STAGES = [
    ('applied',     'Applied'),
    ('screening',   'Screening'),
    ('interview',   'Interview'),
    ('offer',       'Offer'),
    ('accepted',    'Accepted'),
    ('rejected',    'Rejected'),
]


class JobApplication(models.Model):
    company     = models.CharField(max_length=200)
    role        = models.CharField(max_length=200)
    location    = models.CharField(max_length=200, blank=True)
    url         = models.URLField(blank=True)
    stage       = models.CharField(max_length=20, choices=STAGES, default='applied')
    notes       = models.TextField(blank=True)
    applied_on  = models.DateField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return f"{self.role} @ {self.company}"

    def stage_index(self):
        active = ['applied', 'screening', 'interview', 'offer', 'accepted']
        try:
            return active.index(self.stage)
        except ValueError:
            return -1


class StageLog(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='logs')
    from_stage  = models.CharField(max_length=20)
    to_stage    = models.CharField(max_length=20)
    note        = models.TextField(blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
