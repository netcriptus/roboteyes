from sqlalchemy.exc import InvalidRequestError
from blinker import Namespace
from robot_eyes import db

__all__ = ()


signals = Namespace()
model_saved = signals.signal('model-saved')
model_new = signals.signal('model-new')
model_deleted = signals.signal('model-deleted')


class ModelMixin(object):

    def save(self, commit=True):
        new = self.id is None

        db.session.add(self)
        if commit:
            db.session.commit()
        model_saved.send(instance=self)
        if new:
            model_new.send(instance=self)

    def delete(self, commit=True):
        if self.id is None:
            return
        db.session.delete(self)
        if commit:
            db.session.commit()
        model_deleted.send(instance=self)

    def refresh(self):
        try:
            db.session.refresh(self)
        except InvalidRequestError:
            db.session.add(self)
