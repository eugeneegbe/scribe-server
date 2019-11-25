from datetime import datetime
from scribe import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    wd_q_id = db.Column(db.String(10), unique=True)
    lang_code = db.Column(db.String(3))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Article({}, {}, {})".format(
               self.name,
               self.wd_q_id,
               self.lang_code)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    label = db.Column(db.String(25), unique=True, nullable=False)
    article_name = db.Column(db.String(10))
    lang_code = db.Column(db.String(3))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Section({}, {}, {})".format(
               self.label,
               self.article_name,
               self.lang_code)

class Edit(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    article_name = db.Column(db.String(40), unique=True, nullable=False)
    section_label = db.Column(db.String(10))
    content = db.Column(db.Text)
    url = db.Column(db.Text)
    domain = db.Column(db.String(10))
    lang_code = db.Column(db.String(3))
    date = db.Column(db.Date, nullable=False,
                     default=datetime.now().strftime('%Y-%m-%d'))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Change({}, {}, {}, {}, {}, {})".format(
               self.article_name,
               self.section_label,
               self.content,
               self.domain,
               self.url,
               self.lang_code)
