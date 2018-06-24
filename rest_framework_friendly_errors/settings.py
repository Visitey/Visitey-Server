from __future__ import unicode_literals

from django.conf import settings
from rest_framework import exceptions as drf

from .utils import update_field_settings

USER_SETTINGS = getattr(settings, 'DRF_ERRORS', {})

USER_FRIENDLY_FIELD_ERRORS = USER_SETTINGS.get('FIELD_ERRORS', {})
USER_NON_FIELD_ERRORS = USER_SETTINGS.get('NON_FIELD_ERRORS', {})
USER_VALIDATOR_ERRORS = USER_SETTINGS.get('VALIDATOR_ERRORS', {})
USER_EXCEPTION_DICT = USER_SETTINGS.get('EXCEPTION_DICT', {})
USER_ERROR_CODES = USER_SETTINGS.get('ERROR_CODES', {})

CATCH_ALL_EXCEPTIONS = USER_SETTINGS.get(
    'CATCH_ALL_EXCEPTIONS', False)

ERROR_CODE_REQUIRED = 'required'
ERROR_CODE_INVALID = 'invalid'
ERROR_CODE_NULL = 'null'
ERROR_CODE_BLANK = 'blank'
ERROR_CODE_MAX_LENGTH = 'max_length'
ERROR_CODE_MIN_LENGTH = 'min_length'
ERROR_CODE_INVALID_CHOICE = 'invalid_choice'
ERROR_CODE_MAX_STRING_LENGTH = 'max_string_length'
ERROR_CODE_MIN_VALUE = 'min_value'
ERROR_CODE_MAX_VALUE = 'max_value'
ERROR_CODE_MAX_WHOLE_DIGITS = 'max_whole_digits'
ERROR_CODE_MAX_DIGITS = 'max_digits'
ERROR_CODE_MAX_DECIMAL_PLACES = 'max_decimal_places'
ERROR_CODE_NOT_A_LIST = 'not_a_list'
ERROR_CODE_EMPTY = 'empty'
ERROR_CODE_NO_NAME = 'no_name'
ERROR_CODE_INVALID_IMAGE = 'invalid_image'
ERROR_CODE_NOT_A_DICT = 'not_a_dict'
ERROR_CODE_DOES_NOT_EXIST = 'does_not_exist'
ERROR_CODE_INCORRECT_TYPE = 'incorrect_type'
ERROR_CODE_INCORRECT_MATCH = 'incorrect_match'
ERROR_CODE_NO_MATCH = 'no_match'
ERROR_CODE_DATE = 'date'
ERROR_CODE_DATETIME = 'datetime'
ERROR_CODE_MAKE_AWARE = 'make_aware'
ERROR_CODE_OVERFLOW = 'overflow'
ERROR_CODE_UNIQUE = 'unique'
ERROR_CODE_DATE_UNIQUE = 'date_unique'
ERROR_CODE_MONTH_UNIQUE = 'month_unique'
ERROR_CODE_YEAR_UNIQUE = 'year_unique'

FRIENDLY_ERROR_CODES = {
    'required': ERROR_CODE_REQUIRED,
    'invalid': ERROR_CODE_INVALID,
    'null': ERROR_CODE_NULL,
    'blank': ERROR_CODE_BLANK,
    'max_length': ERROR_CODE_MAX_LENGTH,
    'min_length': ERROR_CODE_MIN_LENGTH,
    'invalid_choice': ERROR_CODE_INVALID_CHOICE,
    'max_string_length': ERROR_CODE_MAX_STRING_LENGTH,
    'min_value': ERROR_CODE_MIN_VALUE,
    'max_value': ERROR_CODE_MAX_VALUE,
    'max_whole_digits': ERROR_CODE_MAX_WHOLE_DIGITS,
    'max_digits': ERROR_CODE_MAX_DIGITS,
    'max_decimal_places': ERROR_CODE_MAX_DECIMAL_PLACES,
    'not_a_list': ERROR_CODE_NOT_A_LIST,
    'empty': ERROR_CODE_EMPTY,
    'no_name': ERROR_CODE_NO_NAME,
    'invalid_image': ERROR_CODE_INVALID_IMAGE,
    'not_a_dict': ERROR_CODE_NOT_A_DICT,
    'does_not_exist': ERROR_CODE_DOES_NOT_EXIST,
    'incorrect_type': ERROR_CODE_INCORRECT_TYPE,
    'incorrect_match': ERROR_CODE_INCORRECT_MATCH,
    'no_match': ERROR_CODE_NO_MATCH,
    'date': ERROR_CODE_DATE,
    'datetime': ERROR_CODE_DATETIME,
    'make_aware': ERROR_CODE_MAKE_AWARE,
    'overflow': ERROR_CODE_OVERFLOW,
    'unique': ERROR_CODE_UNIQUE,
    'date_unique': ERROR_CODE_DATE_UNIQUE,
    'month_unique': ERROR_CODE_MONTH_UNIQUE,
    'year_unique': ERROR_CODE_YEAR_UNIQUE,
}
FRIENDLY_ERROR_CODES.update(USER_ERROR_CODES)

FRIENDLY_FIELD_ERRORS = {
    'BooleanField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null']
    },
    'NullBooleanField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null']
    },
    'CharField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'blank': FRIENDLY_ERROR_CODES['blank'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'EmailField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'blank': FRIENDLY_ERROR_CODES['blank'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'RegexField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'blank': FRIENDLY_ERROR_CODES['blank'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'SlugField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'blank': FRIENDLY_ERROR_CODES['blank'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'URLField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'blank': FRIENDLY_ERROR_CODES['blank'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'UUIDField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'blank': FRIENDLY_ERROR_CODES['blank'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'FilePathField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'invalid_choice': FRIENDLY_ERROR_CODES['invalid_choice'],
    },
    'IPAddressField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'blank': FRIENDLY_ERROR_CODES['blank'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'IntegerField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'max_string_length': FRIENDLY_ERROR_CODES['max_string_length'],
        'min_value': FRIENDLY_ERROR_CODES['min_value'],
        'max_value': FRIENDLY_ERROR_CODES['max_value'],
    },
    'FloatField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'max_string_length': FRIENDLY_ERROR_CODES['max_string_length'],
        'min_value': FRIENDLY_ERROR_CODES['min_value'],
        'max_value': FRIENDLY_ERROR_CODES['max_value'],
    },
    'DecimalField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'max_string_length': FRIENDLY_ERROR_CODES['max_string_length'],
        'min_value': FRIENDLY_ERROR_CODES['min_value'],
        'max_value': FRIENDLY_ERROR_CODES['max_value'],
        'max_whole_digits': FRIENDLY_ERROR_CODES['max_whole_digits'],
        'max_digits': FRIENDLY_ERROR_CODES['max_digits'],
        'max_decimal_places': FRIENDLY_ERROR_CODES['max_decimal_places'],
    },
    'ChoiceField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'invalid_choice': FRIENDLY_ERROR_CODES['invalid_choice'],
    },
    'MultipleChoiceField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'invalid_choice': FRIENDLY_ERROR_CODES['invalid_choice'],
        'not_a_list': FRIENDLY_ERROR_CODES['not_a_list'],
        'empty': FRIENDLY_ERROR_CODES['empty'],
    },
    'FileField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'empty': FRIENDLY_ERROR_CODES['empty'],
        'no_name': FRIENDLY_ERROR_CODES['no_name'],
    },
    'ImageField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'empty': FRIENDLY_ERROR_CODES['empty'],
        'no_name': FRIENDLY_ERROR_CODES['no_name'],
        'invalid_image': FRIENDLY_ERROR_CODES['invalid_image'],
    },
    'ListField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'not_a_list': FRIENDLY_ERROR_CODES['not_a_list'],
        'empty': FRIENDLY_ERROR_CODES['empty'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
        'min_length': FRIENDLY_ERROR_CODES['min_length'],
    },
    'DictField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'not_a_dict': FRIENDLY_ERROR_CODES['not_a_dict'],
        'empty': FRIENDLY_ERROR_CODES['empty'],
    },
    'JSONField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'null': FRIENDLY_ERROR_CODES['null'],
    },
    'StringRequiredField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
    },
    'PrimaryKeyRelatedField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'does_not_exist': FRIENDLY_ERROR_CODES['does_not_exist'],
        'incorrect_type': FRIENDLY_ERROR_CODES['incorrect_type'],
    },
    'HyperlinkedRelatedField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'does_not_exist': FRIENDLY_ERROR_CODES['does_not_exist'],
        'incorrect_type': FRIENDLY_ERROR_CODES['incorrect_type'],
        'incorrect_match': FRIENDLY_ERROR_CODES['incorrect_match'],
        'no_match': FRIENDLY_ERROR_CODES['no_match'],
    },
    'SlugRelatedField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'does_not_exist': FRIENDLY_ERROR_CODES['does_not_exist'],
        'incorrect_type': FRIENDLY_ERROR_CODES['incorrect_type'],
    },
    'HyperlinkedIdentityField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'does_not_exist': FRIENDLY_ERROR_CODES['does_not_exist'],
        'incorrect_type': FRIENDLY_ERROR_CODES['incorrect_type'],
        'incorrect_match': FRIENDLY_ERROR_CODES['incorrect_match'],
        'no_match': FRIENDLY_ERROR_CODES['no_match'],
    },
    'ManyRelatedField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'invalid_choice': FRIENDLY_ERROR_CODES['invalid_choice'],
        'not_a_list': FRIENDLY_ERROR_CODES['not_a_list'],
        'empty': FRIENDLY_ERROR_CODES['empty'],
    },
    'ReadOnlyField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
    },
    'HiddenField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
    },
    'ModelField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
    },
    'SerializerMethodField': {
        'required': FRIENDLY_ERROR_CODES['required'],
        'null': FRIENDLY_ERROR_CODES['null'],
        'max_length': FRIENDLY_ERROR_CODES['max_length'],
    },
    'DateTimeField': {
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'date': FRIENDLY_ERROR_CODES['date'],
        'make_aware': FRIENDLY_ERROR_CODES['make_aware'],
        'overflow': FRIENDLY_ERROR_CODES['overflow'],
    },
    'DateField': {
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
        'datetime': FRIENDLY_ERROR_CODES['datetime'],
    },
    'TimeField': {
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
    },
    'DurationField': {
        'invalid': FRIENDLY_ERROR_CODES['invalid'],
    },
}

FRIENDLY_FIELD_ERRORS = update_field_settings(FRIENDLY_FIELD_ERRORS,
                                              USER_FRIENDLY_FIELD_ERRORS)

INVALID_DATA_MESSAGE = 'Invalid data. Expected a dictionary, ' \
                       'but got {data_type}.'

FRIENDLY_NON_FIELD_ERRORS = {
    'invalid': FRIENDLY_ERROR_CODES['invalid']
}

FRIENDLY_NON_FIELD_ERRORS.update(USER_NON_FIELD_ERRORS)

FRIENDLY_VALIDATOR_ERRORS = {
    'UniqueValidator': FRIENDLY_ERROR_CODES['unique'],
    'UniqueTogetherValidator': FRIENDLY_ERROR_CODES['unique'],
    'UniqueForDateValidator': FRIENDLY_ERROR_CODES['date_unique'],
    'UniqueForMonthValidator': FRIENDLY_ERROR_CODES['month_unique'],
    'UniqueForYearValidator': FRIENDLY_ERROR_CODES['year_unique'],
    'RegexValidator': FRIENDLY_ERROR_CODES['invalid'],
    'EmailValidator': FRIENDLY_ERROR_CODES['invalid'],
    'URLValidator': FRIENDLY_ERROR_CODES['invalid'],
    'MaxValueValidator': FRIENDLY_ERROR_CODES['max_value'],
    'MinValueValidator': FRIENDLY_ERROR_CODES['min_value'],
    'MaxLengthValidator': FRIENDLY_ERROR_CODES['max_length'],
    'MinLengthValidator': FRIENDLY_ERROR_CODES['min_length'],
    'DecimalValidator': FRIENDLY_ERROR_CODES['invalid'],
    'validate_email': FRIENDLY_ERROR_CODES['invalid'],
    'validate_slug': FRIENDLY_ERROR_CODES['invalid'],
    'validate_unicode_slug': FRIENDLY_ERROR_CODES['invalid'],
    'validate_ipv4_address': FRIENDLY_ERROR_CODES['invalid'],
    'validate_ipv46_address': FRIENDLY_ERROR_CODES['invalid'],
    'validate_comma_separated_integer_list': FRIENDLY_ERROR_CODES['invalid'],
    'int_list_validator': FRIENDLY_ERROR_CODES['invalid'],
}

FRIENDLY_VALIDATOR_ERRORS.update(USER_VALIDATOR_ERRORS)


FRIENDLY_EXCEPTION_DICT = {
    'APIException': getattr(drf.APIException, 'default_code', 'error'),
    'ParseError': getattr(drf.ParseError, 'default_code', 'parse_error'),
    'AuthenticationFailed': getattr(drf.AuthenticationFailed, 'default_code',
                                    'authentication_failed'),
    'NotAuthenticated': getattr(drf.NotAuthenticated, 'default_code',
                                'not_authenticated'),
    'PermissionDenied': getattr(drf.PermissionDenied, 'default_code',
                                'permission_denied'),
    'NotFound': getattr(drf.NotFound, 'default_code', 'not_found'),
    'MethodNotAllowed': getattr(drf.MethodNotAllowed, 'default_code',
                                'method_not_allowed'),
    'NotAcceptable': getattr(drf.NotAcceptable, 'default_code',
                             'not_acceptable'),
    'UnsupportedMediaType': getattr(drf.UnsupportedMediaType, 'default_code',
                                    'unsupported_media_type'),
    'Throttled': getattr(drf.Throttled, 'default_code', 'throttled')
}
FRIENDLY_EXCEPTION_DICT.update(USER_EXCEPTION_DICT)
