from django.db import models


# class ObsNmsko1H(models.Model):
#     obs_id = models.BigIntegerField(null=False, primary_key=True)
#     si = models.ForeignKey('Si', on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     ta_2m = models.FloatField(blank=True, null=True)
#     pa_avg = models.FloatField(blank=True, null=True)
#     rh_avg = models.FloatField(blank=True, null=True)
#     ws_avg = models.FloatField(blank=True, null=True)
#     wd_avg = models.FloatField(blank=True, null=True)
#     ws_max = models.FloatField(blank=True, null=True)
#     wd_ws_max = models.FloatField(blank=True, null=True)
#     pr_sum = models.FloatField(blank=True, null=True)
#     hg = models.FloatField(db_column='HG', blank=True, null=True)  # Field name made lowercase.
#     pm10 = models.FloatField(db_column='PM10', blank=True, null=True)  # Field name made lowercase.
#     pm2_5 = models.FloatField(db_column='PM2_5', blank=True, null=True)  # Field name made lowercase.
#     so2 = models.FloatField(db_column='SO2', blank=True, null=True)  # Field name made lowercase.
#     no = models.FloatField(db_column='NO', blank=True, null=True)  # Field name made lowercase.
#     no2 = models.FloatField(db_column='NO2', blank=True, null=True)  # Field name made lowercase.
#     nox = models.FloatField(db_column='NOx', blank=True, null=True)  # Field name made lowercase.
#     co = models.FloatField(db_column='CO', blank=True, null=True)  # Field name made lowercase.
#     ben = models.FloatField(db_column='BEN', blank=True, null=True)  # Field name made lowercase.
#     h2s = models.FloatField(db_column='H2S', blank=True, null=True)  # Field name made lowercase.
#     o3 = models.FloatField(db_column='O3', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'obs_nmsko_1h'
#         unique_together = (('si', 'date'),)


# class Si(models.Model):
#     id = models.AutoField(primary_key=True)
#     ci = models.SmallIntegerField()
#     ii = models.BigIntegerField()
#     name = models.CharField(max_length=80, blank=True, null=True)
#     cccc = models.CharField(max_length=4, blank=True, null=True)
#     cc = models.CharField(max_length=2, blank=True, null=True)
#     iso_cc = models.IntegerField(blank=True, null=True)
#     lat = models.FloatField(blank=True, null=True)
#     lon = models.FloatField(blank=True, null=True)
#     elev = models.FloatField(blank=True, null=True)
#     info = models.CharField(max_length=32, blank=True, null=True)
#     vtime = models.DateTimeField()
#     mtime = models.DateTimeField()
#     changed_id = models.IntegerField(blank=True, null=True)
#     changes = models.CharField(max_length=32, blank=True, null=True)
#     ue = models.BooleanField(blank=True, null=True, default=0)
#
#     class Meta:
#         managed = False
#         db_table = 'si'
#
#     def __str__(self):
#         return self.name
