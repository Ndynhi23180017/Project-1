from config import vd, ttk


class ValidationUtils:
    @staticmethod
    def validate_nullable(entry: ttk.Entry):
        '''
        Validate nullable
        '''
        def _null(event: vd.ValidationEvent):
            ValidationUtils.check_status = bool(event.postchangetext)
            return ValidationUtils.check_status
        vd.add_validation(entry, _null)
            