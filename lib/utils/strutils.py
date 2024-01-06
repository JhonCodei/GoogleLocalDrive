"""

@author: eocampo
This module manages OS operations.  All OS specfic should br handled here.

Modification History
date-author-description

"""

__version__ = '20181113'

import re
import sys,os
import datetime



def cleanse_data(s, regexp='[^0-9a-zA-Z,#, ]+', rep_str=''):
    #regexp='[^0-9a-zA-Z,#]+' # Acepta alpha numeric y '#'
    return re.sub(regexp, rep_str, s)

def clear_str(strg):
    strg = strg.strip()
    return strg.replace(",", "").replace("Ã‘", "Ñ").replace("=", "").replace("-", " ").replace('"', "").replace("'", "")

def _str_len_rp(s, ln=8, rp='0'):

    rc = to_str(s)

    if len(rc) != ln:
        rc = rc[:ln].rjust(ln, rp)
    return rc

def _time_complete(f, n):

    regexp = '[^0-9]+'

    f = to_int(to_float(cleanse_data(f, regexp)))
    n = to_int(to_float(cleanse_data(n, regexp)))

    if n > f or n == f:
        return True
    return False

def float_to_full_date(log, s):

    log.info(f" set vars => {s}")
    s = to_float(s)
    try:
        temp  = datetime.datetime(1900, 1, 1)
        delta = datetime.timedelta(days=s)

        log.info(f" set time => {temp + delta}")
        return temp + delta

    except ValueError as e: return None
    except TypeError  as e: return None

def removeNull(s):
    if len(s) == 0 or s == '':
        return 0
    return s

def to_dig_ubigeo(s, logger, dl='*'):

    df = '000000'
    s  = to_str(s)

    if dl not in s:
        return df

    spl = s.split(dl)

    if len(spl) != 3:
        return df

    dps = spl[0]
    pvs = spl[1]
    dss = spl[2]

    if len(to_str(dps)) == 0:
        return df

    if len(to_str(pvs)) == 0:
        return df

    if len(to_str(dss)) == 0:
        return df

    dp = _str_len_rp( to_int( to_float( dps ) ), 2, '0' )
    pv = _str_len_rp( to_int( to_float( pvs ) ), 2, '0' )
    ds = _str_len_rp( to_int( to_float( dss ) ), 2, '0' )

    return f"{dp}{pv}{ds}"

def _to_date(s, log, dl='/'):

    rt = None
    ls = []
    y  = None
    m  = None
    d  = None

    try:
        if " " in s:
            log.critical(f"date dl -> space ' '")
            s = s.split(" ")
            if len(s) != 2:
                return rt
            if dl in s[0]:
                ls = s.split(dl)
        else:
            log.critical(f"date dl -> / ")
            if dl in s:
                ls = s.split(dl)
                #log.critical(f"date ls = {len(ls)},-> {ls}")
        if len(ls) != 3:
            return rt

        if dl == '-':
            y = ls[0]
            m = ls[1]
            d = ls[2]
            rt = f"{d}/{m}/{y}"

        elif dl == '/':
            y = ls[2]
            m = ls[1]
            d = ls[0]
            rt = f"{y}-{m}-{d}"
    except Exception as e:
        log.error(f"error _to_date, detail => {e}")
        log.error(f"error _to_date, out => {sys.exc_info()}")
    finally:
        log.critical(f"date is -> {rt}")
        return rt

def to_str(s):
    try:
        s = str(s)
        return s

    except ValueError: return None
    except TypeError : return None

def to_int(s):
    if type(s) is str: s = s.rstrip()
    try:
        i = int(s)
        return i

    except ValueError: return None
    except TypeError : return None

def to_int_zero(s):
    if type(s) is str: s = s.rstrip()
    try:
        i = int(s)
        return i

    except ValueError: return 0
    except TypeError : return 0

def to_float(s):
    if type(s) is str: s=s.rstrip()
    try:
        i = float(s)
        return i

    except ValueError: return None
    except TypeError : return None

def to_float_zero(s):
    if type(s) is str: s=s.rstrip()
    try:
        i = float(s)
        return i

    except ValueError: return 0.0
    except TypeError : return 0.0

def is_valid_email(email):

    regx = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

    if len(email) > 7:
        if re.match(regx, email) is not None:
            return True
    return False

def is_empty(s):
    if s and s.strip():
        return False
    return True

# l complete list
# n chunk size

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# msg string to check
# stf string to find
# 0 if string was found.
def find_str(msg, stf):

    rc = 1
    if msg is None or len(msg) < 2:
        return rc
    fstr = re.compile(r"%s" % stf, re.IGNORECASE)
    resp = re.findall(fstr, msg)
    if resp:
        rc = 0
    return rc

# returns a date string based on fmt mask.
def get_today_str(fmt='%m/%d/%Y'):
    d = datetime.datetime.now()
    return d.strftime(fmt)

def time_email():
    import time
    t = time.ctime(time.time())
    return to_str(t)

def _nowTime():
	timeNow = datetime.datetime.now()
	tnow    = timeNow.strftime("%Y-%m-%d %H:%M:%S")
	return tnow

def _now_folder_bk():
	timeNow = datetime.datetime.now()
	tnow    = timeNow.strftime("%Y_%m_%d")
	return tnow

def _nowHour():
	timeNow = datetime.datetime.now()
	tnow    = timeNow.strftime("%H:%M:%S")
	return tnow

def build_query(log, sql, target=[], vars=[]):

    log.info("Construyendo Query fc:build_query")

    if len(target) != len(vars):

        log.error(f"no son iguales")
        log.error(f'Except {sys.exc_info()}')
    else:

        for tg in target:
            if tg in sql:
                pass
        else:
            log.error(f"{tg} no existe en \n {sql}")
            log.error(f'Except {sys.exc_info()}')
    x = 0
    for i in range(len(target)):
        if x == 0:
            rt = sql.replace(str(target[i]), str(vars[i]))
        else:
            rt = rt.replace(str(target[i]), str(vars[i]))
        x += 1
    return rt

def sql_target_to_ls(log, vars):
    rt = []

    if len(vars) == 0:
        log.error(f"fc: sql_target_to_ls => vars => vacio!! ")
        log.error(f'Except {sys.exc_info()}')

    v = vars.split(",")

    for d in v:
        rt.append(f":{d}")

    log.info(f"fc: ret => {rt}")
    return rt

def _int_to_date_db(s, prd):

    if len(to_str(s)) == 8:
        if len(to_str(prd)) == 6:
            y = prd[:4]
            m = prd[4:6]
            d = s[6:8]
            f = f"{y}-{m}-{d}"
            return f
    return s

def __str__encode__(s):
    return str.encode(s)

def _validate_date_(y, m, d):
    y = to_int(y)
    m = to_int(m)
    d = to_int(d)

    correctDate = None
    try:
        newDate = datetime.datetime(y, m, d)
        correctDate = True
    except ValueError:
        correctDate = False
    finally:
        return correctDate

def day_week(y, m, d):
    y = to_int(y)
    m = to_int(m)
    d = to_int(d)

    a = (14 - m) // 12
    y = y - a
    m = m + 12 * a - 2
    w = (d + y + (y//4) - (y//100) + (y//400) + ((31 * m)//12)) % 7
    return w

def _datetime_to_format(f, t='f'):

    f = to_str(f)

    try:
        format_str = '%Y-%m-%d %H:%M:%S' # The format
        datetime_obj = datetime.datetime.strptime(f, format_str)

        if t == 'h':
            return datetime_obj.time()
        return datetime_obj.date()

    except ValueError as e: return f

    #return f.strftime(fmt)
