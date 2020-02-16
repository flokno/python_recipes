#!/usr/bin/env python
# coding: utf-8

import collections
import hashlib
import inspect
import json
from pathlib import Path

import xarray as xr


def get_hash(x):
    """hash x and digest"""
    return hashlib.sha1(x).hexdigest()


keys = {
    k: k
    for k in (
        "hash",
        "hash_input",
        "hash_function",
        "cache",
        "function_name",
        "function_signature",
    )
}

keys = collections.namedtuple("keys", keys.keys())(**keys)


_path_cache = Path(keys.cache)
_path_log = _path_cache / f"{keys.hash}.json"


def cached(func):
    """Provides on-disk cache for a function that accepts and returns an xarray.DataArray"""
    name = func.__name__

    def _func(array, **kwargs):
        signature = get_signature_dict(func, array, kwargs)
        signature_str = json.dumps(signature)

        # create hashes
        hash_input = array.attrs.get(keys.hash, "")  # hash input array
        hash_function = get_hash(signature_str.encode())  # hash the function
        input_function_str = hash_function.encode() + hash_input.encode()
        hash_output = get_hash(input_function_str)  # hash output array

        filename = cache_filename(array, name)

        # look up if the result is already cached in the local cache folder
        hash_lookup = log_lookup(filename)

        if hash_lookup == hash_output:
            return cache_read(filename)  # return the cached result

        # otherwise compute and attach metainfo
        result = func(array=array, **kwargs)
        attrs = {
            keys.hash_input: hash_input,
            keys.function_signature: signature_str,
            keys.hash_function: hash_function,
            keys.hash: hash_output,
        }
        result.attrs.update(attrs)

        cache_write(result, filename)

        return result

    return _func


def log_update(filename, hash_str):
    """Update the hash logfile with current `filename: hash` pair"""
    path = _path_log
    log = {}
    if path.exists():
        log = json.load(path.open())
    log.update({filename: hash_str})

    with path.open("w") as f:
        json.dump(log, f, indent=2)


def log_lookup(filename):
    """lookup hash for given filename"""
    path = _path_log
    if path.exists():
        log = json.load(path.open())
        return log.get(filename)


def function_name_from_attrs(attrs):
    """helper: extract function name from attrs"""
    s = json.loads(attrs[keys.function_signature])
    return s["__name__"]


def cache_filename(array, function_name):
    """determine filename for cache-file from the function name"""
    assert isinstance(array, xr.DataArray)
    return str(function_name) + ".nc"


def cache_write(array, filename):
    """write array to the cache"""
    h = array.attrs[keys.hash]  # extract hash
    file = _path_cache / filename
    file.parent.mkdir(exist_ok=True)  # make sure folder exists
    array.to_netcdf(file)
    # update hash.json
    log_update(filename, h)


def cache_read(filename):
    """read file in cache folder"""
    path = _path_cache / filename
    array = xr.load_dataarray(path)
    return array


def get_signature_dict(func, array, kwargs):
    """add the function signature dictionary"""
    s = inspect.signature(func)
    dct = {"__name__": func.__name__}
    dct.update({k: v.default for (k, v) in s.parameters.items()})
    dct.update(kwargs)  # update the signature
    dct.update({"__type__": str(type(array))})  # add data type
    dct.pop("kwargs", None)  # pop literal "kwargs" (if they were empty)

    return dct
