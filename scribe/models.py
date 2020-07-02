from datetime import datetime
from scribe import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text, nullable=False)
    wd_q_id = db.Column(db.String(20), nullable=False)
    lang_code = db.Column(db.String(7))
    domain = db.Column(db.Text)
    tag = db.Column(db.Text)
    retrieved_date = db.Column(db.Date, nullable=False,
                    default=datetime.now().strftime('%Y-%m-%d'))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Article({}, {}, {}, {}, {})".format(
               self.name,
               self.wd_q_id,
               self.lang_code,
               self.domain,
               self.tag)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    label = db.Column(db.String(150), nullable=False)
    article_id = db.Column(db.Text)
    order_number = db.Column(db.Integer)
    content_selection_method = db.Column(db.Text)
    lang_code = db.Column(db.String(7))
    quality = db.Column(db.String(25))
    retrieved_date = db.Column(db.Date, nullable=False,
                            default=datetime.now().strftime('%Y-%m-%d'))   

    def __repr__(self):
        # This is what is shown when object is printed
        return "Section({}, {}, {})".format(
               self.label,
               self.article_id,
               self.lang_code)


class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    article_id = db.Column(db.Integer)
    section_id = db.Column(db.Integer)
    publisher_name = db.Column(db.Text)
    wd_q_id = db.Column(db.String(20), nullable=False)
    publication_title = db.Column(db.Text)
    lang_code = db.Column(db.String(7))
    summary = db.Column(db.Text)
    url = db.Column(db.Text)
    quality = db.Column(db.String(25))
    publication_date = db.Column(db.Date, nullable=False,
                    default=datetime.now().strftime('%Y-%m-%d'))
    retrieved_date = db.Column(db.Date, nullable=False,
                    default=datetime.now().strftime('%Y-%m-%d'))
    content_selection_method = db.Column(db.Text)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Reference({}, {}, {}, {})".format(
               self.publisher_name,
               self.publication_title,
               self.summary,
               self.url)


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    article_id = db.Column(db.Integer)
    created = db.Column(db.Boolean, nullable=True)
    sandbox = db.Column(db.Boolean, nullable=True)
    timestamp = db.Column(db.Date, nullable=True,
                    default=datetime.now().strftime('%Y-%m-%d'))
    references_used = db.Column(db.String(500), nullable=False) # Concatenation of the reference_ids
    sections_used = db.Column(db.String(25), nullable=False) # Concatenation of the section_ids
    mobile = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Statistics({}, {}, {}, {}, {}, {})".format(
               self.article_id,
               self.created,
               self.sandbox,
               self.timestamp,
               self.references_used,
               self.sections_used)


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    domain_name = db.Column(db.Text, nullable=False)
    wikipedia_score = db.Column(db.Integer)
    wikipedia_domain = db.Column(db.Integer)
    search_result_score = db.Column(db.String(15))
    en_title = db.Column(db.Text)
    wd_q_id = db.Column(db.String(20), nullable=False)
    twitter_handle = db.Column(db.String(25), nullable=False)
    twitter_followers = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Domain({}, {}, {}, {}, {}, {}, {}, {})".format(
               self.domain_name,
               self.wikipedia_score,
               self.wikipedia_domain,
               self.search_result_score,
               self.en_title,
               self.wd_q_id,
               twitter_handle,
               twitter_followers)
