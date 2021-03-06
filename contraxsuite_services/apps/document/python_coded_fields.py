import importlib
import logging
from typing import List, Any, Tuple, Dict

from django.conf import settings


class PythonCodedField:
    code = ''
    title = ''
    type = ''

    # If true - detect field values separately in each sentence.
    # If false - run get_values() against the whole document and next try to find matching text unit (sentence)
    #            for each detected value.
    # see apps.document.tasks.detect_field_values_for_python_coded_field()
    by_sentence = True

    def get_values(self, text: str) -> List[Tuple[Any, int, int]]:
        """
        Locates field values in text - either in a sentence or in a whole document text
        (depending on 'by_sentence' flag).
        :param text: Sentence or whole document text.
        :return: List of tuples: (value, location_start, location_end)
        """
        raise NotImplemented()


# Registry of Python-coded fields in the form of: code -> PythonCodedField descendant instance.
# DocumentField.python_coded_field can have one of field codes as its value.
# In this case field values will be detected using the methods of PythonCodedField descendant registered in
# this dictionary.
PYTHON_CODED_FIELDS_REGISTRY = {}  # type: Dict[str, PythonCodedField]


def init_field_registry():
    """
    Searches for module called 'python_coded_fields' in each app. If there is such module and it has
    'PYTHON_CODED_FIELDS' list attribute in it then try to add each field from this list to
    PYTHON_CODED_FIELDS_REGISTRY.
    Additionally updates choice values of DocumentField.python_coded_field model.
    :return:
    """
    logging.info('Going to register Python-coded document fields from all Django apps...')
    custom_apps = [i for i in settings.INSTALLED_APPS if i.startswith('apps.')]
    for app_name in custom_apps:
        module_str = '%s.python_coded_fields' % app_name
        try:
            fields_module = importlib.import_module(module_str)
            if hasattr(fields_module, 'PYTHON_CODED_FIELDS'):
                fields = fields_module.PYTHON_CODED_FIELDS

                try:
                    fields = list(fields)
                except TypeError:
                    raise TypeError('{0}.PYTHON_CODED_FIELDS is not iterable'.format(module_str))

                i = -1
                for field in fields:
                    i += 1
                    try:
                        PYTHON_CODED_FIELDS_REGISTRY[field.code] = field
                    except AttributeError:
                        raise AttributeError('{0}.PYTHON_CODED_FIELDS[{1}] is something wrong'.format(module_str, i))
                    print('Registered python-coded document field: {0} ({1})'.format(field.title, field.code))

        except ImportError:
            continue

    from apps.document.models import DocumentField
    for f in DocumentField._meta.fields:
        if f.name == 'python_coded_field':
            f.choices = list((k, PYTHON_CODED_FIELDS_REGISTRY[k].title or k)
                             for k in sorted(PYTHON_CODED_FIELDS_REGISTRY))
            break
