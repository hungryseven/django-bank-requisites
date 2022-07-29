# Django Bank Requisites

# Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Working with Django](#working-with-django)
  - [Working with DRF](#working-with-drf)
  - [Validators](#validators)
- [Available model/serializer fields](#available-modelserializer-fields)
- [License](#license)

# Overview

This package provides models, serializers, mixins and validators for russian bank details such as
INN, KPP, BIK, RS, KS, OGRN and so on.

# Requirements

- Python (3.5+)
- Django (3, 4)
- Django REST framework (3.10+)

# Installation
```pip install django-bank-requisites```

# Usage

## Working with Django

If you work only with Django (admin, forms, etc.), simply inherit your model from ```BankDetailsValidated``` abstract model.\
This model has all bank details validation steps on field-level and ```clean``` method.

```
from django_bank_requisites.models import BankDetailsValidated
  
class OrganizationModel(BankDetailsValidated):
  pass
```

## Working with DRF

You have several options when you work with DRF.

1. Inherit your model from ```BankDetailsUnValidated``` abstract model. This abstract model doesn't have any validation on it's own level:

```
from django_bank_requisites.models import BankDetailsUnvalidated
  
class OrganizationModel(BankDetailsUnvalidated):
  pass
```

The next step is create ```ModelSerializer```. Since your model doesn't have any validation, you should provide it for serializer.

```
from django_bank_requisites.mixin import BankDetailsValidationMixin

class OrganizationSerializer(BankDetailsValidationMixin, serializers.ModelSerializer):
  
  # It's important to inherit BankDetailsValidationMixin Meta class
  # to have serializer field-level validation
  class Meta(BankDetailsValidationMixin.Meta):
    model = OrganizationModel
    field = "__all__"
```

2. If you use ```BankDetailsValidated``` abstract model with all validation on model level and want validation from ```clean``` method works in serializer you also should inherit your model from ```SaveMethodMixin```:

```
from django_bank_requisites.models import BankDetailsValidated
from django_bank_requisites.mixins import SaveMethodMixin
  
class OrganizationModel(SaveMethodMixin, BankDetailsValidated):
  pass
```

If you leave everything as it is, you will get a ```HTTP 500 Internal Server Error```, because Django REST framework doesn't handle ```ValidationError``` from Django.

In order for DRF to correctly handle ```ValidationError``` from Django, you should add custom exception handler to ```REST_FRAMEWORK``` settings dict in your ```settings.py``` file.

```
REST_FRAMEWORK = {
  ...
  'EXCEPTION_HANDLER': 'django_bank_requisites.exception_handler.exception_handler',
  ...
}
```

Now DRF will handle Django ```ValidationError``` correctly with a ```HTTP 400 Bad Request```.

3. If you use ```BankDetailsValidated``` abstract model with all validation on model level and don't want to bother with ```SaveMethodMixin``` and exception handler, you can implement the same validation from model ```clean``` method in serializer ```validate``` method:

Inherit your model from ```BankDetailsValidated``` abstract model:

```
from django_bank_requisites.models import BankDetailsValidated
  
class OrganizationModel(BankDetailsValidated):
  pass
```

Then add ```BankDetailsValidationMixin``` to your serializer:

```
from django_bank_requisites.mixin import BankDetailsValidationMixin

class OrganizationSerializer(BankDetailsValidationMixin, serializers.ModelSerializer):
  
  class Meta:
    model = OrganizationModel
    field = "__all__"
```

4. Also you can use non-model serializer with all validation steps:

```
from django_bank_requisites.serializers import BankDetailsSerializer
```

## Validators

This package provides a lot of built-in bank details validators for both Django and Python, so you can create your own models and serializers.

Base validators from ```base_validators.py``` are not framework bound. They are implemented on Python-level and simply return ```True/False```.

Django validators from ```django_validators.py``` are made up of base validators and raise Django ```ValidationError``` on validation fails.

# Available model/serializer fields

Currently the following fields are available in models and serializers:
- Legal address
- Bank name
- INN
- KPP
- BIK
- RS
- KS

# License

See [License](LICENSE.md).
