from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


class NominationAgreementModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'nomination_agreement'

    nomination_agreement_id = AutoField()
    store_id = CharField(max_length=100)
    username_requester = CharField(max_length=100) # a owner that requested
    username_to_approve = CharField(max_length=100) # a owner or founder
    username_to_nominate = CharField(max_length=100)
