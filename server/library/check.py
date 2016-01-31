# -*- coding: utf-8 -*-
# 专门用来检查数据的
# 没有格式限制的数据一律base64, 有的话就检查格式
import re
try:
    from django.conf import settings
except:
    pass
TESTTING = False

def is_clean_input(key_name, data):
    binding = {
        'account':is_clean_account,
        'watchsum':is_clean_watchsum,
        'name':is_clean_name,
        'spnumber':is_clean_spnumber,
        'iswatching':is_clean_iswatching,
        'lpnumber':is_clean_lpnumber,
        'type':is_clean_type,
        'integer':is_clean_int,
    }
    if key_name in binding:
        return binding[key_name](data)
    return False

def is_clean_int(data):
    try:
        wsum = int(data)
        if -32767<=wsum<=32767:
            return True
    except:
        pass
    return False

def is_clean_float(data):
    try:
        float(data)
        return True
    except:
        return False

def is_clean_account(string):
    try:
        if not string:
            return True
        if TESTTING:
            root_user_name = 'root'
        else:
            root_user_name = settings.SUPER_USER
        print settings.SUPER_USER
        if string == root_user_name:
            return True
        if re.match(r'^(\d{10})$',string):
            return True
    except Exception as e:
        print e
        pass
    return False

def is_clean_watchsum(data):
    return is_clean_int(data)

def is_clean_name(data):
    return data!=None and data!=True and data!=False

def is_clean_spnumber(data):
    if not data:
        return True
    try:
        if re.match(r'^\d{6}$',data):
            return True
    except:
        pass
    return False

def is_clean_iswatching(data):
    try:
        return (data=='yes' or data=='no')
    except:
        return False

def is_clean_lpnumber(data):
    if not data:
        return True
    try:
        if re.match(r'^(\+\d\d)?\d{11}$',data):
            return True
    except:
        pass
    return False

def is_clean_type(data):
    return data in ['delete','new','normal']


if __name__=='__main__':
    TESTTING = True
    assert is_clean_int(0)
    assert is_clean_int(True)
    assert is_clean_int(False)
    assert is_clean_int('1234')
    assert not is_clean_int(None)
    assert not is_clean_int('123r')
    assert not is_clean_int('asdf')

    assert is_clean_float(0)
    assert is_clean_float(2.3)
    assert is_clean_float('2.3')
    assert is_clean_float(True)
    assert is_clean_float(False)
    assert not is_clean_float(None)
    assert not is_clean_float('2.3r')
    assert not is_clean_float('asdf')

    assert is_clean_account('2012052207')
    assert is_clean_account('root')
    assert is_clean_account('')
    assert is_clean_account(None)
    assert not is_clean_account('root_')
    assert not is_clean_account('20120522078')
    assert not is_clean_account('201205220')

    assert is_clean_watchsum(0)
    assert is_clean_watchsum(True)
    assert is_clean_watchsum(False)
    assert is_clean_watchsum('1234')
    assert not is_clean_watchsum(None)
    assert not is_clean_watchsum('123r')
    assert not is_clean_watchsum('asdf')

    assert is_clean_name('dengzuoheng')
    assert is_clean_name('drop table *')
    assert is_clean_name('')
    assert not is_clean_name(None)
    assert not is_clean_name(True)
    assert not is_clean_name(False)

    assert is_clean_spnumber('666666')
    assert is_clean_spnumber('')
    assert is_clean_spnumber(None)
    assert not is_clean_spnumber('7777777')
    assert not is_clean_spnumber('55555')
    assert not is_clean_spnumber('z')
    assert not is_clean_spnumber('zzzzzz')

    assert is_clean_iswatching('yes')
    assert is_clean_iswatching('no')
    assert not is_clean_iswatching(None)
    assert not is_clean_iswatching('er')
    assert not is_clean_iswatching('')

    assert is_clean_lpnumber('13723232323')
    assert is_clean_lpnumber('+8613723232323')
    assert not is_clean_lpnumber('1372626262')
    assert not is_clean_lpnumber('137262626262')
    assert is_clean_lpnumber('')

    TESTTING = False




