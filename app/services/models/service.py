from random import randint, SystemRandom
from datetime import datetime

from app.utils.extensions.database import module as connector
from app.services.models.category_items import get_category_item_by_name

bool_types = [
    'published',
    'open_ended'
]

int_types = [
    'search_result_priority',
]

date_types = [
    'start',
    'end'
]



class Service(connector.Model):
    id                              = connector.Column(connector.Integer,       primary_key = True)
    created                         = connector.Column(connector.DateTime,      default     = datetime.utcnow)
    published                       = connector.Column(connector.Boolean)                           # Julkinen
    
    ptv_service_id                  = connector.Column(connector.String(100))                       # PTV Palvelun ID
    ptv_service_channel_id          = connector.Column(connector.String(100))                       # PTV Palvelukanavan ID

    search_result_priority          = connector.Column(connector.Integer,       primary_key = True) # Hakutulosprioriteetti
    name                            = connector.Column(connector.String(100))                       # Palvelun nimi
    organization                    = connector.Column(connector.Text)                              # JÃ¤rjestÃ¤vÃ¤ organisaatio
    ingress                         = connector.Column(connector.Text)                              # Ingressi

    description                     = connector.Column(connector.Text)                              # Kuvaus
    description2                    = connector.Column(connector.Text)                              # Kuvaus 2
    description3                    = connector.Column(connector.Text)                              # Kuvaus 3
    description4                    = connector.Column(connector.Text)                              # Kuvaus 4

    provider                        = connector.Column(connector.Text)                              # Toimija
    benefit_effect                  = connector.Column(connector.Text)                              # Vaikuttaako tukiin
    constraint                      = connector.Column(connector.Text)                              # Palvelun rajaukset

    open_ended                      = connector.Column(connector.Boolean)                           # Voimassa toistaiseksi
    
    start                           = connector.Column(connector.DateTime,      default     = datetime.utcnow)                          # Voimassaolon alku
    end                             = connector.Column(connector.DateTime,      default     = datetime.utcnow)                          # Voimassaolon loppu
    
    address                         = connector.Column(connector.String(100))                       # Katuosoite
    address_extended                = connector.Column(connector.String(100))                       # Osoitteen tarkennus
    post_address                    = connector.Column(connector.String(20))                        # Postiosoite
    
    contact_person                  = connector.Column(connector.String(100))                       # YhteyshenkilÃ¶
    contact_person_phone            = connector.Column(connector.String(100))                       # Puhelinnumero
    contact_email                   = connector.Column(connector.String(100))                       # SÃ¤hkÃ¶posti
    
    www                             = connector.Column(connector.String(100))                       # Verkkosivu
    facebook                        = connector.Column(connector.String(100))                       # Facebook
    twitter                         = connector.Column(connector.String(100))                       # Twitter

    category_items                  = connector.Column(connector.PickleType)

    notes                           = connector.Column(connector.Text)                              # Palveluntarjoajan viestilaatikko
    content_contact                 = connector.Column(connector.String(100))                       # SisÃ¤llÃ¶n yhteyshenkilÃ¶


    def __init__(self,  published=True,     ptv_service_id="",  ptv_service_channel_id="",  search_result_priority=0,       name="", 
                        organization="",    ingress="",         description="",             description2="",                description3="", 
                        description4="",    provider="",        benefit_effect="",          constraint="",                  open_ended=True,
                        start=None,         end=None,           address="",                 address_extended="",            post_address="",
                        www="",             facebook="",        twitter="",                 service_path=None,              target=None, 
                        study=None,         integration=None,   notes="",                   content_contact="",             immigration=None,
                        contact_person="",  age_group=None,     unemployment_duration=None, health=None,                    contact_person_phone="",
                        contact_email="",   classification=None,                            category_items=None,            form={}):

                        self.id                     = amount() + 1
                        self.published              = form.get('published')                 if form.get('published')                else published
                        self.ptv_service_id         = form.get('ptv_service_id')            if form.get('ptv_service_id')           else ptv_service_id
                        self.ptv_service_channel_id = form.get('ptv_service_channel_id')    if form.get('ptv_service_channel_id')   else ptv_service_channel_id
                        self.search_result_priority = form.get('search_result_priority')    if form.get('search_result_priority')   else search_result_priority
                        self.name                   = form.get('name')                      if form.get('name')                     else name
                        self.organization           = form.get('organization')              if form.get('organization')             else organization
                        self.ingress                = form.get('ingress')                   if form.get('ingress')                  else ingress
                        self.description            = form.get('description')               if form.get('description')              else description
                        self.description2           = form.get('description2')              if form.get('description2')             else description2
                        self.description3           = form.get('description3')              if form.get('description3')             else description3
                        self.description4           = form.get('description4')              if form.get('description4')             else description4
                        self.provider               = form.get('provider')                  if form.get('provider')                 else provider
                        self.benefit_effect         = form.get('benefit_effect')            if form.get('benefit_effect')           else benefit_effect
                        self.constraint             = form.get('constraint')                if form.get('constraint')               else constraint
                        self.open_ended             = form.get('open_ended')                if form.get('open_ended')               else open_ended
                        self.start                  = form.get('start')                     if form.get('start')                    else start
                        self.end                    = form.get('end')                       if form.get('end')                      else end
                        self.address                = form.get('address')                   if form.get('address')                  else address
                        self.address_extended       = form.get('address_extended')          if form.get('address_extended')         else address_extended
                        self.post_address           = form.get('post_address')              if form.get('post_address')             else post_address
                        self.www                    = form.get('www')                       if form.get('www')                      else www
                        self.facebook               = form.get('facebook')                  if form.get('facebook')                 else facebook
                        self.twitter                = form.get('twitter')                   if form.get('twitter')                  else twitter
                        self.service_path           = form.get('service_path')              if form.get('service_path')             else service_path
                        self.target                 = form.get('target')                    if form.get('target')                   else target
                        self.study                  = form.get('study')                     if form.get('study')                    else study
                        self.integration            = form.get('integration')               if form.get('integration')              else integration
                        self.notes                  = form.get('notes')                     if form.get('notes')                    else notes
                        self.content_contact        = form.get('content_contact')           if form.get('content_contact')          else content_contact
                        self.immigration            = form.get('immigration')               if form.get('immigration')              else immigration
                        self.contact_person         = form.get('contact_person')            if form.get('contact_person')           else contact_person
                        self.age_group              = form.get('age_group')                 if form.get('age_group')                else age_group
                        self.unemployment_duration  = form.get('unemployment_duration')     if form.get('unemployment_duration')    else unemployment_duration
                        self.health                 = form.get('health')                    if form.get('health')                   else health
                        self.contact_person_phone   = form.get('contact_person_phone')      if form.get('contact_person_phone')     else contact_person_phone
                        self.contact_email          = form.get('contact_email')             if form.get('contact_email')            else contact_email
                        self.classification         = form.get('classification')            if form.get('classification')           else classification
                        self.category_items         = form.get('category_items')            if form.get('category_items')           else category_items



    def __str__(self):
        if self.name:
            return self.name
        return ''

    def __repr__(self):
        return "<Service %d>" % self.id

    
    def save(self):
        connector.session.add(self)
        connector.session.commit()
        return self
    
    def delete(self):
        connector.session.delete(self)
        connector.session.commit()

    def fixed(self, t):
        if t == 'start':
            return str(self.start).replace(' ','T')
        elif t == 'end':
            return str(self.end).replace(' ','T')
        return ''

def create_new(fields=[], form={}):
    return Service(form=form).save()

def get_services():
    return Service.query.all()


def find_service(id):
    return Service.query.filter_by(id=id).first()

def services_from_category(name=None):
    if name:
        query = Service.query.filter_by(category_id=name)
        return query if query else []
    else:
        query = Service.query.all()
        return query if query else []

def amount():
    return len(get_services())


def normalize(fields=[]):
    x = []
    for field in fields:
        try:
            x.append('%s %s' % (field.split('_')[0].capitalize(), field.split('_')[1]))
        except:
            x.append(field.split('_')[0].capitalize())
    return x

def get_fields():
    fields = {                            
    'published':                (None, 'bool'),             # Julkinen
    
    'ptv_service_id':           (None, 'str'),              # PTV Palvelun ID
    'ptv_service_channel_id':   (None, 'str'),              # PTV Palvelukanavan ID

    'search_result_priority':   (None, 'int'),              # Hakutulosprioriteetti
    'name':                     (None, 'str'),              # Palvelun nimi
    'organization':             (None, 'str'),              # JÃ¤rjestÃ¤vÃ¤ organisaatio
    'ingress':                  (None, 'str'),              # Ingressi

    'description':              (None, 'str'),              # Kuvaus
    'description2':             (None, 'str'),              # Kuvaus 2
    'description3':             (None, 'str'),              # Kuvaus 3
    'description4':             (None, 'str'),              # Kuvaus 4

    'provider':                 (None, 'str'),              # Toimija
    'benefit_effect':           (None, 'str'),              # Vaikuttaako tukiin
    'constraint':               (None, 'str'),              # Palvelun rajaukset

    'open_ended':               (None, 'bool'),             # Voimassa toistaiseksi
    
    'start':                    (None, 'date'),             # Voimassaolon alku
    'end':                      (None, 'date'),             # Voimassaolon loppu
    
    'address':                  (None, 'str'),              # Katuosoite
    'address_extended':         (None, 'str'),              # Osoitteen tarkennus
    'post_address':             (None, 'str'),              # Postiosoite
    
    'contact_person':           (None, 'str'),              # YhteyshenkilÃ¶
    'contact_person_phone':     (None, 'str'),              # Puhelinnumero
    'contact_email':            (None, 'str'),              # SÃ¤hkÃ¶posti
    
    'www':                      (None, 'str'),              # Verkkosivu
    'facebook':                 (None, 'str'),              # Facebook
    'twitter':                  (None, 'str'),              # Twitter

    'notes':                    (None, 'str'),              # Palveluntarjoajan viestilaatikko
    'content_contact':          (None, 'str'),              # SisÃ¤llÃ¶n yhteyshenkilÃ¶
    }
    return fields