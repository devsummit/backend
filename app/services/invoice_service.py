from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.invoices import Invoice
from app.models.base_model import BaseModel
from app.models.partners import Partner
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class InvoiceService(BaseService):

    def get(self):
        response = ResponseBuilder()
        invoices = db.session.query(Invoice).all()
        return response.set_data(BaseModel.as_list(invoices)).set_message('invoices retrieved successfully').build()

    def show(self, id):
        response = ResponseBuilder()
        invoice = db.session.query(Invoice).filter_by(id=id).first()
        included = None
        if invoice is None:
            return response.set_error(True).set_data(None).set_message('invoice not found').build()
        if(invoice.invoiceable_type == 'partners'):
            # include partner data here.
            partner = db.session.query(Partner).filter_by(id=invoice.invoiceable_id).first()
            if partner is not None:
                included = partner.as_dict()
        return response.set_data(invoice.as_dict()).set_included(included).set_message('invoice retrieved succesfully').build()

    def create(self, payload):
        response = ResponseBuilder()
        invoice = Invoice()
        invoice.payload = payload['description'] if 'description' in payload else ''
        invoice.total = payload['total'] if 'total' in payload else None
        invoice.address = payload['address'] if 'address' in payload else ''
        invoice.description = payload['description'] if 'description' in payload else ''
        invoice.invoiceable_type = payload['invoiceable_type'] if 'invoiceable_type' in payload else ''
        invoice.invoiceable_id = payload['invoiceable_id'] if 'invoiceable_id' in payload else ''
        if invoice.total is None:
            return response.set_data(None).set_error(True).build()
        else:
            db.session.add(invoice)
            try:
                db.session.commit()
                return response.set_data(invoice.as_dict()).set_message('invoice created').build()
            except SQLAlchemyError as e:
                data = e.orig.args
                return response.set_data(None).set_message(data).set_error(True).build()