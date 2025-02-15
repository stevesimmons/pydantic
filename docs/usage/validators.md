Custom validation and complex relationships between objects can be achieved using the `validator` decorator.

```py
{!./examples/validators_simple.py!}
```
_(This script is complete, it should run "as is")_

A few things to note on validators:

* validators are "class methods", so the first argument value they receive is the `UserModel` class, not an instance
  of `UserModel`.
* the second argument is always the field value to validate; it can be named as you please
* you can also add any subset of the following arguments to the signature (the names **must** match):
    * `values`: a dict containing the name-to-value mapping of any previously-validated fields 
    * `config`: the model config
    * `field`: the field being validated
    * `**kwargs`: if provided, this will include the arguments above not explicitly listed in the signature  
* validators should either return the parsed value or raise a `ValueError`, `TypeError`, or `AssertionError`
  (``assert`` statements may be used).

!!! warning
    If you make use of `assert` statements, keep in mind that running
    Python with the [`-O` optimization flag](https://docs.python.org/3/using/cmdline.html#cmdoption-o)
    disables `assert` statements, and **validators will stop working**.

* where validators rely on other values, you should be aware that:

    - Validation is done in the order fields are defined.
      E.g. in the example above, `password2` has access to `password1` (and `name`),
      but `password1` does not have access to `password2`. See [Field Ordering](models.md#field-ordering)
      for more information on how fields are ordered

    - If validation fails on another field (or that field is missing) it will not be included in `values`, hence
      `if 'password1' in values and ...` in this example.

## Pre and per-item validators

Validators can do a few more complex things:

```py
{!./examples/validators_pre_item.py!}
```
_(This script is complete, it should run "as is")_

A few more things to note:

* a single validator can be applied to multiple fields by passing it multiple field names
* a single validator can also be called on *all* fields by passing the special value `'*'`
* the keyword argument `pre` will cause the validator to be called prior to other validation
* passing `each_item=True` will result in the validator being applied to individual values
  (e.g. of `List`, `Dict`, `Set`, etc.), rather than the whole object

## Validate Always

For performance reasons, by default validators are not called for fields when a value is not supplied.
However there are situations where it may be useful or required to always call the validator, e.g.
to set a dynamic default value.

```py
{!./examples/validators_always.py!}
```
_(This script is complete, it should run "as is")_

You'll often want to use this together with `pre`, since otherwise with `always=True`
*pydantic* would try to validate the default `None` which would cause an error.

## Root Validators

Validation can also be performed on the entire model's data.

```py
{!./examples/validators_root.py!}
```
_(This script is complete, it should run "as is")_

As with field validators, root validators can have `pre=True`, in which case they're called before field
validation occurs (and are provided with the raw input data), or `pre=False` (the default), in which case
they're called after field validation.

Field validation will not occur if `pre=True` root validators raise an error. As with field validators,
"post" (i.e. `pre=False`) root validators will be called even if field validation fails; the `values` argument will
be a dict containing the values which passed field validation and field defaults where applicable.

## Field Checks

On class creation, validators are checked to confirm that the fields they specify actually exist on the model.

Occasionally however this is undesirable: e.g. if you define a validator to validate fields on inheriting models.
In this case you should set `check_fields=False` on the validator.

## Dataclass Validators

Validators also work with *pydantic* dataclasses.

```py
{!./examples/validators_dataclass.py!}
```
_(This script is complete, it should run "as is")_
