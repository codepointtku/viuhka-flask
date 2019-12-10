from random                                 import randint, SystemRandom
from datetime                               import datetime
from app.utils.extensions.database          import module as connector
from app.services.models.category_items     import get_category_item_by_name


class Service(connector.Model):
    id                              = connector.Column(connector.Integer,       primary_key = True, autoincrement=True)
    created                         = connector.Column(connector.DateTime,      default     = datetime.utcnow)
    published                       = connector.Column(connector.Boolean)                           # Julkinen
    
    ptv_service_id                  = connector.Column(connector.Text)                       # PTV Palvelun ID
    ptv_service_channel_id          = connector.Column(connector.Text)                       # PTV Palvelukanavan ID

    search_result_priority          = connector.Column(connector.Integer,       default     = 0) # Hakutulosprioriteetti
    name                            = connector.Column(connector.Text)                       # Palvelun nimi
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
    
    address                         = connector.Column(connector.Text)                       # Katuosoite
    address_extended                = connector.Column(connector.Text)                       # Osoitteen tarkennus
    post_address                    = connector.Column(connector.Text)                        # Postiosoite
    
    contact_person                  = connector.Column(connector.Text)                       # YhteyshenkilÃ¶
    contact_person_phone            = connector.Column(connector.Text)                       # Puhelinnumero
    contact_email                   = connector.Column(connector.Text)                       # SÃ¤hkÃ¶posti
    
    www                             = connector.Column(connector.Text)                       # Verkkosivu
    facebook                        = connector.Column(connector.Text)                       # Facebook
    twitter                         = connector.Column(connector.Text)                       # Twitter

    category_items                  = connector.Column(connector.PickleType)

    notes                           = connector.Column(connector.Text)                       # Palveluntarjoajan viestilaatikko
    content_contact                 = connector.Column(connector.Text)                       # SisÃ¤llÃ¶n yhteyshenkilÃ¶

    owner_id                        = connector.Column(connector.Integer,       primary_key = True)


    def __init__(self,  published=True,     ptv_service_id="",  ptv_service_channel_id="",  search_result_priority=0,       name="", 
                        organization="",    ingress="",         description="",             description2="",                description3="", 
                        description4="",    provider="",        benefit_effect="",          constraint="",                  open_ended=True,
                        start=None,         end=None,           address="",                 address_extended="",            post_address="",
                        www="",             facebook="",        twitter="",                 service_path=None,              target=None, 
                        study=None,         integration=None,   notes="",                   content_contact="",             immigration=None,
                        contact_person="",  age_group=None,     unemployment_duration=None, health=None,                    contact_person_phone="",
                        contact_email="",   classification=None,                            category_items=None,            csrf_token="",
                        owner_id=0,         form={}):

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
                        self.csrf_token             = form.get('csrf_token')                if form.get('csrf_token')               else csrf_token
                        self.owner_id               = form.get('owner_id')                  if form.get('owner_id')                 else owner_id


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
    
    def joined(self):
        return ' '.join([i for i in self.category_items.values()])
    def joined_sanitized(self):
        try:
            _list = self.category_items.values() if not isinstance(self.category_items, list) else self.category_items
            s = ' '.join([i.replace(' ','').replace(',','').replace('-','').lower() for i in _list])
        except:
            return ""
        return s

def create_new(fields=[], form={}):
    return Service(form=form).save()

def get_services():
    return Service.query.filter(Service.published == True).all()

def get_service_by_name(name):
    return Service.query.filter(Service.name == name).first()


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


def paginate_service_owner_id(owner_id, page=1, per_page=50):
    return Service.query.filter_by(owner_id=owner_id).paginate(page=page, per_page=per_page)